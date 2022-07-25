def array_to_string(list):
    return (' '.join([str(elem) for elem in list]))

def handle_status_install(str):
    status = ""
    if(str=='ii'):
        status="Đã cài đặt thành công"
    elif(str!=''):
        status="Cài bị lỗi"
    else:
        status="Chưa cài đặt"
    return status

def handle_status_str(str, eo):
    status = ""
    if eo == "":
        status = "None"
    elif str == eo:
        status = "True"
    else: 
        status = "False"
    return status
