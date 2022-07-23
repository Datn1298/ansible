from run_ansible import *


# Đổi quyền cho File
def file_edit_permission(file, mode, inventory):
	task=[
		dict(action=dict(module='file', args=dict(name=file, mode=mode)))
	]
	name_task="Edit permission user"
	ip, status, output, error, time = run_ansible(task, "user", inventory)
	return { "ip": ip, "task": name_task, "status": status, "result": output, "error": error, "date": time} 