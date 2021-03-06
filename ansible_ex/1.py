# coding=utf-8

import json
import shutil
from collections import namedtuple, defaultdict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        # super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result
        print result.is_failed()
        # print result._task
        # cmd = result._task_fields["args"]["_raw_params"]
        # print result._task
        print (result._host, result._task, result._result.get("stdout_lines", ""))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.Options = namedtuple('Options',
                                  ['connection',
                                   'remote_user',
                                   'ask_sudo_pass',
                                   'verbosity',
                                   'ack_pass',
                                   'module_path',
                                   'forks',
                                   'become',
                                   'become_method',
                                   'become_user',
                                   'check',
                                   'listhosts',
                                   'listtasks',
                                   'listtags',
                                   'syntax',
                                   'sudo_user',
                                   'sudo',
                                   'diff'])

        self.ops = self.Options(connection='ssh',
                                remote_user='Administrator',  # ?????????????????????
                                ack_pass=None,
                                sudo_user=None,
                                forks=5,
                                sudo=None,
                                ask_sudo_pass=False,
                                verbosity=5,
                                module_path=None,
                                become=None,
                                become_method=None,
                                become_user="root",  # ???????????????????????????????????????= root???
                                check=False,
                                diff=False,
                                listhosts=None,
                                listtasks=None,
                                listtags=None,
                                syntax=None)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources='192.168.43.14,')
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        print dir(self.variable_manager)
        self.variable_manager._extra_vars = {"ansible_ssh_user":"Administrator" , "ansible_ssh_pass":"123.com"," ansible_connection":"winrm"}

    '''
    inventory --> ???ansible.inventory???????????????????????????inventory??????
    variable_manager --> ???ansible.vars?????????????????????????????????????????????
    loader --> ???ansible.parsing.dataloader?????????????????????????????????
    options --> ???????????????????????????????????????
    passwords --> ????????????????????????????????????
    stdout_callback --> ????????????
    
 
    '''

    def runansible(self, host_list, task_list):

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
                passwords={"conn_pass": "123.com", "become_pass": "root"},  # conn_pass ???????????????????????????
                stdout_callback=self.results_callback,  # ??????????????????
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                # run_additional_callbacks=False,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True) # ??????????????????
        # print(C.DEFAULT_LOAD_CALLBACK_PLUGINS, C.DEFAULT_LOCAL_TMP)
        results_raw = defaultdict(dict)
        # results_raw['success'] = {}
        # results_raw['failed'] = {}
        # results_raw['unreachable'] = {}

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result

        # for host, result in results_raw.iteritems(): todo ????????????????????????????????????????????????????????????
        #     # host = result._host
        #     print json.dumps(result, indent=4)

    # def playbookrun(self, playbook_path):
    #
    #     self.variable_manager.extra_vars = {"ansible_ssh_user":"root" , "ansible_ssh_pass":"123456"}
    #     playbook = PlaybookExecutor(playbooks=playbook_path,
    #                                 inventory=self.inventory,
    #                                 variable_manager=self.variable_manager,
    #                                 loader=self.loader, options=self.ops, passwords=self.passwords)
    #     result = playbook.run()
    #     return result


if __name__ == "__main__":
    a = AnsibleApi()
    host_list = "192.168.43.14"
    tasks_list = [
        dict(action=dict(module='command', args='ls')),
        dict(action=dict(module='command', args='w')),
        dict(action=dict(module='copy', args='src=/root/2.py dest=/root/2222dfsdf.py')),
        # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
    ]
    a.runansible(host_list, tasks_list)
    # a.playbookrun(playbook_path=['/etc/ansible/test.yml'])
