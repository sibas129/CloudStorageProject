import qrcode
from io import BytesIO
from PIL import Image


def generate_qr(url: str) -> BytesIO:
    logo = Image.open("src/logo.png")
    basewidth = 50
    wpercent = basewidth / float(logo.size[0])
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize))
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr.add_data(url)
    qr.make()
    QRimg = qr.make_image(fill_color=(163, 212, 247), back_color=(255, 255, 255))
    pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    img_byte_io = BytesIO()
    QRimg.save(img_byte_io)
    img_byte_io.seek(0)
    return img_byte_io
