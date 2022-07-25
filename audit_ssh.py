from run_ansible import *
from handle_output import *

def get_string(inventory, file, str):
    args = f"cat {file} | grep {str}" + "| awk '{print $2}'"
    task = [dict(action=dict(module='shell',args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {str: output}

def audit_host_allow(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/hosts.allow | grep -wv "^#"'))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"host_allow": output}

def audit_host_deny(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/hosts.allow | grep -wv "^#"'))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"host_deny": output}


def audit_ssh(inventory):
    task = [dict(action=dict(module='shell', args='true'))]
    name_task = "Audit SSH"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)

    list_permitroot=get_string(inventory, "/etc/ssh/sshd_config", "^PermitRootLogin")
    list_port_ssh=get_string(inventory, "/etc/ssh/sshd_config", "^Port")
    list_pubkey_authen=get_string(inventory, "/etc/ssh/sshd_config", "^PubkeyAuthentication")
    list_host_allow=audit_host_allow(inventory)
    list_host_deny=audit_host_deny(inventory)

    list = []

    for i in range(len(ip)):
        output[i].append({ \
            "PermitRootLogin": {
                "value": array_to_string(list_permitroot['^PermitRootLogin'][i]),
                "status_check": handle_status_str(array_to_string(list_permitroot['^PermitRootLogin'][i]), "no")
            },
            "Port SSH": {
                "value": array_to_string(list_port_ssh['^Port'][i]),
                "status_check": handle_status_str(array_to_string(list_port_ssh['^Port'][i]), "1309")
                
            },
            "PubkeyAuthentication": {
                "value": array_to_string(list_pubkey_authen['^PubkeyAuthentication'][i]),
                "status_check": handle_status_str(array_to_string(list_pubkey_authen['^PubkeyAuthentication'][i]), "no")     
            },
            "Hosts allow": {
                "value": array_to_string(list_host_allow['host_allow'][i]),
                "status_check": ""     
            },
            "Hosts deny": {
                "value": array_to_string(list_host_deny['host_deny'][i]),
                "status_check": ""     
            }    
            })     
        list.append({"ip": ip[i], "task": name_task, "output": output[i],"status": status[i], "error": error[i], "date": time[i]})

    return {"output": list}

