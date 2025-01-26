# # pip install pyzbar

# from pyzbar.pyzbar import decode
# from PIL import Image
# print(decode(Image.open('wiki.png')))

# pip install opencv-python

import cv2
print(cv2.__version__)
img = cv2.imread('wiki.png')

qcd = cv2.QRCodeDetector()

retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

print(retval)
print(decoded_info)
print(points)
print(straight_qrcode)

for i in straight_qrcode[0]:
    for j in i:
        if j == 0:
            print(" ", end="")
        else:
            print("█", end="")
    print()

version = int((len(straight_qrcode[0][0]) - 17) / 4)
print(version)

error_lvl_dict = {(255,255): "H", (255,0): "Q", (0,255): "M", (0,0): "L"}
error_correction_lvl = error_lvl_dict[(straight_qrcode[0][8][0], straight_qrcode[0][8][1])]
print(error_correction_lvl)

# mask types from https://en.wikipedia.org/wiki/QR_code#/media/File:QR_Format_Information.svg

mask_type = ''
for i in straight_qrcode[0][8][2:5]:
    if i == 255:
        mask_type += str(1)
    else:
        mask_type += str(0)

print(mask_type)



