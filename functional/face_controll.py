import os, json, base64
from deepface import DeepFace
from functional import accaunts


#
# img2 ='/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/database/jake2.jpg'
img1 = os.path.abspath('faces/..jpg')
# print(img1)
#
pin = 22109199100358
# print(img1, os.path.abspath(f'database/{pin}.jpg'))


def photo_identificate(img, pin):
    # try:
        req = accaunts.requests.get(f'http://10.2.10.82:8000/check-photo/{pin}/') #
        a = req.json()['image']
        print(a)
        image_64_decode = base64.b64decode(a)
        image_result = open(f'database/{pin}.jpg', 'wb')
        image_result.write(image_64_decode)
        if image_result:
            photos = DeepFace.verify(img1_path=img, img2_path=os.path.abspath(f'database/{pin}.jpg'))
            with open('faces/result.json', 'w') as file:
                json.dump(photos, file, indent=4, ensure_ascii=False)
            if photos.get('verified'):
                return True
            else:
                return False
        else:
            return False
    # except Exception:
    #     return False
    # loc = os.path.abspath(f'../database/')
    # os.remove(os.path.join(loc, f'{pin}.jpg'))
    # print('succes')
    # http://10.2.10.82:8000/check-photo/22109199100358/

# photo_identificate(img1, pin)


# def photo_identificate(img1):
#     photos = DeepFace.verify(img1_path=img1, img2_path=img2)
#     with open('/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/result.json', 'w') as file:
#         json.dump(photos, file, indent=4, ensure_ascii=False)
#     if photos.get('verified'):
#         print('Dostup otkryt')
#         return True
#     else:
#         print('error')
#         return False


# photo_identificate(img1='/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/eda.jpg', img2='/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/jake2.jpg')



# import face_recognition
# from PIL import Image # Библиотека для работы с изображениями
#
# find_face = face_recognition.load_image_file("face/sergey.jpg") # Загружаем изображение нужного человека
# face_encoding = face_recognition.face_encodings(find_face)[0] # Кодируем уникальные черты лица, для того чтобы сравнивать с другими
#
# i = 0 # Счётчик общего выполнения
# done = 0 # Счётчик совпадений
# numFiles = 8330 # Тут указываем кол-во фото
# while i != numFiles:
#     i += 1 # Увеличиваем счётчик общего выполнения
#     unknown_picture = face_recognition.load_image_file(f"img/{i}.jpg") # Загружаем скачанное изображение
#     unknown_face_encoding = face_recognition.face_encodings(unknown_picture) # Кодируем уникальные черты лица
#
#     pil_image = Image.fromarray(unknown_picture) # Записываем изображение в переменную
#
#     # Проверяем нашла ли нейросеть лицо
#     if len(unknown_face_encoding) > 0: # Если нашли лицо
#         encoding = unknown_face_encoding[0] # Обращаемся к 0 элементу, чтобы сравнить
#         results = face_recognition.compare_faces([face_encoding], encoding) # Сравниваем лица
#
#         if results[0] == True: # Если нашли сходство
#             done += 1 # Увеличиваем счётчик общего выполнения
#             print(i,"-","Нашли нужного человека !")
#             pil_image.save(f"done/{int(done)}.jpg") # Сохраняем фото с найденным человеком
#         else: # Если не нашли сходство
#             print(i,"-","Не нашли нужного человека!")
#     else: # Если не нашли лицо
#         print(i,"-","Лицо не найдено!")


# import face_recognition
#
# def compare_faces(img1_path, img2_path):
#     img1 = face_recognition.load_image_file(img1_path)
#     img1_encodings = face_recognition.face_encodings(img1)[0]
#     # print(img1_encodings)
#
#     img2 = face_recognition.load_image_file(img2_path)
#     img2_encodings = face_recognition.face_encodings(img2)[0]
#
#     result = face_recognition.compare_faces([img1_encodings], img2_encodings)
#     # print(result)
#
#     if result[0]:
#         print("Welcome to the club! :*")
#     else:
#         print("Sorry, not today... Next!")




