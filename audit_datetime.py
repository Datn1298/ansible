from run_ansible import *
from handle_output import *
from datetime import datetime

def audit_datetime(inventory):
    task = [dict(action=dict(module='shell', args='true'))]
    name_task = "Audit Datetime"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)

    args = "date '+%Y/%m/%d %H:%M:%S'"
    args_sec = "date '+ %s'"
    task_get_datetime = [dict(action=dict(module='shell', args=args))]
    task_get_timestamp = [dict(action=dict(module='shell', args=args_sec))]
    list_datetime = run_ansible(task_get_datetime, "get_list_output", inventory)
    list_timestamp = run_ansible(task_get_timestamp, "get_list_output", inventory)

    list = []
    status_audit = []

    timestamp = datetime.timestamp(datetime.now())

    for i in range(len(ip)):
        if (timestamp-float(array_to_string(list_timestamp[i]))+i < 10):
            status_audit.append("true")
        else:
            status_audit.append("false")

    for i in range(len(ip)):
        output[i].append({"Datetime": {
            "value": array_to_string(list_datetime[i]),
            "status": status_audit[i]
        }})
        
        list.append({"ip": ip[i], "task": name_task, "output": output[i], "status": status[i], "error": error[i], "date": time[i]})

    return {"output": list}

