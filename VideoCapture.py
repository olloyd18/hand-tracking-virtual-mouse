import cv2 as cv #opencv is a library used letting python interact with the cameraa 
import mediapipe as mp #this is a library that detects things in images 
import pyautogui


#these lines are shorthand
#mp is a whole library and inside that library is a folder called solutions which stores each of the detectors so we call mp. (then) solutions (then) 'detector'#

# so calling this shorthand is just making it quicker to call the mediapipe hand tracking module (the folder that contains everything to do with hand tracking)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cam = cv.VideoCapture(0) #vc is a class #0 means use the default camera, 1 is for pluggins and so on

frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

print("width ",cv.CAP_PROP_FRAME_WIDTH, frame_width)
print("height ",cv.CAP_PROP_FRAME_HEIGHT, frame_height)

#print(pyautogui.size()) this lines tells us the size of our window could make this variable so it works on other devices but fgor now it is 1920w and 1200l

# in theory we need a robot that can look through photos and spot a hand in them. To do that you need to make the robot
# hand_detecting_robot = mp_hands.Hands() creates a robot that can do this but each robot has its own setting thats when you make the parameters
#mp hands is the hands module .Hands() is a class in that module so 
hand_detecting_robot = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) 

def findDistance(x1,y1,x2,y2):
    #here just use euclidian distance 
    xsqr = (x1-x2)*(x1-x2)
    ysqr = (y1-y2)*(y1-y2)
    xny = xsqr + ysqr 
    final = xny ** 0.5 
    return final 


while True:
    ret, frame = cam.read() #.read returns a boolean confirming if we could get a frame, frame is the image in array form
    rgbframe = cv.cvtColor(frame, cv.COLOR_BGR2RGB)# convert the color of the frame to format for mp's requiremnetns 

    result = hand_detecting_robot.process(rgbframe) #the robot takes the frame and actually processes a report it has info of if handlandmarks were found and where & etc

    if result.multi_hand_landmarks: #in report we have a box that has a list of hand (objects), each object stores the x,y of landmarks, in the if its treated as T/F
        for hand_landmarks in result.multi_hand_landmarks: #loops over every hand, handldmks represents the current hands list of landmarks 
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) #draw landmarks knows how to draw one hand but its needs a frame, and landmark pos

    cv.imshow("camera", frame) #open a window and show this image 
    cv.waitKey(1) #0 means wait forever until a key is pressed #1 gives it 1 milisecond to refresh the window and do all its processing, it also checks for keypresses

    if result.multi_hand_landmarks:
        hand1 = result.multi_hand_landmarks[0] #
        pointer = hand1.landmark[8]
        thumb = hand1.landmark[4]
        print("x co-ordinate: ", pointer.x, "   y co-ordinate: ", pointer.y, "   thumb x:", thumb.x, "thumb y:", thumb.y) #these give normalised co ordinates

        #we need to unnormalise them first and make them match the actual screen
        pyautogui.moveTo(((1-pointer.x)*1920), (pointer.y*1200))

    if result.multi_hand_landmarks:
        hand1 = result.multi_hand_landmarks[0]
        pointer = hand1.landmark[8]
        thumb = hand1.landmark[4]

        euc = findDistance(pointer.x,pointer.y,thumb.x,thumb.y)

        if euc < 0.04:
            pyautogui.click((1-pointer.x)*1920,pointer.y*1200)



    if cv.waitKey(1) == ord('q') or cv.waitKey(1) == ord('Q'): 
        break
    #“Call waitKey(1) right now. If the number it returns equals the number for the letter ‘q’, then break.” 

'''
def leftclick(x,y):

    if distance between index and thumb is < some number:
        
        pyautogui.click(position of the thumb ,y)'''
    




