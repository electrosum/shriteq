## Tech Stack

This project demonstrates energy-saving using face detection with a Raspberry Pi, relay, and bulb, all monitored via a web dashboard.

### **Hardware**
- **Raspberry Pi** (4 or above recommended)
- **Pi Camera** or USB Camera
- **Relay Module** (to control the bulb)
- **Bulb / Load**

### Software & Programming
- **Python** – Main programming language
- **OpenCV** – Face detection
- **GPIO Libraries** (`gpiozero` or `RPi.GPIO`) – Relay control
- **Flask** – Web dashboard backend
- **Threading** – Simultaneous camera processing and web server
- **SQLite / JSON / CSV** – Energy usage logging

### **Web Dashboard**
- **Frontend**:
  - HTML / CSS / JavaScript
  - Charts: **Chart.js** or **Plotly.js** for visualizing energy usage

### **Energy Monitoring Logic**
- Energy usage calculation:  
  `Energy (Wh) = Power (W) × Time (h)`
- Track energy saved when no face is detected (relay OFF)

### **Optional Enhancements**
- Real-time dashboard updates using **WebSocket / Socket.IO**
- Optimized face detection (Haar cascades or OpenCV DNN)
