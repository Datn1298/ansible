from run_ansible import *
from handle_output import *

def check_install(inventory, package):
    args = f"dpkg -l | grep {package}" + " | awk '{print $1}'"
    task_status = [dict(action=dict(module='shell', args=args))]
    output = run_ansible(task_status, "get_list_output", inventory)
    return {"status": output}

def audit_port(inventory, port):
    args = f"netstat -alntp | grep {port}" 
    task = [dict(action=dict(module='shell', args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {f"Port {port}": output}    

def audit_monitor(inventory):
    task = [dict(action=dict(module='shell', args='true'))]
    name_task = "Audit Monitor"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)
    list_check_install_zabbix_agent=check_install(inventory, "zabbix-agent")
    list_check_port_10050=audit_port(inventory, "10050")
    list = []

    for i in range(len(ip)):
        if (array_to_string((list_check_install_zabbix_agent['status'][i]))) == 'ii' :
            output[i].append({
                    "name": "Zabbix-agent",
                    "value": handle_status_install(array_to_string((list_check_install_zabbix_agent['status'][i]))),
                    "violate_policy" : "true"
                },{
                    "name": "Port 10050",
                    "value": handle_status_install(array_to_string((list_check_port_10050['status'][i]))),
                    "violate_policy" : "true"
                })
        else: 
            output[i].append({
                    "name": "Zabbix-agent", 
                    "value": handle_status_install(array_to_string((list_check_install_zabbix_agent['status'][i]))),
                    "violate_policy" : "false"
                })
        list.append({"ip": ip[i], "task": name_task, "output": output[i],"status": status[i], "error": error[i], "date": time[i]})

    return {"output": list}