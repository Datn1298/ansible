from run_ansible import *



def audit_service(inventory):
    task = [dict(action=dict(module='shell', args='true'))]
    name_task = "Audit Service"
    task_get_service = [dict(action=dict(module='shell', args='systemctl --all list-unit-files --type=service |  awk \'{print $1 ":" $3}\' | grep enabled'))]
    list_service = run_ansible(task_get_service, "get_list_output", inventory)
    ip, status, error, output, time = run_ansible(task, "audit", inventory)
    print(list_service)

    # list = []

    # for i in range(len(ip)):

    return {"output": "list"}