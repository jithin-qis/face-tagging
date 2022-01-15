import cv2


def clickpic(img_name):
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Press space to capture")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            cv2.imwrite(img_name, frame)
            print(img_name)
            print("{} written!".format(img_name))
            img_counter += 1
            break

    cam.release()

    cv2.destroyAllWindows()
