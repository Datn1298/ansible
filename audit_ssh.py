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
        output[i].append({
                "name": "PermitRootLogin",
                "value": array_to_string(list_permitroot['^PermitRootLogin'][i]),
                "violate_policy": handle_status_str(array_to_string(list_permitroot['^PermitRootLogin'][i]), "no")
            })

        output[i].append({
                "name": "Port SSH",
                "value": array_to_string(list_port_ssh['^Port'][i]),
                "violate_policy": handle_status_str(array_to_string(list_port_ssh['^Port'][i]), "1309")
                
            })
        output[i].append({ 
                "name": "PubkeyAuthentication",
                "value": array_to_string(list_pubkey_authen['^PubkeyAuthentication'][i]),
                "violate_policy": handle_status_str(array_to_string(list_pubkey_authen['^PubkeyAuthentication'][i]), "no")     
            })

        output[i].append({
                "name": "Hosts allow",
                "value": array_to_string(list_host_allow['host_allow'][i]),
                "violate_policy": ""     
            })

        output[i].append({
                "name": "Hosts deny",
                "value": array_to_string(list_host_deny['host_deny'][i]),
                "violate_policy": ""
            })     
        list.append({"ip": ip[i], "task": name_task, "output": output[i],"status": status[i], "error": error[i], "date": time[i]})

    return {"output": list}

