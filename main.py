import cv2
from cvzone.HandTrackingModule import HandDetector

#furthure readings https://github.com/cvzone/cvzone/blob/master/cvzone/HandTrackingModule.py


capture = cv2.VideoCapture(0)
capture.set(3,1280)
capture.set(4,720)
#giving the confidence and the hand count
detector_hand = HandDetector(detectionCon=0.7)
initialDistance = None
image_scale = 0
cx,cy = 300,500

while True:
    #scucess is true img is the video image
    success,img = capture.read()
    # print(success)
    #hand is a the array of points
    hands,img = detector_hand.findHands(img)
    image1 = cv2.imread('gamer.jpg')
    if (len(hands) == 2):

        # print("Both hands on screen!!!")
        # plan ur gesture which you want to use i use the thumb and index finger
        # hand[0] == right hand & hand[1] == left hand
        print(detector_hand.fingersUp(hands[1]) , detector_hand.fingersUp(hands[0]))
        if(detector_hand.fingersUp(hands[1])==[1,1,0,0,0] and detector_hand.fingersUp(hands[0])==[1,1,0,0,0]):
            # print("correct action of hand")
            #now lets find the distance from the hand
            lmList0 = hands[0]['lmList']
            lmList1 = hands[1]['lmList']

            #get the length using tip of finger

            if (initialDistance == None):

                length, info, img = detector_hand.findDistance(lmList0[8], lmList1[8], img)
                # print(length)
                initialDistance = length
            length, info, img = detector_hand.findDistance(lmList0[8], lmList1[8], img)

            # decrese the sensitivity by making a int
            image_scale = int((length - initialDistance) // 2)
            # print(image_scale)

            #find the center point of the distance
            #which is loacted in info -> findDistance

            cx,cy = info[4:]




    else:
        #we make the distance to 0 when hands are taken away from screen
        initialDistance = None

    try:
        #store the image in a variable
        image1 = cv2.imread('gamer.jpg')
        #get the height and width of the given image 250*250
        h1,w1,_=image1.shape

        new_height, new_width = ((h1+image_scale)//2)*2, ((w1+image_scale) //2)*2

        image1 =cv2.resize(image1, (new_width,new_height))

        #slizing the image and overlaying it shit a image by 10 should increase both the same value
        #keep the image in the center of the width
        #cx == height
        img[cy-new_height//2:cy+new_height//2, cx-new_width//2:cx+new_width//2] = image1
        cv2.imshow("image",img)
        key = cv2.waitKey(1)
        if (key == ord('c')):
            break

    except:
        pass

