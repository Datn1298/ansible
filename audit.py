from run_ansible import *

"""
Kiểm tra Datetime của OS
- Lấy ngày giờ hiện tại của OS
- Kết quả trả về: ngày giờ
"""

def audit_datetime(inventory):
    task = [
        dict(action=dict(module='shell', args='date'))
    ]
    name_task = "Audit Datetime"
    ip, status, result, error, date = run_ansible(task, "audit", inventory)
    return {"ip": ip, "task": name_task, "status": status, "result": result, "error": error, "date": date, }

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

"""
Kiểm tra monitor:
- Kiểm tra xem port 10050 đã được sử dụng chưa
- Kết quả: port 10050
"""

def audit_port10050(inventory):
    task = [
        dict(action=dict(module='shell', args='netstat -alntp | grep 10050'))
    ]
    name_task = "Audit Port 10050"
    ip, status, result, error, date = run_ansible(task, "audit", inventory)
    return {"ip": ip, "task": name_task, "status": status, "result": result, "error": error, "date": date, }



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

def audit_port(inventory, port):
    args = f"netstat -alntp | grep {port}" 
    task = [dict(action=dict(module='shell', args=args))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"Port 5044": output}

def audit_port5044(inventory):
    task = [dict(action=dict(module='shell', args='netstat -alntp | grep 5044'))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"Port 5044": output}

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

def audit_pass_min_days(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/login.defs | grep "^PASS_MIN_DAYS.*" | awk \'{print $2}\''))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"PASS_MIN_DAYS": output}

def audit_pass_min_len(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/login.defs | grep "^PASS_MIN_LEN.*" | awk \'{print $2}\''))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"PASS_MIN_LEN": output}

def audit_pass_warn_age(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/login.defs | grep "^PASS_WARN_AGE.*" | awk \'{print $2}\''))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"PASS_WARN_AGE": output}

def audit_permitroot(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/ssh/sshd_config | grep \'^PermitRootLogin.*\''))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"PermitRootLogin": output}

def audit_port_ssh(inventory):
    task = [dict(action=dict(module='shell',args='cat /etc/ssh/sshd_config | grep \'^Port.*\' | awk \'{print $2}\''))]
    output = run_ansible(task, "get_list_output", inventory)
    return {"Port SSH": output}

def change_permission_file(_file, _mode, inventory):
    task=[
        dict(action=dict(module='file', args=dict(path=_file, mode=_mode)))
    ]
    run_ansible(task, "shell", "")

def audit_permission_file(_file, inventory, expected):
    args = f"ls -la {_file} | awk " + "'{print $1}'"
    task=[
        dict(action=dict(module='shell', args=args))
    ]
    output = run_ansible(task, "get_list_output", "")
    print(output)
    object = handle_permission(_file, ''.join(output[0]), expected)
    print(output[1])
    return object

def handle_permission(_file, str, expected):
    switcher={
        '-': 'File',
        'd':'Director',
        'l':'Link',
    }
    first = switcher.get(str[0])
    user = str[1:4]
    group = str[4:7]
    other = str[7:10]
    permission = []
    if(str != expected):
        status = "Chưa config"
    else: 
        status = "Đã config"
    permission.append({f"{str[0]}": first, "User": user, "Group": group, "Other": other, "Status": status})
    return {f"{_file}": permission}

# def audit_permission(inventory):
#     task = [
#         dict(action=dict(module='shell', args='true'))
#     ]
#     name_task = "Lấy thông tin chung của server"
#     ip, status, error, output, time = run_ansible(task, "audit", inventory)

#     name_task = "Audit important files's permission"

#     permission_etc_group = "-rw-r--r--"
#     permission_etc_shadow = "-rw-r--r--"
#     permission_etc_passwd = "-rw-r--r--"
#     permission_etc_fstab = "-rw-r--r--"
#     output=[]
#     list = []

#     for i in range(len(ip)):
 
#         output[i] = result

#         list.append({"ip": ip[i], "task": name_task, "output": output[i],
#                     "status": status[i], "error": error[i], "date": time[i]})

#     return {"output": list}

#     output.append(audit_permission_file("/etc/group", inventory, permission_etc_group))
#     output.append(audit_permission_file("/etc/shadow", inventory, permission_etc_shadow))
#     output.append(audit_permission_file("/etc/passwd", inventory, permission_etc_passwd))
#     output.append(audit_permission_file("/etc/fstab", inventory, permission_etc_fstab))

#     return {name_task: output}

def audit_os(inventory):
    task = [
        dict(action=dict(module='shell', args='true'))
    ]
    name_task = "Lấy thông tin chung của server"
    ip, status, error, output, time = run_ansible(task, "audit", inventory)

    list_pass_max_days=audit_pass_max_days(inventory)
    list_pass_min_days=audit_pass_min_days(inventory)
    list_pass_min_len=audit_pass_min_len(inventory)
    list_pass_warn_age=audit_pass_warn_age(inventory)
    list_permitroot=audit_permitroot(inventory)
    list_port_ssh=audit_port_ssh(inventory)
    port_open=audit_port_open(inventory)
    network_connection=audit_network_connection(inventory)
    list_check_install_sudo=check_install(inventory, "sudo")
    list_check_install_filebeat=check_install(inventory, "filebeat")

    list = []

    for i in range(len(ip)):
        if (array_to_string((list_check_install_filebeat['status'][i]))) == 'ii' :
            output[i].append({ \
                "Package Firebeat": handle_status(array_to_string((list_check_install_filebeat['status'][i]))),

                })
        else: 
            output[i].append({"Package Firebeat": handle_status(array_to_string((list_check_install_filebeat['status'][i])))})
        output[i].append(audit_crontab(inventory))
        output[i].append({ \
            "PASS_MAX_DAY": array_to_string(list_pass_max_days['PASS_MAX_DAY'][i]),
            "PASS_MIN_DAYS": array_to_string(list_pass_min_days['PASS_MIN_DAYS'][i]),
            "PASS_MIN_LEN": array_to_string(list_pass_min_len['PASS_MIN_LEN'][i]),
            "PASS_WARN_AGE": array_to_string(list_pass_warn_age['PASS_WARN_AGE'][i])})
        # output[i].append({"PermitRootLogin": array_to_string(list_permitroot['PermitRootLogin'][i])})
        output[i].append({ \
            "Port SSH": array_to_string(list_port_ssh['Port SSH'][i]),
            "PermitRootLogin": "no"
            })
        output[i].append({ \
            "Port Open": port_open['output'][i]['Port Open'], 
            "Network Connect": network_connection['output'][i]['Network Connect']
            })

        # output[i].append({"Package Sudo": handle_status(array_to_string((list_check_install_sudo['status'][i])))})
        
        list.append({"ip": ip[i], "task": name_task, "output": output[i],
                    "status": status[i], "error": error[i], "date": time[i]})

    return {"output": list}


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

