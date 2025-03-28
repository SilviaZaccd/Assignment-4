# MoodHalo – Motion-Activated LED Headband for Posture & Eye Protection

MoodHalo is a smart headband designed to encourage better posture and reduce eye strain using motion detection, RGB light feedback, and visual notifications. It enhances focus and well-being through real-time head position monitoring and feedback via both physical and digital cues.

---

## 🧠 Concept

- **Primary Input:** IMU motion sensor to detect head tilt and direction.
- **Primary Output:** RGB LED strip on the headband that changes color based on posture.
- **Secondary Output:** Computer-based notifications using ProtoPie, providing visual alerts and posture cues.

---

## 📐 Posture Recognition Logic

![Head Movement Logic](diagrams/state-diagram.png) <!-- Replace with actual uploaded path or filename -->

Supported movements:
- **Vertical Tilt:** Up → Front-Up → Front → Front-Down → Down
- **Horizontal Turn:** Left → Front-Left → Front → Front-Right → Right

Each posture corresponds to a different LED color and a message sent to the ProtoPie app for live feedback.

---

## 🧰 Hardware List

- M5Stack Atom Lite
- IMU Pro Unit (connected to Port A)
- RGB LED Strip (WS2812 or compatible)
- USB-C Cable for power + serial data
- Headband structure or mount (custom or elastic)
- Breadboard / jumper wires (optional)

---

## 🔌 Wiring Diagram

- **IMU Sensor** → Port A (Red connector on Atom)
- **RGB Strip DIN** → G26
- **GND/5V** shared among components

![Hardware Wiring](wiring/hardware-setup.jpg)

---

## 🧾 Firmware Logic (Arduino)

1. Read IMU data (acceleration + gyroscope)
2. Classify head direction using angle thresholds
3. Update LED strip color accordingly
4. Send serial message to ProtoPie:  
   `direction||Front_Up`, `direction||Right`, etc.

[View full code here](firmware/final-nikita-4.py)

---

## 📱 ProtoPie App

- Listens to serial input via USB
- Receives formatted messages like `direction||Front_Down`
- Triggers visual responses:  
  - Background color
  - Textual feedback
  - Optional animations or haptics

ProtoPie shows real-time posture feedback in sync with hardware actions.

---

## 🎥 Media

- [Demo Video](media/demo-video.mp4)  
- ![Prototype Photo](media/prototype-photo.jpg)

---

## 📂 Folder Structure

# Assignment-4
