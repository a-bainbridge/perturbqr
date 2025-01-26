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
            print("█", end="")
        else:
            print(" ", end="")
    print()

version = int((len(straight_qrcode[0][0]) - 17) / 4)
print(version)

error_correction_lvl = 

