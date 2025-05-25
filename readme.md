


# 🎮 Gesture Controller – Hand Tracking Control System

Control your media, browser, or system actions using intuitive hand gestures through your webcam. This project supports both single-hand and dual-hand operation modes.

---

## 🖐️ Single-Hand Mode – Supported Gestures

| Gesture               | Action          | Description                          |
|-----------------------|------------------|--------------------------------------|
| ✋ Palm               | Play / Pause     | All five fingers extended            |
| ✌️ Two Fingers (Index + Middle) | Volume Up      | Like a peace sign                    |
| ☝️ Point (Index Only) | Skip Forward     | Only the index finger up             |
| 🤘 Index + Pinky      | Volume Down      | Rock sign – index and pinky          |
| ✊ Fist               | Back / Previous  | All fingers curled                   |
| 👍 + ✌️ Full Hand (Thumb + Three) | Fullscreen       | Thumb, index, middle up              |
| 👆 Thumb Only         | Scroll Down      | Only thumb extended                  |
| 👉 Pinky Only         | Scroll Up        | Only pinky extended                  |
| ✌️ + 👉 Index + Pinky | 2x (Hold Key)    | Index and pinky held                 |

📝 **Note**: The gesture must be held steadily for ~0.2s to trigger the action. The `"2x"` gesture holds the space key; releasing the gesture releases the key.

---

## 🖐️🖐️ Dual-Hand Mode – Supported Gestures

Each hand works independently and supports the same set of gestures:

| Hand | Gesture             | Action           |
|------|---------------------|------------------|
| Left / Right | ✋ Palm              | Play / Pause      |
| Left / Right | ✊ Fist              | Back / Previous   |
| Left / Right | ☝️ Index Only        | Skip Forward      |
| Left / Right | ✌️ Index + Middle    | Volume Up         |
| Left / Right | 🤘 Index + Pinky     | Volume Down       |
| Left / Right | 👍 + ✌️ Thumb + Index + Middle | Fullscreen        |
| Left / Right | 👍 Thumb Only        | Scroll Down       |
| Left / Right | 👉 Pinky Only        | Scroll Up         |
| Left / Right | ✌️ + 👉 Index + Pinky | 2x (Hold)         |

💡 **Pro Tip**: You can perform different gestures with each hand simultaneously — e.g., volume up with one hand while skipping forward with the other.

---

## 🔧 System Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI

Install dependencies with:
```bash
pip install opencv-python mediapipe pyautogui
```

## ▶️ Launching the Controller

```bash
# For single-hand mode
python YOUR-PATH/version1.py #or version2
 # For two-hand mode
python gesture_controller_dual.py   
```

---

Made with ❤️ using OpenCV + MediaPipe + PyAutoGUI

