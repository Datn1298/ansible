from run_ansible import *

def audit_port(inventory, port):
    args = f"netstat -alntp | grep {port}" 
    task = [dict(action=dict(module='shell', args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {f"Port {port}": output}

def audit_port_open(inventory):
    name_task = "Audit Port Open"
    task = [dict(action=dict(module='shell', args='true'))]
    task_create_temp=[dict(action=dict(module='file', args=dict(path='/opt/temp', state='touch')))]
    task_save=[dict(action=dict(module='shell', args='netstat -tpunl > /opt/temp'))]
    task_delete_file=[dict(action=dict(module='file', args=dict(path='/opt/temp', state='absent')))]
    task_list_port = [dict(action=dict(module='shell', args='cat /opt/temp | grep "LISTEN" | grep -wv "tcp6" | awk \'{print $4}\' | awk -F : \'{print $2}\''))]
    task_list_pid = [dict(action=dict(module='shell', args='cat /opt/temp | grep "LISTEN" | grep -wv "tcp6" | awk \'{print $7}\' | awk -F / \'{print $1}\''))]
    task_list_service = [dict(action=dict(module='shell', args='cat /opt/temp | grep "LISTEN" | grep -wv "tcp6" | awk \'{print $7}\' | awk -F / \'{print $2}\''))]
    ip, status, error, output, time = run_ansible(task, "audit", inventory)
    run_ansible(task_create_temp, "shell", inventory)
    run_ansible(task_save, "shell", inventory)
    list_port = run_ansible(task_list_port, "get_output", inventory)
    list_pid = run_ansible(task_list_pid, "get_output", inventory)
    list_service = run_ansible(task_list_service, "get_output", inventory)
    run_ansible(task_delete_file, "shell", inventory)

    list = []
    for i in range(len(ip)):
        result = [{"Port": list_port[j], "PID": list_pid[j], "Program name": list_service[j], "violate_policy": "true"} for j in range(len(list_port))]

        output[i] = result
        list.append({"ip": ip[i], "task": name_task, "output": output[i],
                    "status": status[i], "error": error[i], "date": time[i]})
    return {"output": list}




