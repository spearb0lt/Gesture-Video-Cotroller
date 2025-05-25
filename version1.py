import cv2
import mediapipe as mp
import pyautogui
import time

# Configuration
DEBUG = True
MAX_NUM_HANDS = 1
DETECTION_CONFIDENCE = 0.7
HISTORY_LENGTH = 5
GESTURE_COOLDOWN = 0.04  # fast gesture response
KEY_HOLDING_GESTURES = ["2x"]

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=MAX_NUM_HANDS, min_detection_confidence=DETECTION_CONFIDENCE)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Could not open webcam.")
    exit()

# Gesture to key mapping
GESTURE_ACTIONS = {
    "back": "left",
    "ahead": "right",
    "volume_up": "volumeup",
    "volume_down": "volumedown",
    "fullscreen": "f",
    "palm": "space",
    "2x": "space",  # hold key
    "up": "up",
    "down": "down"
}

# State variables
gesture_history = []
prev_gesture = None
last_action_time = 0
held_keys = set()

def detect_gesture(landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x else 0)
    # Other fingers
    for i in range(1, 5):
        fingers.append(1 if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y else 0)

    # Define gestures
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
    key = GESTURE_ACTIONS.get(gesture)
    if key:
        if gesture in KEY_HOLDING_GESTURES:
            if key not in held_keys:
                pyautogui.keyDown(key)
                held_keys.add(key)
                print(f"Holding: {gesture} → '{key}'")
        else:
            pyautogui.press(key)
            print(f"Performed: {gesture} → '{key}'")
    else:
        print(f"No action mapped for gesture: {gesture}")

print("Gesture control started. Press 'Q' to quit.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame not received. Exiting...")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        current_gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                current_gesture = detect_gesture(hand_landmarks.landmark)

                gesture_history.append(current_gesture)
                if len(gesture_history) > HISTORY_LENGTH:
                    gesture_history.pop(0)

                # Stable gesture check
                if gesture_history.count(current_gesture) >= 4:
                    if current_gesture != prev_gesture and (time.time() - last_action_time) > GESTURE_COOLDOWN:
                        perform_action(current_gesture)
                        prev_gesture = current_gesture
                        last_action_time = time.time()

        # Release key if holding gesture has ended
        for gesture in KEY_HOLDING_GESTURES:
            key = GESTURE_ACTIONS[gesture]
            if prev_gesture == gesture and current_gesture != gesture and key in held_keys:
                pyautogui.keyUp(key)
                held_keys.remove(key)
                print(f"Released: {gesture} → '{key}'")

        if DEBUG:
            cv2.putText(frame, f'Gesture: {current_gesture}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Gesture Controller", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release any held keys on exit
    for key in held_keys:
        pyautogui.keyUp(key)
    cap.release()
    cv2.destroyAllWindows()
    print("Exited Gesture Controller.")
