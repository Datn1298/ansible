from run_ansible import *
from handle_output import *

def get_string(inventory, file, str):
    args = f"cat {file} | grep {str}" + "| awk '{print $2}'"
    task = [dict(action=dict(module='shell',args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {str: output}


def audit_password_policy(inventory):
    task = [dict(action=dict(module='shell', args='true'))]
    name_task = "Audit Password Policy"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)

    list_pass_max_days=get_string(inventory, "/etc/login.defs", "^PASS_MAX_DAYS.*")
    list_pass_min_days=get_string(inventory, "/etc/login.defs", "^PASS_MIN_DAYS.*")
    list_pass_min_len=get_string(inventory, "/etc/login.defs", "^PASS_MIN_LEN.*")
    list_pass_warn_age=get_string(inventory, "/etc/login.defs", "^PASS_WARM_AGE.*")

    list = []

    for i in range(len(ip)):
        output[i].append({ \
            "PASS_MAX_DAYS": {
                "value": array_to_string(list_pass_max_days['^PASS_MAX_DAYS.*'][i]),
                "status_check": ""
            },
            "PASS_MIN_DAYS": {
                "value": array_to_string(list_pass_min_days['^PASS_MIN_DAYS.*'][i]),
                "status_check": ""
            },
            "PASS_MIN_LEN": {
                "value": array_to_string(list_pass_min_len['^PASS_MIN_LEN.*'][i]),
                "status_check": ""
            },
            "PASS_WARN_AGE": {
                "value": array_to_string(list_pass_warn_age['^PASS_WARM_AGE.*'][i]),
                "status_check": ""
            }
        })
        list.append({"ip": ip[i], "task": name_task, "output": output[i],"status": status[i], "error": error[i], "date": time[i]})
    return {"output": list}
