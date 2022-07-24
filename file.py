from run_ansible import *


# Đổi quyền cho File
def file_edit_permission(file, mode, inventory):
	task=[dict(action=dict(module='file', args=dict(name=file, mode=mode)))]
	name_task="Edit permission user"
	ip, status, output, error, time = run_ansible(task, "user", inventory)
	return { "ip": ip, "task": name_task, "status": status, "result": output, "error": error, "date": time} 

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
    permission.append({ 
        f"{str[0]}": first, 
        "User": user, 
        "Group": group, 
        "Other": other, 
        "Status": status})
    return {f"{_file}": permission}

def audit_permission_file(_file, inventory, expected):
    args = f"ls -la {_file} | awk " + "'{print $1}'"
    task=[
        dict(action=dict(module='shell', args=args))
    ]
    output = run_ansible(task, "get_list_output", "")
    return {"permission_file": output}

def change_permission_file(_file, _mode, inventory):
    task=[dict(action=dict(module='file', args=dict(path=_file, mode=_mode)))]
    run_ansible(task, "shell", "")