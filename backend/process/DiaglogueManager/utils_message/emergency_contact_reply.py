import regex as re
from unidecode import unidecode

from backend.config.constant import DISTRICT


def emergency_contact_rep(text, last_infor):
    #----------------------------------------------#
    # Kịch bản:
    # - Khi khách hàng request liên lạc với các trung tâm y tế, ...
    # - Nếu đầu vào câu khách nhắn hỏi liên lạc trạm y tế hay trạm y tế lưu động nhưng chưa biết địa chỉ của bệnh nhân
    #     => hỏi bệnh nhân ở quận nào
    #     - Nếu bệnh nhân báo quận thì gửi hình ảnh các số liên lạc cho bệnh nhân
    # - Nếu đầu vào có đủ các thông tin, ví dụ "em ở quận X thì liên hệ trạm y tế nào vậy ạ"
    #     => gửi hình ảnh sđt cho bệnh nhân
    # - Nếu câu hỏi mang tính chung chung
    #     => gửi danh sách các cách thức liên hệ với bệnh nhân + request thêm bệnh nhân muốn hỏi cụ thể chỗ nào.
    #----------------------------------------------#

    print('\t\t------------------TƯ VẤN LIÊN HỆ HỖ TRỢ-------------------')
    res = {}
    if last_infor['infor']['address']:
        res_code = 'inform_contact+' + last_infor['infor']['address']
    else:
        res_code = 'request_location_contact'
    res[res_code] = last_infor
    return res