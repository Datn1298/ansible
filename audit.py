from run_ansible import *
from file import *




# fix sau
"""
Kiểm tra monitor:
- Kiểm tra xem zabbix-agent đã cài đặt chưa
- Kết quả: True/
"""
# def audit_monitor(inventory):
#   task=[
#     dict(action=dict(module='package_facts', args=dict(manager='auto'))),
#     dict(action=dict(module='debug', args=dict(msg='True')),when='\'zabbix-agent2\' in ansible_facts.packages'),
#   ]
#   name_task="Audit Monitor"
#   ip, status, result, error, date = run_ansible(task, "audit", inventory)
#   return { "ip": ip, "task": name_task, "status": status, "result": result, "error": error, "date": date,}




# def audit_change_permission(inventory):
#   task=[
#     dict(action=dict(module='shell', args='chmod 600 /etc/ssh/sshd_config')),
#     dict(action=dict(module='shell', args='chown root:root /etc/ssh/sshd_config')),
#   ]
#   result = run_ansible(task, "audit", inventory)
#   print(result)

def audit_user(inventory):
    task = [
        dict(action=dict(module='shell',
             args='getent passwd | grep -wv "nologin" | awk -F: \'$3 > 999\' | awk -F: \'$3 < 60000 {print $1}\''))
    ]
    name_task = "Danh sách User đã tạo"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)
    print("============================" , ip)
    list = []

    change_permission_file("/home/datnt/test/test.txt", "0777", "")
    for i in range(len(ip)):
        temp = []
        for j in range(len(output[i])):
            list_group = audit_group_of_user(output[i][j], inventory)
            group = list_group[0].split()
            password_expire = audit_password_expire(output[i][j], inventory)
            last_password_change = audit_last_password_change(
                output[i][j], inventory)
            temp.append({"user": output[i][j], "group": group,
                        "Password expire": password_expire, "Last password change": last_password_change})
        list.append({"ip": ip[i], "output": temp, "task": name_task,
                    "status": status[i], "error": error[i], "date": time[i]})
    return {"output": list}


def audit_group_of_user(user, inventory):
    args = "id -nG " + user
    task = [
        dict(action=dict(module='shell', args=args))
    ]
    output = run_ansible(task, "get_output", inventory)
    return output


def audit_password_expire(user, inventory):
    args = "chage -l " + user + \
        " | grep \"Password expires.*\" | awk -F : '{print $2}'"
    task = [
        dict(action=dict(module='shell', args=args))
    ]
    output = run_ansible(task, "get_output", inventory)
    return output


def audit_last_password_change(user, inventory):
    args = "chage -l " + user + \
        " | grep \"Last password change.*\" | awk -F : '{print $2}'"
    task = [
        dict(action=dict(module='shell', args=args))
    ]
    output = run_ansible(task, "get_output", inventory)
    return output


def audit_user_uid(inventory):
    task = [
        dict(action=dict(module='shell',
             args='getent passwd | grep -wv "root" | awk -F: \'$3 < 1 {print $0}\''))
    ]
    name_task = "Danh sách User có UID=0"
    ip, status, result, error, date = run_ansible(task, "audit", inventory)
    return {"ip": ip, "task": name_task, "status": status, "result": result, "error": error, "date": date, }

def check_install(inventory, package):
    args = f"dpkg -l | grep {package}" + " | awk '{print $1}'"
    task_status = [dict(action=dict(module='shell', args=args))]
    output = run_ansible(task_status, "get_list_output", inventory)
    return {"status": output}

def audit_list_package(inventory):

    task_status = [dict(action=dict(module='shell', args='dpkg -l | grep "^ii" | awk \'{print $1}\''))]
    task_name = [dict(action=dict(module='shell', args='dpkg -l | grep "^ii" | awk \'{print $2}\''))]
    task_version = [dict(action=dict(module='shell', args='dpkg -l | grep "^ii" | awk \'{print $3}\''))]
    task_description = [dict(action=dict(module='shell', args='dpkg -l | grep "^ii" | awk \'{print $5}\''))]
    status = run_ansible(task_status, "get_list_output", inventory)
    name = run_ansible(task_name, "get_list_output", inventory)
    version = run_ansible(task_version, "get_list_output", inventory)
    description = run_ansible(task_description, "get_list_output", inventory)

    list = []
    output = []
    for i in range(len(status)):
        for j in range(len(status[i])):
            print(name[i][j])
            output.append({ \
                "Status": status[i][j],
                "Name": name[i][j],
                "Version": version[i][j],
                "Description": description[i][j],
            })
        list.append(output)

    return {"status": list}


def audit_datetime(inventory):
    args = "date '+%Y/%m/%d %H:%M:%S'"
    task = [dict(action=dict(module='shell', args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"Datetime": output}
   
    

def audit_port(inventory, port):
    args = f"netstat -alntp | grep {port}" 
    task = [dict(action=dict(module='shell', args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {f"Port {port}": output}

def audit_group(inventory):
    task = [
        dict(action=dict(module='shell',
             args='getent group | awk -F: \'$3 > 1000\' | awk -F: \'$3 < 60000 {print $1}\''))
    ]
    name_task = "Danh sách Group"
    ip, status, result, error, date = run_ansible(task, "audit", inventory)
    return {"ip": ip, "task": name_task, "status": status, "result": result, "error": error, "date": date, }

def audit_port_open(inventory):
    name_task = "Danh sách Open Port"
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
        result = []
        for j in range(len(list_port)):
            result.append(
                {"Port": list_port[j], "PID": list_pid[j], "Program name": list_service[j]})
        output[i] = result
        list.append({"Port Open": output[i]})
    return {"output": list}

def audit_network_connection(inventory):
    name_task = "Danh sách Network Connection"
    task = [dict(action=dict(module='shell', args='true'))]
    task_create_temp=[dict(action=dict(module='file', args=dict(path='/opt/temp', state='touch')))]
    task_save=[dict(action=dict(module='shell', args='netstat -tpanl > /opt/temp'))]
    task_delete_file=[dict(action=dict(module='file', args=dict(path='/opt/temp', state='absent')))]
    task_list_port = [dict(action=dict(module='shell', args='cat /opt/temp | grep "LISTEN" | grep -wv "tcp6" | awk \'{print $4}\' | awk -F : \'{print $2}\''))]
    task_list_state = [dict(action=dict(module='shell', args='cat /opt/temp | grep "LISTEN" | grep -wv "tcp6" | awk \'{print $6}\''))]
    task_list_pid = [dict(action=dict(module='shell', args='cat /opt/temp | grep "LISTEN" | grep -wv "tcp6" | awk \'{print $7}\' | awk -F / \'{print $1}\''))]
    task_list_service = [dict(action=dict(module='shell', args='cat /opt/temp | grep "LISTEN" | grep -wv "tcp6" | awk \'{print $7}\' | awk -F / \'{print $2}\''))]
    ip, status, error, output, time = run_ansible(task, "audit", inventory)
    run_ansible(task_create_temp, "shell", inventory)
    run_ansible(task_save, "shell", inventory)
    list_port = run_ansible(task_list_port, "get_output", inventory)
    list_pid = run_ansible(task_list_pid, "get_output", inventory)
    list_state = run_ansible(task_list_state, "get_output", inventory)
    list_service = run_ansible(task_list_service, "get_output", inventory)
    run_ansible(task_delete_file, "shell", inventory)
    list = []
    for i in range(len(ip)):
        result = []
        for j in range(len(list_port)):
            result.append(
                {"Port": list_port[j], "PID": list_pid[j], "Program name": list_service[j], "State": list_state[j]})
        output[i] = result
        list.append({"Network Connect": output[i]})
    return {"output": list}

def audit_crontab(inventory):
    task = [
        dict(action=dict(module='shell', args='crontab -l | grep -wv "^#.*"' ))
    ]
    output = run_ansible(task, "get_list_output", inventory)
    return {"Crontab": output}

def audit_service(inventory):
    task = [
        dict(action=dict(module='shell',
             args='systemctl --type=service | grep active | grep running'))
    ]
    name_task = "Audit Service"
    ip, status, result, error, date = run_ansible(task, "audit", inventory)
    return {"ip": ip, "task": name_task, "status": status, "result": result, "error": error, "date": date, }

def audit_general_info(inventory):
    task = [
        dict(action=dict(module='shell', args='true'))
    ]
    name_task = "Lấy thông tin chung của server"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)

    list_pass_min_days = audit_pass_min_days(inventory)
    list_pass_max_days = audit_pass_max_days(inventory)
    list_pass_min_len = audit_pass_min_len(inventory)
    list_pass_warn_age = audit_pass_warn_age(inventory)
    list_port_ssh = audit_port_ssh(inventory)
    list_permitroot = audit_permitroot(inventory)

    list = []

    for i in range(len(ip)):
        result = []
        result.append({
            "PASS_MIN_DAYS": list_pass_min_days[i][0],
            "PASS_MAX_DAYS": list_pass_max_days[i][0],
            "PASS_MIN_LEN": list_pass_min_len[i],
            "PASS_WARM_AGE": list_pass_warn_age[i][0],
            "Port SSH": list_port_ssh[i],
            "PermitRootLogin": list_permitroot[i],
        })
        output[i] = result

        list.append({"ip": ip[i], "task": name_task, "output": output[i],
                    "status": status[i], "error": error[i], "date": time[i]})

    return {"output": list}

def audit_pass_max_days(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/login.defs | grep "^PASS_MAX_DAYS.*" | awk \'{print $2}\''))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"PASS_MAX_DAY": output}

def get_string(inventory, file, str):
    args = f"cat {file} | grep {str}" + "| awk '{print $2}'"
    task = [dict(action=dict(module='shell',args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {str: output}


def audit_os(inventory):
    task = [
        dict(action=dict(module='shell', args='true'))
    ]
    name_task = "Lấy thông tin chung của server"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)

    list_datetime=audit_datetime(inventory)
    # list_pass_max_days=get_string(inventory, "/etc/login.defs", "^PASS_MAX_DAYS.*")
    # list_pass_min_days=get_string(inventory, "/etc/login.defs", "^PASS_MIN_DAYS.*")
    # list_pass_min_len=get_string(inventory, "/etc/login.defs", "^PASS_MIN_LEN.*")
    # list_pass_warn_age=get_string(inventory, "/etc/login.defs", "^PASS_WARM_AGE.*")

    # list_permitroot=get_string(inventory, "/etc/ssh/sshd_config", "^PermitRootLogin")
    # list_port_ssh=get_string(inventory, "/etc/ssh/sshd_config", "^Port")
    # list_pubkey_authen=get_string(inventory, "/etc/ssh/sshd_config", "^PubkeyAuthentication")
    # list_host_allow=audit_host_allow(inventory)
    # list_host_deny=audit_host_deny(inventory)

    # port_open=audit_port_open(inventory)
    # network_connection=audit_network_connection(inventory)
    # list_check_install_sudo=check_install(inventory, "sudo")
    # list_check_install_filebeat=check_install(inventory, "filebeat")
    # list_check_install_zabbix_agent=check_install(inventory, "zabbix-agent")
    # list_check_port_5044=audit_port(inventory, "5044")
    # list_check_port_10050=audit_port(inventory, "10050")

    # list_package=audit_list_package(inventory)


    # name_file = ["/etc/passwd", "/etc/group", "/etc/shadow", "/etc/fstab"]
    # file_permission = ["-rw-r--r--"," -rw-r--r--", "----------", "-rw-r--r--"]
    # for i in range(name_file):
    #     name

    #     f"check{name_file[i]}" = audit_permission_file(name_file[i], inventory, file_permission[i])

    # print(check/etc/passwd)
    # list_check_file_etc_passwd=audit_permission_file("/etc/passwd", inventory,  "-rw-r--r--")
    # list_check_file_etc_passwd=audit_permission_file("/etc/passwd", inventory,  "-rw-r--r--")
    # list_check_file_etc_passwd=audit_permission_file("/etc/passwd", inventory,  "-rw-r--r--")
    # list_check_file_etc_passwd=audit_permission_file("/etc/passwd", inventory,  "-rw-r--r--")


    list = []

    for i in range(len(ip)):
        # output[i].append({
        #     "Audit Datetime": {
        #         "Datetime": array_to_string(list_datetime['Datetime'][i])
        #         }})
        output[i].append({"Datetime": array_to_string(list_datetime['Datetime'][i])})
        # if (array_to_string((list_check_install_filebeat['status'][i]))) == 'ii' :
        #     output[i].append({ \
        #         "Package Firebeat": handle_status(array_to_string((list_check_install_filebeat['status'][i]))),
        #         "Port 5044": handle_status(array_to_string((list_check_port_5044['status'][i]))),
        #         })
        # else: 
        #     output[i].append({"Package Firebeat": handle_status(array_to_string((list_check_install_filebeat['status'][i])))})
        # if (array_to_string((list_check_install_zabbix_agent['status'][i]))) == 'ii' :
        #     output[i].append({ \
        #         "Zabbix-agent": handle_status(array_to_string((list_check_install_zabbix_agent['status'][i]))),
        #         "Port 10050": handle_status(array_to_string((list_check_port_10050['status'][i]))),
        #         })
        # else: 
        #     output[i].append({"Zabbix-agent": handle_status(array_to_string((list_check_install_zabbix_agent['status'][i])))})

        # handle_output = handle_permission("/etc/passwd", list_check_file_etc_passwd['permission_file'][i][0], "-rw-r--r--")


        # output[i].append(audit_crontab(inventory))



        # output[i].append({ \
        #     "Port Open": port_open['output'][i]['Port Open'], 
        #     "Network Connect": network_connection['output'][i]['Network Connect']
        #     })

        # output[i].append({"Package Sudo": handle_status(array_to_string((list_check_install_sudo['status'][i])))})
        
        list.append({"ip": ip[i], "task": name_task, "output": output[i],
                    "status": status[i], "error": error[i], "date": time[i]})

    return {"output": list_package}


def array_to_string(list):
    return (' '.join([str(elem) for elem in list]))

def handle_status(str):
    status = ""
    if(str=='ii'):
        status="Đã cài đặt thành công"
    elif(str!=''):
        status="Cài bị lỗi"
    else:
        status="Chưa cài đặt"
    return status

