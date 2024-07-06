# Copyright (c) 2024 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Create agents for a (mini)kube orchestrator."""

from typing import Any, Dict, List, Optional, Tuple, Union

import base64
import hashlib
import json
import os
import random
import string
import threading
import time

from queue import Queue, Empty

import kopf
import requests

from kubernetes import client, config, stream

########################################################################
### Constants and helpers

POOLS_API_GROUP = 'agent.opentestfactory.org'
POOLS_API_VERSION = 'v1alpha1'
POOLS_KIND = 'pools'
AGENTS_URL_TMPL = '{pod}/agents'
AGENT_ID_URL_TMPL = '{pod}/agents/{agent_id}'
FILE_URL_TMPL = '{agent_url}/files/{file_id}'

REGISTRATION = {
    'apiVersion': 'opentestfactory.org/v1alpha1',
    'kind': 'AgentRegistration',
    'metadata': {'name': 'test agent'},
    'spec': {
        'tags': [],
        'encoding': 'utf-8',
        'script_path': '',
    },
}

REQUEST_TIMEOUT = 60
POD_TIMEOUT = 60


class OperatorException(Exception):
    """OperatorException class"""

    def __init__(self, msg, details=None):
        self.msg = msg
        self.details = details


class NotFound(OperatorException):
    """AgentNotFound exception."""


class PodError(OperatorException):
    """PodError exception."""


def _as_list(what: Union[str, List[str]]) -> List[str]:
    return [what] if isinstance(what, str) else what


def _get_path(src: Dict[str, Any], path: List[str], msg: Optional[str] = None) -> Any:
    if not path:
        return src
    try:
        return _get_path(src[path[0]], path[1:])
    except (KeyError, TypeError) as err:
        txt = msg or f"Failed to get custom resource property {'.'.join(path)}"
        raise KeyError(txt) from err


def _make_copy(what):
    return json.loads(json.dumps(what))


def _make_headers(token: Optional[str]) -> Optional[Dict[str, str]]:
    return {'Authorization': f'Bearer {token}'} if token else None


def _make_suffix(length: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def _make_resource_id(name: str) -> str:
    name_hash = hashlib.md5(name.encode()).hexdigest()[:10]
    return f'{name}-{name_hash}-{_make_suffix(length=5)}'


def _make_agent_name(claim_name: str) -> str:
    return f'{claim_name}-{_make_suffix(length=5)}'


########################################################################
### Properties handling


def _get_param_or_fail(
    source: Dict[str, Any], path: List[str], msg: Optional[str] = None
) -> Any:
    try:
        return _get_path(source, path, msg)
    except KeyError as err:
        raise kopf.PermanentError(err)


def _get_token(spec: Dict[str, Any], logger) -> Optional[str]:
    if not (secret_name := spec.get('orchestratorSecret')):
        return secret_name
    config.load_kube_config()
    core_api = client.CoreV1Api()
    try:
        secret = core_api.read_namespaced_secret(secret_name, 'default')
        return base64.b64decode(secret.data['token']).decode('utf-8')  # type: ignore
    except Exception as err:
        logger.error(str(err))
        raise NotFound(f'Cannot retrieve orchestrator token: {str(err)}') from err


def _get_pod() -> str:
    if not (pod := os.environ.get('ORCHESTRATOR_URL')):
        raise NotFound('Cannot retrieve orchestrator url, what for is this all about?')
    return pod


########################################################################
### /agents requests handling


def _register_agent(
    agent_name: str,
    url: str,
    tags: Union[str, List[str]],
    headers: Optional[Dict[str, str]],
    logger,
) -> requests.Response:
    REGISTRATION['spec']['tags'] = _as_list(tags)
    REGISTRATION['metadata']['name'] = agent_name
    logger.debug(
        f'Registering agent. Name: {agent_name}, tags: {REGISTRATION["spec"]["tags"]}.'
    )
    response = requests.post(
        url, json=REGISTRATION, headers=headers, timeout=REQUEST_TIMEOUT
    )

    if response.status_code != 201:
        raise kopf.PermanentError(
            f'Failed to register agent: error code {response.status_code}, {response.text}'
        )
    logger.debug(response.json()['message'])
    return response


def _deregister_agent(
    pod: str, agent_id: str, headers: Optional[Dict[str, str]], logger
) -> None:
    url = AGENT_ID_URL_TMPL.format(pod=pod, agent_id=agent_id)
    logger.debug(f'De-registering agent {agent_id}.')
    response = requests.delete(url, headers=headers, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200:
        raise kopf.PermanentError(
            f'Cannot de-register agent {agent_id}: {response.json()["message"]}'
        )
    logger.debug(response.json()['message'])


def _get_agents_uuids(
    url: str, headers: Optional[Dict[str, str]], logger
) -> List[Dict[str, Any]]:
    logger.debug(f'Retrieving registered agents from {url}.')
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200 or not 'items' in response.json():
        raise kopf.PermanentError(
            f'Cannot retrieve registered agents list: {response.json()["message"]}'
        )
    logger.debug('Agents list retrieved.')
    return [item['metadata']['agent_id'] for item in response.json()['items']]


def _register_agents_return_uuids(
    pool_size: int, resource_name: str, spec: Dict[str, Any], logger
) -> List[str]:
    agents = []
    tags, pod = _get_param_or_fail(spec, ['tags']), _get_pod()
    token = _get_token(spec, logger)
    for _ in range(pool_size):
        agent_name = _make_agent_name(resource_name)
        response = _register_agent(
            agent_name,
            AGENTS_URL_TMPL.format(pod=pod),
            tags,
            _make_headers(token),
            logger,
        )
        agents.append(response.json()['details']['uuid'])
    return agents


########################################################################
### Event handlers


@kopf.on.create(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND)  # type: ignore
def create_agents(spec, name, logger, **kwargs):
    try:
        pool_size = spec.get('poolSize', 0)
        if not isinstance(pool_size, int) or pool_size < 0:
            raise ValueError(f'Pool size must be a positive integer, got {pool_size}.')
        return {
            'agents': _register_agents_return_uuids(pool_size, name, spec, logger),
            'resource_id': _make_resource_id(name),
        }
    except Exception as err:
        raise kopf.PermanentError(f'Error while registering agents: {err}')


@kopf.on.delete(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND)  # type: ignore
def delete_agents(spec, status, logger, **kwargs):
    try:
        agents, pod = (
            _get_param_or_fail(
                status,
                ['create_agents', 'agents'],
                'This resource has no related agents, cannot delete any.',
            ),
            _get_pod(),
        )
        token = _get_token(spec, logger)
        for agent_id in agents:
            _deregister_agent(
                pod,
                agent_id,
                _make_headers(token),
                logger,
            )
    except Exception as err:
        raise kopf.PermanentError(f'Error while trying to delete agents: {err}.')


@kopf.on.resume(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND)  # type: ignore
def relaunch_agents(spec, status, name, logger, patch, **kwargs):
    try:
        pod = _get_pod()
        otf_agents = _get_agents_uuids(
            AGENTS_URL_TMPL.format(pod=pod),
            _make_headers(_get_token(spec, logger)),
            logger,
        )

        kube_agents = status.get('create_agents', {}).get('agents')
        if kube_agents is None:
            logger.debug('No agents found for this resource, will create some.')
            return create_agents(spec, name, logger)  # type: ignore
        if len(kube_agents) > len(otf_agents):
            # TODO : add poolSize verification
            to_create = len(kube_agents) - len(otf_agents)
            logger.debug(f'Recreating {to_create} agents.')
            agents = _register_agents_return_uuids(to_create, name, spec, logger)
            new_agents = list(set(kube_agents).intersection(set(otf_agents))) + agents
            patch.status['create_agents'] = {'agents': new_agents}
        # TODO: if len(otf_agents) > len(kube_agents) ??? Do we need to handle it?
    except Exception as err:
        raise kopf.PermanentError(f'Error while trying to resume agents: {err}')


@kopf.on.field(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND, field='spec.poolSize')  # type: ignore
def update_pool_size(diff, spec, status, name, logger, patch, **kwargs):
    try:
        action, _, current_pool, new_pool = diff[0]
        if action == 'change' and (current_pool != new_pool):
            pod = _get_pod()
            current_agents = status.get('create_agents', {}).get('agents', [])
            if current_pool < new_pool:
                add = new_pool - current_pool
                patch.status['create_agents'] = {
                    'agents': current_agents
                    + _register_agents_return_uuids(add, name, spec, logger)
                }
            elif current_pool > new_pool:
                morituri = random.sample(current_agents, k=current_pool - new_pool)
                headers = _make_headers(_get_token(spec, logger))
                for moriturus in morituri:
                    _deregister_agent(
                        pod,
                        moriturus,
                        headers,
                        logger,
                    )
                patch.status['create_agents'] = {
                    'agents': list(set(current_agents) - set(morituri))
                }
    except Exception as err:
        raise kopf.PermanentError(f'Error while updating pool size: {err}')


@kopf.on.field(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND, field='spec.tags')  # type: ignore
def update_tags(diff, spec, status, name, logger, patch, **kwargs):
    try:
        action, _, old_tags, new_tags = diff[0]
        if action == 'change' and (old_tags != new_tags):
            pod = _get_pod()
            if old_agents := status.get('create_agents', {}).get('agents'):
                headers = _make_headers(_get_token(spec, logger))
                for agent_id in old_agents:
                    _deregister_agent(
                        pod,
                        agent_id,
                        headers,
                        logger,
                    )
            new_agents = _register_agents_return_uuids(
                spec.get('poolSize', 0), name, spec, logger
            )
            patch.spec['tags'] = new_tags
            patch.status['create_agents'] = {'agents': new_agents}
    except Exception as err:
        raise kopf.PermanentError(f'Error while updating agents tags: {err}')


########################################################################
### Little daemons

AGENTS_COMMANDS = Queue()
AGENTS_POLLING_DELAY = 5
AGENTS_WITH_POD = set()

PENDING_AGENTS_LOCK = threading.Lock()


def _maybe_get_agent_command(
    agent_id: str, spec: Dict[str, Any], logger
) -> Optional[Dict[str, Any]]:
    pod, headers = _get_pod(), _make_headers(_get_token(spec, logger))
    url = AGENT_ID_URL_TMPL.format(agent_id=agent_id, pod=pod)

    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    if response.status_code == 204:
        return None
    if response.status_code == 200 and 'details' in response.json():
        return response.json()['details']
    raise NotFound(f'Agent {agent_id} not found or .details not in response.')


def _get_pod_template(pod_name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    template = _make_copy(
        _get_param_or_fail(
            spec, ['template'], 'Failed to get pod template from pools definition'
        )
    )
    template['api_version'] = 'v1'
    template['kind'] = 'Pod'
    template.setdefault('metadata', {})['name'] = pod_name
    return template


def _create_exec_pod(pod_name: str, spec: Dict[str, Any], api_instance, logger):
    """Create a pod for an agent. Raise exception if creation fails."""
    pod_template = _get_pod_template(pod_name, spec)
    existing_pods = api_instance.list_namespaced_pod(namespace='default')

    if existing_pods and pod_name in [pod.metadata.name for pod in existing_pods.items]:
        logger.debug(f'Pod `{pod_name}` already exists, will not create new one.')
        return

    try:
        api_instance.create_namespaced_pod(namespace='default', body=pod_template)
        logger.info(f'Pod `{pod_name}` created.')
    except Exception as err:
        raise PodError(f'Failed to create pod: {str(err)}') from err


def _delete_exec_pod(pod_name: str, api_instance, logger):
    """Delete a pod related to an inactive agent. Raise exception if fail."""
    try:
        api_instance.delete_namespaced_pod(name=pod_name, namespace='default')
        logger.info(f'Pod `{pod_name}` deleted.')
    except Exception as err:
        logger.error(f'Cannot delete pod: {str(err)}')


def _is_pod_running(pod_name: str, api_instance: client.CoreV1Api) -> bool:
    timeout = time.time() + POD_TIMEOUT
    while time.time() <= timeout:
        pod_status = api_instance.read_namespaced_pod_status(
            pod_name, namespace='default'
        )
        if pod_status.status.phase == 'Running':  # type: ignore
            return True
        time.sleep(1)
    return False


def _read_pod_response(pod_response) -> Tuple[str, str, int]:
    stdout, stderr = '', ''
    while pod_response.is_open():
        pod_response.update(timeout=1)
        if pod_response.peek_stdout():
            stdout += pod_response.read_stdout()
        if pod_response.peek_stderr():
            stderr += pod_response.read_stderr()
    return_code = pod_response.returncode
    pod_response.close()
    return stdout, stderr, return_code


def _upload_file_to_pod(
    agent_url: str,
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    command: Dict[str, Any],
    api_instance,
):
    cmd = ['/bin/sh', '-c', f'cat > {command["path"]}']
    pod_response = stream.stream(
        api_instance.connect_get_namespaced_pod_exec,
        pod_name,
        'default',
        command=cmd,
        stderr=True,
        stdin=True,
        stdout=True,
        tty=False,
        _preload_content=False,
    )
    response = requests.get(
        agent_url, stream=True, headers=headers, timeout=REQUEST_TIMEOUT
    )
    if response.status_code != 200:
        raise Exception(
            f'Failed to get filestream from orchestrator, error code: {response.status_code}.'
        )
    for chunk in response.iter_content(chunk_size=128):
        if not chunk:
            continue
        pod_response.write_stdin(chunk.decode('utf-8'))
    pod_response.close()


def _execute_cmd_on_pod(
    instruction: str, pod_name: str, api_instance: client.CoreV1Api
) -> Tuple[str, str, int]:
    cmd = ['/bin/sh', '-c', instruction]
    pod_response = stream.stream(
        api_instance.connect_get_namespaced_pod_exec,
        pod_name,
        'default',
        command=cmd,
        stderr=True,
        stdin=True,
        stdout=True,
        tty=False,
        _preload_content=False,
    )
    return _read_pod_response(pod_response)


def _process_put_cmd(
    agent_url: str,
    command: Dict[str, Any],
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    api_instance: client.CoreV1Api,
    logger,
):
    """Download file from orchestrator to the agent pod."""
    if 'path' not in command:
        logger.error('No path specified in command.')
    if 'file_id' not in command:
        logger.error('No file_id specified in command.')
    url = FILE_URL_TMPL.format(agent_url=agent_url, file_id=command['file_id'])
    try:
        # TODO: what to do with working_dir / script_path ?
        if _is_pod_running(pod_name, api_instance):
            _upload_file_to_pod(url, headers, pod_name, command, api_instance)
        else:
            raise TimeoutError('Timed out, pod still not running')
    except Exception as err:
        result = requests.post(
            url,
            json={
                'details': {
                    'error': f'Failed to download file {command["file_id"]} to {command["path"]}: {err}'
                }
            },
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        logger.error(f'An error occurred while downloading file: {err}.')
        if result.status_code != 200:
            logger.debug(
                f'Failed to notify the orchestrator. Got a {result.status_code} status code.'
            )


def _process_exec_cmd(
    agent_url: str,
    command: Dict[str, Any],
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    api_instance,
    logger,
):
    """Execute the execute command on a pod."""
    try:
        instruction = command['command']
        if _is_pod_running(pod_name, api_instance):
            stdout, stderr, return_code = _execute_cmd_on_pod(
                instruction, pod_name, api_instance
            )
        else:
            raise TimeoutError('Timed out, pod still not running')
        sent = False
        while not sent:
            try:
                result = requests.post(
                    agent_url,
                    json={
                        'stdout': stdout.splitlines(),
                        'stderr': stderr.splitlines(),
                        'exit_status': return_code,
                    },
                    headers=headers,
                    timeout=REQUEST_TIMEOUT,
                )
                sent = True
                if result.status_code != 200:
                    logger.error(
                        f'Failed to push command result. Response code {result.status_code}.'
                    )
            except Exception as err:
                logger.error(f'Failed to push command result: {str(err)}, retrying.')
    except Exception as err:
        logger.error(f'Failed to execute command: {str(err)}.')


def _process_get_cmd(
    agent_url: str,
    command: Dict[str, Any],
    headers: Optional[Dict[str, Any]],
    pod_name: str,
    api_instance,
    logger,
):
    """Upload file from the pod to the orchestrator."""
    if 'path' not in command:
        logger.error('No path specified in command.')
        return
    if 'file_id' not in command:
        logger.error('No file_id specified in command.')
        return
    url = FILE_URL_TMPL.format(agent_url=agent_url, file_id=command['file_id'])
    try:
        if _is_pod_running(pod_name, api_instance):
            file_base64, stderr, return_code = _execute_cmd_on_pod(
                f'base64 {command["path"]}', pod_name, api_instance
            )
            if return_code != 0:
                raise PodError(stderr)
            file_binary = base64.b64decode(file_base64)
            requests.post(
                url, data=file_binary, headers=headers, timeout=REQUEST_TIMEOUT
            )
        else:
            raise TimeoutError('Timed out, pod still not running.')
    except Exception as err:
        file_path = command['path']
        result = requests.post(
            agent_url,
            json={'details': {'error': f'Failed to fetch file {file_path}: {err}.'}},
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        if result.status_code != 200:
            logger.error(
                f'Failed to push command result. Status code: {result.status_code}'
            )


KIND_HANDLERS = {
    'put': _process_put_cmd,
    'exec': _process_exec_cmd,
    'get': _process_get_cmd,
}


def _kill_orphan_agent(
    pod: str,
    agent_id: str,
    headers: Optional[Dict[str, Any]],
    name: str,
    spec: Dict[str, Any],
    status: Dict[str, Any],
    logger,
):
    logger.debug('De-registering orphan agent, creating new agent instead.')
    with PENDING_AGENTS_LOCK:
        _deregister_agent(pod, agent_id, headers, logger)
        new_agent = _register_agents_return_uuids(1, name, spec, logger)
        agents_patch = [
            item for item in status['create_agents']['agents'] if item != agent_id
        ] + new_agent
        custom_object_api = client.CustomObjectsApi()
        custom_object_api.patch_namespaced_custom_object(
            group=POOLS_API_GROUP,
            version=POOLS_API_VERSION,
            namespace='default',
            plural=POOLS_KIND,
            name=name,
            body={'status': {'create_agents': {'agents': agents_patch}}},
        )
        logger.debug(
            f'Agent {agent_id} de-registered, agent {new_agent[0]} created, status patched.'
        )


def _remove_agent_and_pod(agent_id: str, pod_name: str, api_instance, logger):
    try:
        AGENTS_WITH_POD.remove(agent_id)
    except KeyError:
        pass
    _delete_exec_pod(pod_name, api_instance, logger)


@kopf.daemon(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND, initial_delay=5, cancellation_backoff=1.0)  # type: ignore
def handle_agent_command(stopped, name, spec, status, logger, **kwargs):
    """Agent commands handling daemon.

    Waits for a command, creates an execution environment if required and processes
    a command. When channel release command (-2.sh) is received, deletes the execution
    environment.
    """
    logger.info('Starting agent commands handling daemon...')
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    while not stopped:
        pod, headers = _get_pod(), _make_headers(_get_token(spec, logger))
        try:
            agent_id, command = AGENTS_COMMANDS.get(timeout=1)
            pod_name = f"{spec.get('template', {}).get('metadata', {}).get('name', name)}-{agent_id}"
            url = AGENT_ID_URL_TMPL.format(agent_id=agent_id, pod=pod)
            if command['kind'] == 'exec' and ('-2.sh' in command['command']):
                _process_exec_cmd(url, command, headers, pod_name, api_instance, logger)
                time.sleep(0.5)
                if not _maybe_get_agent_command(agent_id, spec, logger):
                    _remove_agent_and_pod(agent_id, pod_name, api_instance, logger)
                    continue
            if agent_id not in AGENTS_WITH_POD:
                try:
                    _create_exec_pod(pod_name, spec, api_instance, logger)
                except PodError as err:
                    logger.error(str(err))
                    _kill_orphan_agent(
                        pod, agent_id, headers, name, spec, status, logger
                    )
                    continue
                AGENTS_WITH_POD.add(agent_id)
            KIND_HANDLERS[command['kind']](
                url, command, headers, pod_name, api_instance, logger
            )
        except Empty:
            continue
        except Exception as err:
            logger.error(f'Error while handling commands: {str(err)}.')
    logger.info('Stopping agent commands handling daemon...')


@kopf.daemon(POOLS_API_GROUP, POOLS_API_VERSION, POOLS_KIND, initial_delay=5, cancellation_backoff=1.0)  # type: ignore
def monitor_agents(stopped, name, spec, logger, **kwargs):
    """Agents monitoring daemon.

    Reads agents list from pools status, then loops over it to get a command.
    """
    logger.info('Starting agents monitoring daemon...')

    def get_live_status():
        config.load_kube_config()
        custom_object_api = client.CustomObjectsApi()
        try:
            obj = custom_object_api.get_namespaced_custom_object(
                group=POOLS_API_GROUP,
                version=POOLS_API_VERSION,
                namespace='default',
                plural=POOLS_KIND,
                name=name,
            )
            return obj.get('status', {}).get('create_agents', {}).get('agents', [])  # type: ignore
        except Exception as err:
            logger.error(f'Error fetching live status: {err}.')
            return []

    while not stopped:
        try:
            live_agents = get_live_status()
            if not live_agents:
                logger.debug('No agents found for resource. Will retry.')
                time.sleep(AGENTS_POLLING_DELAY)
                continue
            with PENDING_AGENTS_LOCK:
                for agent in live_agents:
                    try:
                        command = _maybe_get_agent_command(agent, spec, logger)
                    except NotFound as err:
                        logger.error(str(err))
                        continue
                    if not command:
                        continue
                    AGENTS_COMMANDS.put((agent, command))
            time.sleep(AGENTS_POLLING_DELAY)
        except Exception as err:
            logger.error(f'Error while monitoring agents: {str(err)}')
    logger.info('Stopping agents monitoring daemon...')
