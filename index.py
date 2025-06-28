import cv2
import mediapipe as mp  # type: ignore
import pyautogui  # type: ignore
import time
from tkinter import Tk, Label, Button

control_enabled = False
last_action_time = 0
cooldown_period = 1.2
prev_index_pos = None


def toggle_control():
    global control_enabled
    control_enabled = not control_enabled
    status_label.config(text=f"Control Enabled: {control_enabled}")


def exit_app():
    root.destroy()
    cap.release()
    cv2.destroyAllWindows()


root = Tk()
root.title("Gesture Controller Panel")
root.attributes("-topmost", True)
root.resizable(False, False)
root.geometry("250x120+10+10")


def prevent_minimize(event=None):
    root.deiconify()


# root.bind("<Unmap>", prevent_minimize)

status_label = Label(root, text=f"Control Enabled: {control_enabled}")
status_label.pack(pady=10)

Button(root, text="Toggle Control (Peace Sign)", command=toggle_control).pack(pady=5)
Button(root, text="Exit", command=exit_app).pack(pady=5)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        gesture_text = "No Gesture"
        current_time = time.time()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                landmarks = hand_landmarks.landmark

                def finger_is_up(id_tip, id_dip):
                    return landmarks[id_tip].y < landmarks[id_dip].y

                fingers = [
                    finger_is_up(8, 6),
                    finger_is_up(12, 10),
                    finger_is_up(16, 14),
                    finger_is_up(20, 18),
                ]

                h, w, _ = frame.shape
                index_tip = landmarks[8]
                cx, cy = int(index_tip.x * w), int(index_tip.y * h)

                if prev_index_pos:
                    dx = cx - prev_index_pos[0]
                    if abs(dx) > 80:
                        if (
                            control_enabled
                            and current_time - last_action_time > cooldown_period
                        ):
                            if dx > 0:
                                gesture_text = "Swipe Right - Next Window"
                                pyautogui.hotkey("alt", "tab")
                            else:
                                gesture_text = "Swipe Left - Previous Window"
                                pyautogui.hotkey("shift", "alt", "tab")
                            last_action_time = current_time
                prev_index_pos = (cx, cy)

                # Peace Sign Detection
                if fingers[0] and fingers[1] and not any(fingers[2:]):
                    gesture_text = f"Peace Sign - Toggle Control {control_enabled}"
                    if current_time - last_action_time > cooldown_period:
                        toggle_control()
                        last_action_time = current_time

                # Fist = Minimize
                elif not any(fingers):
                    if (
                        control_enabled
                        and current_time - last_action_time > cooldown_period
                    ):
                        gesture_text = "Fist - Minimize Window"
                        pyautogui.hotkey("win", "down")
                        last_action_time = current_time

                # Open Palm = Maximize
                elif all(fingers):
                    if (
                        control_enabled
                        and current_time - last_action_time > cooldown_period
                    ):
                        gesture_text = "Open Palm - Maximize Window"
                        pyautogui.hotkey("win", "up")
                        last_action_time = current_time

                # # Pinch = Close Window
                # else:
                #     thumb_tip = landmarks[4]
                #     tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
                #     dist = ((cx - tx) ** 2 + (cy - ty) ** 2) ** 0.5

                #     if dist < 40:
                #         if (
                #             control_enabled
                #             and current_time - last_action_time > cooldown_period
                #         ):
                #             gesture_text = "Pinch - Close Window"
                #             pyautogui.hotkey("alt", "f4")
                #             last_action_time = current_time

        # Show gesture info
        cv2.putText(
            frame,
            f"Gesture: {gesture_text}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2,
        )

        cv2.imshow("Gesture Controller", frame)
        root.update()

        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

cap.release()
cv2.destroyAllWindows()
root.destroy()
