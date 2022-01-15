import cv2
import sys
import face_recognition
import os
from tkinter.filedialog import *
def blur_img(post, pro_pic):
    imagePath = post
    pro = pro_pic
    # print(pro)
    pro = cv2.imread(pro)
    image = cv2.imread(imagePath) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    # print("[INFO] Found {0} Faces!".format(len(faces)))
    images = os.listdir(os.path.join(os.getcwd(),'core','data'))
    for i in images:
        os.remove(os.path.join(os.getcwd(),'core','data',i))

    cv2.imwrite(os.path.join(os.getcwd(),'core','data','1.jpg'),pro)
    m=0
    im=os.listdir(os.path.join(os.getcwd(),'core','face'))
    for i in im:
        os.remove(os.path.join(os.getcwd(),'core','face',i))


    for (x, y, w, h) in faces:
        m=m+1
        
        name=str(m)+'.jpg'
        path=os.path.join(os.path.join(os.getcwd(),'core','face'),name)
        # print(path)
        # cv2.imshow('faces',image[y:y+h,x:x+w])
        # cv2.waitKey(1000)
        cv2.imwrite(path,image[y:y+h,x:x+w])
        # cv2.imwrite(images[0],image[y:y+h,x:x+w])
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 6)
        
        image_to_be_matched = face_recognition.load_image_file(path)
        try:
            img_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
        except IndexError:
            continue
        for face in images:
    ##        print(face)
            
            # load the image
            current_image = face_recognition.load_image_file(os.path.join(os.getcwd(),'core','data',face))
            # encode the loaded image into a feature vector
            current_image_encoded = face_recognition.face_encodings(current_image)[0]
            # match your image with the image and check if it matches
            result = face_recognition.compare_faces(
                [img_encoded], current_image_encoded)

            if result ==[True]:
                print('+++++++++++++++++Found this',face)

        
                aaa=image[y:y+h,x:x+w]
                blurImg = cv2.blur(aaa,(70,70))
                blurImg = cv2.blur(blurImg,(70,70))
                image[y:y+h,x:x+w]=blurImg
                # cv2.imshow('image',cv2.resize(image,(256,256)))
                # cv2.waitKey(4000)
                


    # cv2.imshow('image',cv2.resize(image,(256,256)))
    # cv2.waitKey(1000)
    cv2.imwrite(imagePath,image)



def check_img(post, pro_pic):
    imagePath = post
    pro = pro_pic
    # print(pro)
    pro = cv2.imread(pro)
    image = cv2.imread(imagePath) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    # print("[INFO] Found {0} Faces!".format(len(faces)))
    images = os.listdir(os.path.join(os.getcwd(),'core','data'))
    for i in images:
        os.remove(os.path.join(os.getcwd(),'core','data',i))

    cv2.imwrite(os.path.join(os.getcwd(),'core','data','1.jpg'),pro)
    m=0
    im=os.listdir(os.path.join(os.getcwd(),'core','face'))
    for i in im:
        os.remove(os.path.join(os.getcwd(),'core','face',i))


    for (x, y, w, h) in faces:
        m=m+1
        
        name=str(m)+'.jpg'
        path=os.path.join(os.path.join(os.getcwd(),'core','face'),name)
        # print(path)
        # cv2.imshow('faces',image[y:y+h,x:x+w])
        # cv2.waitKey(1000)
        cv2.imwrite(path,image[y:y+h,x:x+w])
        # cv2.imwrite(images[0],image[y:y+h,x:x+w])
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 6)
        
        image_to_be_matched = face_recognition.load_image_file(path)
        try:
            img_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
        except IndexError:
            continue
        for face in images:
    ##        print(face)
            
            # load the image
            current_image = face_recognition.load_image_file(os.path.join(os.getcwd(),'core','data',face))
            # encode the loaded image into a feature vector
            current_image_encoded = face_recognition.face_encodings(current_image)[0]
            # match your image with the image and check if it matches
            result = face_recognition.compare_faces(
                [img_encoded], current_image_encoded)

            if result ==[True]:
                return pro_pic