#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, with_statement
from asyncio import tasks
from atexit import register
import json
import shutil
from datetime import datetime

from ansible import context
import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from pyparsing import line

__metaclass__ = type


# Create a callback plugin so we can capture the output
class ResultsCollectorJSONCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        host = result._host
        self.host_ok[host.get_name()] = result
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


def run_ansible(_task, _type, _inventory):
    # host_list = ["test"]
    # since the API is constructed for CLI it expects certain options to always be set in the context object
    context.CLIARGS = ImmutableDict(
        connection="smart",
        module_path=["/to/mymodules", "/usr/share/ansible"],
        forks=10,
        become=True,
        become_method="sudo",
        become_user="root",
        check=False,
        diff=False,
        verbosity=0,
    )

    # initialize needed objects
    loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
    passwords = dict(vault_pass="secret")

    # Instantiate our ResultsCollectorJSONCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
    results_callback = ResultsCollectorJSONCallback()

    # create inventory, use path to host config file as source or hosts in a comma separated string
    inventory = InventoryManager(loader=loader, sources="inventory")

    # get time
    now = datetime.now()
    time = now.strftime("%Y/%m/%d %H:%M:%S")

    # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=passwords,
        # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
        stdout_callback=results_callback,
    )

    # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
    play_source = dict(
        name="Ansible Play", hosts='all', gather_facts="no", tasks=_task
    )

    # Create play object, playbook objects use .load instead of init or new methods,
    # this will also automatically create the task objects from the info provided in play_source
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # Actually run it
    try:
        result = tqm.run(
            play
        )  # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    if (_type == "audit"):
        ip, status, error, output, times = [], [], [], [], []
        for host, result in results_callback.host_ok.items():
            ip.append(host)
            status.append('success')
            output.append(result._result['stdout_lines'])
            error.append(result._result['stderr'])
            times.append(time)
        for host, result in results_callback.host_failed.items():
            ip.append(host)
            status.append('fail')
            output.append(result._result['msg'])
            error.append(result._result['msg'])
            times.append(time)
        for host, result in results_callback.host_unreachable.items():
            ip.append(host)
            status.append('unreachable')
            output.append(result._result['msg'])
            error.append(result._result['msg'])
            times.append(time)
        return ip, status, error, output, times
    elif (_type == "user"):
        for host, result in results_callback.host_ok.items():
            ip = host
            output = ''
            status = 'success'
            error = ''
        for host, result in results_callback.host_failed.items():
            ip = host
            status = 'fail'
            output = result._result['msg']
            error = result._result['msg']
        for host, result in results_callback.host_unreachable.items():
            ip = host
            status = 'unreachable'
            output = result._result['msg']
            error = result._result['msg']
        return ip, status, output, error, time
    elif (_type == "install"):
        for host, result in results_callback.host_ok.items():
            ip = host
            status = 'success'
            output = result._result['changed']
            error = ''
        return ip, status, output, error, time
    elif (_type == "config"):
        for host, result in results_callback.host_ok.items():
            ip = host
            status = 'success'
            output = result._result['changed']
            error = ''
        return ip, status, output, error, time
    elif (_type == "get_output"):
        output = ""
        for host, result in results_callback.host_ok.items():
            output = result._result['stdout_lines']
        return output
    elif (_type == "get_list_output"):
        output = []
        for host, result in results_callback.host_ok.items():
            output.append(result._result['stdout_lines'])
            if(result._result['stdout_lines'] == ""):
                output.append("")
        return output
    elif (_type == "shell"):
        for host, result in results_callback.host_ok.items():
            print()
    
