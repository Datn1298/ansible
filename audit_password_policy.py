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
        add_result(output, list_pass_max_days, list_pass_min_days, list_pass_min_len, list_pass_warn_age, i)
        list.append({"ip": ip[i], "task": name_task, "output": output[i],"status": status[i], "error": error[i], "date": time[i]})
    return {"output": list}

def add_result(output, list_pass_max_days, list_pass_min_days, list_pass_min_len, list_pass_warn_age, i):
    output[i].append({ \
                "name": "PASS_MAX_DAYS",
                "value": handle_status_str(array_to_string(list_pass_max_days['^PASS_MAX_DAYS.*'][i]), "90")["value"],
                "violate_policy": handle_status_str(array_to_string(list_pass_max_days['^PASS_MAX_DAYS.*'][i]), "90")["status"]
            })
    output[i].append({
                "name": "PASS_MIN_DAYS",
                "value": handle_status_str(array_to_string(list_pass_min_days['^PASS_MIN_DAYS.*'][i]), "6")["value"],
                "violate_policy": handle_status_str(array_to_string(list_pass_min_days['^PASS_MIN_DAYS.*'][i]), "6")["status"]
            })
    output[i].append({
                "name": "PASS_MIN_LEN",
                "value": handle_status_str(array_to_string(list_pass_min_len['^PASS_MIN_LEN.*'][i]), "14")["value"],
                "violate_policy": handle_status_str(array_to_string(list_pass_min_len['^PASS_MIN_LEN.*'][i]), "14")["status"]
            })
    output[i].append({
                "name": "PASS_WARN_AGE",
                "value": handle_status_str(array_to_string(list_pass_warn_age['^PASS_WARM_AGE.*'][i]), "7")["value"],
                "violate_policy": handle_status_str(array_to_string(list_pass_warn_age['^PASS_WARM_AGE.*'][i]), "7")["status"]
            })
