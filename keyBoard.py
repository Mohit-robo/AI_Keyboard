## Import Required Modules 
import cv2
import time
import cvzone
from handTrackingModule import handDetector
from pynput.keyboard import Controller
from playsound import playsound

## Declare Variables
cap = cv2.VideoCapture(0)
width = 1080
height = 720
hand_detect = handDetector(detectionCon=0.6)            ## Initialze the Hand Detector...
keys =  [["1","2","3","4","5","6","7","8","9","0",],    ## Making a list of all the keys that are to be used...   
         ["Q","W","E","R","T","Y","U","I","O","P"],
         ["A","S","D","F","G","H","J","K","L"],
         ["Z","X","C","V","B","N","M",",",".","/"]]
text = ""
keyboard = Controller()                                 ## Initialze the Keyboard Controller  
buttons = []

"""
Draw function:
    To draw the rectangle and keys on the screen
    x_button, y_button : Position of the Button
    width_button, height_button : Position of the Button
    cornerRect : Makes corners around the keys  
"""
def draw(frame,buttonList):
   
    for buttn in buttonList:
        x_button, y_button = buttn.position
        width_button, height_button = buttn.size
        cv2.rectangle(frame, buttn.position, (x_button + width_button - 30, y_button + height_button - 30), (120, 0, 120), cv2.FILLED)
        cv2.putText(frame, buttn.text, (x_button + 25, y_button + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cvzone.cornerRect(frame, (buttn.position[0], buttn.position[1], buttn.size[0] - 30, buttn.size[1] - 30), 20, rt=1)
    return frame

"""
Declare Positon, Text on the button and Size of the button 
"""
class Button():
    def __init__(self,position,text,size=[100,80]):
        self.position = position
        self.text = text
        self.size = size

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttons.append(Button([100 * j + 60, 100 * i + 60], key))

while True:
    _,frame = cap.read()
    frame = cv2.resize(frame,(width,height))                       ## Resize the Window

    ### Detecting Hands in the Frame .....

    frame = hand_detect.findHands(frame)
    landmark_list = hand_detect.findPosition(frame,draw=False)
    # print(landmark_list)
    frame = draw(frame, buttons)

    ## Setcting the Landmarks of Hand using the mediapipe Library

    if len(landmark_list) != 0 :
        landmark_x,landmark_y = landmark_list[8][1:]

    """
    If the landmarks are present change the button size and when clicked change the color
    """
    if landmark_list:
        for btn in buttons:
            x,y = btn.position
            w,h = btn.size
            if x < landmark_x < x+ w and y < landmark_y < y+h:
                cv2.rectangle(frame, btn.position, (x + w , y + h ), (175,0,175), cv2.FILLED)
                cv2.putText(frame, btn.text, (x + 20, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                length,_,_ = hand_detect.findDistance(8,12,frame)

                """
                length : get the length between the tip of middle and index fingre and when the length goes below 
                         the below mentioned values then the button is clicked
                """

                if length < 40:
                    keyboard.press(btn.text)
                    # playsound('typewriter-key-1.mp3')
                    cv2.rectangle(frame, btn.position, (x + w , y + h ), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, btn.text, (x + 20, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    text += btn.text              ### Update the text on every click
                    time.sleep(0.25)              ### Time delay between two clicks so that the click dont happen very quickly

    cv2.imshow("frame",frame)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows
