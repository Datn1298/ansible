def array_to_string(list):
    return (' '.join([str(elem) for elem in list]))

def handle_status_install(str):
    if str == '':
        return "Chưa cài đặt"
    elif str == 'ii':
        return "Đã cài đặt thành công"
    else:
        return "Cài bị lỗi"

def handle_status_str(str, eo):
    if eo == "":
        return "None"
    elif str == eo:
        return "True"
    else: 
        return "False"
