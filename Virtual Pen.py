import cv2
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(3, 640)
vid.set(4, 480)
vid.set(10, 150)

color = [[90, 128, 96, 109, 255, 255]]
myColorValues = [236, 245, 66]
myPoint = []
a,b,x1,y1,i = 0,0,0,0,0

def masking(colors, img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    point = []
    lower = np.array(colors[0][0:3])
    upper = np.array(colors[0][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    x, y = shapedec(mask)
    cv2.circle(imgResult, (x, y), 10, myColorValues, cv2.FILLED)
    if x!=0 and y!=0:
        point.append([x,y])
    return point


def shapedec(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h= 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        # print(peri)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        objCor = len(approx)
        x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

def drawOnScreen(mypoint):
    global a,b,i

    for point in mypoint:
        x1,y1=point[0],point[1]
        if x1==0 and y1==0:
            x1 , y1 = a,b
            i=0
        else:
            if i==0:
                a ,b = x1 ,y1
                i=i+1

        cv2.line(imgResult,(a,b), (x1, y1),  myColorValues,3)
        a, b = point[0], point[1]



while (True):

    # Capture the video frame
    # by frame

    success, frame = vid.read()
    if frame is None:
        break
    imgResult = frame.copy()
    newPoint = masking(color, frame)

    if len(newPoint)!=0:
        for newP in newPoint:
            myPoint.append(newP)
    else:
        newP = [0,0]
        myPoint.append(newP)
    if len(myPoint)!=0:
        drawOnScreen(myPoint)


    # Display the resulting frame
    cv2.imshow('frame', imgResult)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
