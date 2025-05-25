import cv2
import mediapipe as mp
import pyautogui
import time

# Init MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) 

# Gesture Recog
gesture_history = []
HISTORY_LENGTH = 5
prev_gesture = None
last_action_time = 0
cooldown = 0.04 #last try 0.5: still not rapid

def detect_gesture(landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x else 0)
    # Other fingers
    for i in range(1, 5):
        fingers.append(1 if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y else 0)

    if fingers == [0, 1, 1, 0, 0]:
        return "back"
    elif fingers == [1, 1, 1, 1, 1]:
        return "palm"
    elif fingers == [0, 1, 0, 0, 0]:
        return "ahead"
    elif fingers == [0, 1, 1, 1, 0]:
        return "volume_up"
    elif fingers == [0, 1, 1, 1, 1]:
        return "volume_down"
    elif fingers == [1, 1, 1, 0, 0]:
        return "fullscreen"
    elif fingers == [0, 1, 0, 0, 1]:
        return "2x"
    elif fingers == [1, 0, 0, 0, 0]:
        return "down"
    elif fingers == [0, 0, 0, 0, 1]:
        return "up"



    return "unknown"
    



def perform_action(gesture):
    if gesture == "palm":
        pyautogui.press("space")

    elif gesture == "2x":
        pyautogui.keyDown('space')


    # elif gesture == "up":
    #     pyautogui.press("up")
    # elif gesture == "down":
    #     pyautogui.press("down")


    elif gesture == "back":
        pyautogui.press("left")    
    elif gesture == "ahead":
        pyautogui.press("right") 
    elif gesture == "volume_up":
        pyautogui.press("volumeup")
    elif gesture == "volume_down":
        pyautogui.press("volumedown")
    elif gesture == "fullscreen":
        pyautogui.press("f")


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    current_gesture = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            current_gesture = detect_gesture(hand_landmarks.landmark)

            gesture_history.append(current_gesture)
            if len(gesture_history) > HISTORY_LENGTH:
                gesture_history.pop(0)

            if gesture_history.count(current_gesture) >= 4:
                if current_gesture != prev_gesture and (time.time() - last_action_time) > cooldown:
                    perform_action(current_gesture)
                    prev_gesture = current_gesture
                    last_action_time = time.time()

            cv2.putText(img, f'Gesture: {current_gesture}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

    cv2.imshow("Gesture Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
