from run_ansible import *
from file import *
from handle_output import * 
def get_string(inventory, file, str):
    args = f"cat {file} | grep {str}" + "| awk '{print $2}'"
    task = [dict(action=dict(module='shell',args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {str: output}


def audit_file(inventory):
    task = [
        dict(action=dict(module='shell', args='true'))
    ]
    name_task = "Audit Important File's Permission"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)

    list_check_file_etc_passwd=audit_permission_file("/etc/passwd", inventory,  "-rw-r--r--")
    list_check_file_etc_group=audit_permission_file("/etc/group", inventory,  "-rw-r--r--")
    list_check_file_etc_fstab=audit_permission_file("/etc/fstab", inventory,  "-rw-r--r--")
    list_check_file_etc_shadow=audit_permission_file("/etc/shadow", inventory,  "----------")

    list = []

    for i in range(len(ip)):
        output[i].append(handle_permission("/etc/passwd", array_to_string(list_check_file_etc_passwd['permission_file'][0]), "-rw-r--r--"))
        output[i].append(handle_permission("/etc/group", array_to_string(list_check_file_etc_group['permission_file'][0]), "-rw-r--r--"))
        output[i].append(handle_permission("/etc/fstab", array_to_string(list_check_file_etc_fstab['permission_file'][0]), "-rw-r--r--"))
        output[i].append(handle_permission("/etc/shadow", array_to_string(list_check_file_etc_shadow['permission_file'][0]), "----------"))

        list.append({"ip": ip[i], "task": name_task, "output": output[i],
                    "status": status[i], "error": error[i], "date": time[i]})

    return {"output": list}



