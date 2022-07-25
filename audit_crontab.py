from run_ansible import *
def audit_crontab(inventory):
    task = [dict(action=dict(module='shell', args='true'))]
    name_task = "Lấy thông tin chung của server"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)
    task_crontab = [dict(action=dict(module='shell', args='crontab -l | grep -wv "^#.*"' ))]
    crontab = run_ansible(task_crontab, "get_list_output", inventory) 
    print(crontab)
    # list=[]
    # for i in range(len(ip)):
    #     output[i].append({"Crontab": {
    #         "value": crontab[i],
    #         "status_check" : ""
    #     }})
    #     list.append({"ip": ip[i], "task": name_task, "output": output[i], "status": status[i], "error": error[i], "date": time[i]})

    return {"output": "list"}