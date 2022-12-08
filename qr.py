import cv2


def read_qr_code(filename):
    """Read an image and read the QR code.

    Args:
        filename (string): Path to file

    Returns:
        qr (string): Value from QR code
    """

    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return 'Ошибка при считывании QR-кода'


# print(read_qr_code('/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/id.jpg'))

# import hashlib
# import qrcode


# def create_qr_code(data):
#     """
#     Create a QR code from a string.
#     """
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
#
#     img = qr.make_image(fill_color="black", back_color="white")
#     filename = hashlib.md5(data.encode()).hexdigest() + ".jpg"
#     img.save(filename)
#
#     return filename
#
# create_qr_code('7')

# 9085472057e4348f5a0e2680b914c8ed.png