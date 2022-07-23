from run_ansible import *


def user_delete(username):
    task = [
        dict(
            action=dict(
                module="user", args=dict(name=username, state="absent", remove="yes")
            )
        )
    ]
    name_task = "Delete user"
    ip, status, result = run_ansible(task, "user")
    return {"ip": ip, "task": name_task, "status": status, "result": result}


def user_create(username, password):
    task = [
        dict(action=dict(module="user", args=dict(name=username, password=password)))
    ]
    name_task = "Create user"
    ip, status, output, error, time = run_ansible(task, "user")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def user_edit_permission(username):
    task = [dict(action=dict(module="user", args=dict(name=username, groups="sudo")))]
    name_task = "Edit permission user"
    ip, status, output, error, time = run_ansible(task, "user")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }


def file_edit_permission(file, mode):
    task = [dict(action=dict(module="file", args=dict(name=file, mode=mode)))]
    name_task = "Edit permission user"
    ip, status, output, error, time = run_ansible(task, "user")
    return {
        "ip": ip,
        "task": name_task,
        "status": status,
        "result": output,
        "error": error,
        "date": time,
    }
