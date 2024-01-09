import json
import shutil
import time

import ansible.constants as C
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase

from ansible.vars.manager import VariableManager
from ansible import context

# Create a callback plugin so we can capture the output
class ResultsCollectorJSONCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in.

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin.
    """

    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        task = result._task
        self.host_unreachable[f"{host.get_name()} -> {task.get_name()}"] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        task = result._task
        # print(dir(host))
        # print(dir(task))
        # print(host.get_vars())
        self.host_ok[f"{host.get_name()} -> {task.get_name()}"] = result
        #print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        task = result._task
        self.host_failed[f"{host.get_name()} -> {task.get_name()}"] = result


def main(hosts):
    # 判断主机是否为列表，可以多台机器执行命令
    if isinstance(hosts,list):
        host_list = hosts
    else:
        host_list = [hosts]
    # since the API is constructed for CLI it expects certain options to always be set in the context object
    context.CLIARGS = ImmutableDict(connection='smart',
                                    syntax=None,start_at_task=None,
                                    module_path=['/data/work/pydev/venv_ansible/lib/python3.10/site-packages/ansible',
                                                 '/usr/share/ansible',
                                                 '/data/work/pydev/ansible_ex'],
                                    forks=10, become=True,
                                    ssh_args='-C -o ControlMaster=auto -o ControlPersist=600s -o ConnectTimeout=300 -o ServerAliveInterval=30 -o ServerAliveCountMax=10',
                                    timeout=10, #ssh connect timeout,
                                    extra_vars={"ping_ip=127.0.0.1"},
                                    become_method='sudo', become_user="root", check=False, diff=False, verbosity=3)
    # required for
    # https://github.com/ansible/ansible/blob/devel/lib/ansible/inventory/manager.py#L204
    sources = ','.join(host_list)
    if len(host_list) == 1:
        sources += ','

    # initialize needed objects
    loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files

    # create inventory, use path to host config file as source or hosts in a comma separated string
    inventory = InventoryManager(loader=loader, sources=sources)

    # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    results_callback = ResultsCollectorJSONCallback()
    playbook = PlaybookExecutor(playbooks=['/data/work/pydev/ansible_ex/demo.yml'],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,passwords=dict())
    callback = results_callback
    playbook._tqm._stdout_callback = callback
    playbook.run()
    data = {"up": None, "failed": None, "down": None}
    # print("UP ***********")
    for host, result in results_callback.host_ok.items():
        # data["up"] = '{0} >>> {1}'.format(host, result._result['stdout'])
        print('{0} >>> {1}'.format(host, result._result))

    # print("FAILED *******")
    for host, result in results_callback.host_failed.items():
        # data["up"] = '{0} >>> {1}'.format(host, result._result['msg'])
        print('{0} >>> {1}'.format(host, result._result))

    # print("DOWN *********")
    for host, result in results_callback.host_unreachable.items():
        # data["down"] = '{0} >>> {1}'.format(host, result._result['msg'])
        print('{0} >>> {1}'.format(host, result._result))

    return data

if __name__ == '__main__':
    start= time.time()
    run_shell = main("120.133.83.145")
    print(f"time:{time.time()-start}")
