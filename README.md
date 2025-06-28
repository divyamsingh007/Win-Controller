# Win-Controller
A Python-based tool to control basic Windows actions like switching, minimizing, and maximizing windows using hand gestures captured via webcam.

# ✋ Gesture-Based Windows Controller

A Python-based tool to control basic Windows window management functions like switching, minimizing, and maximizing windows using **hand gestures** captured from a webcam.

## 🧠 Motivation

Ever felt too lazy to press Alt + Tab?  
I did.  
So I decided to make my laptop listen to my hands instead.  

This started as a fun detour while I was learning the MERN stack — and ended up becoming a useful gesture-control utility that could be scaled into something more meaningful.

---

## 🎯 Features

- ✌️ **Peace Sign** → Toggle gesture control (on/off)
- ✊ **Fist** → Minimize the current window
- 🖐️ **Open Palm** → Maximize the current window
- 👉 **Swipe Right** → Switch to next window (Alt + Tab)
- 👈 **Swipe Left** → Switch to previous window (Shift + Alt + Tab)
- 🪟 **Always-on-top GUI panel** using Tkinter to toggle control and exit app

---

## 🛠️ Tech Stack & Libraries

| Tool / Library   | Role                                      |
|------------------|-------------------------------------------|
| `OpenCV`         | Webcam input and image processing         |
| `MediaPipe`      | Real-time hand tracking & landmarks       |
| `PyAutoGUI`      | Simulate system keyboard actions          |
| `Tkinter`        | Lightweight Python GUI for control panel  |
| `time`           | Gesture cooldown handling                 |

---
