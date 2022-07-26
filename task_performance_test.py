
from run_ansible import *

"""
- pt = performance test
Task:
- copy file tu source den dich
- run file
- nen zip
"""


"""
Copy file .jmt vào 6 hosts: master + 5 slave
- Đầu vào: path file inventory, địa chỉ file cần chuyền, đích cần đến
"""
def pt_copy_file(inventory, source, dest):
    task_copy_file = [
        dict(action=dict(module="copy", args=dict(src=source, dest=dest)))
    ]
    run_ansible(task_copy_file, "shell", inventory)


"""
Chạy file .jmt tại máy chủ master
- Đầu vào: path file inventory, đường dẫn đến file .jmt (dest của pt_copy_file())
"""
def pt_run_file(inventory, source):
    args = f"./{source}"
    task_run_file = [
        dict(action=dict(module="shell", args=args))
    ]
    run_ansible(task_run_file, "shell", inventory)

"""
Nén file kết quả vừa chạy file .jmt
- Đầu vào: path file inventory, đường dẫn đến file kết quả
"""
def pt_run_file(inventory, source):
    dest = f"{source}.zip"
    task_zip_result = [
        dict(action=dict(module="archive", args=dict(source=source, dest=dest, format='zip')))
    ]
    run_ansible(task_zip_result, "shell", inventory)
