from deepface import DeepFace
import json

img2 ='/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/jake2.jpg'
img1 = '/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/faces/'


def photo_identificate(img1):
    photos = DeepFace.verify(img1_path=img1, img2_path=img2)
    with open('/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/result.json', 'w') as file:
        json.dump(photos, file, indent=4, ensure_ascii=False)
    if photos.get('verified'):
        print('Dostup otkryt')
        return True
    else:
        print('error')
        return False


# photo_identificate(img1='/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/eda.jpg', img2='/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/jake2.jpg')
