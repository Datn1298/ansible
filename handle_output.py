def array_to_string(list):
    return (' '.join([str(elem) for elem in list]))

def handle_status_install(str):
    if str == '':
        return "Chưa cài đặt"
    elif str == 'ii':
        return "Đã cài đặt thành công"
    else:
        return "Cài bị lỗi"

def handle_status_str(str_input, eo):
    status = ""
    if eo == "":
        status =  "None"
    elif str_input == "":
        str_input = "Default"
        status = "false"
    elif str_input == eo:
        status = "true"
    else: 
        status = "false"
    return {"value": str_input, "status":status}
