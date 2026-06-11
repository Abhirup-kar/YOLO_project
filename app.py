import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import time
import requests
from ultralytics import YOLO

st.title("☁️ Cloud AI Intruder Detection Dashboard")

# ===================================================
# 1. SETUP & CONFIGURATION
# ===================================================
TELEGRAM_TOKEN = "8658774188:AAHnM_cVZHDMPZH_PCbiUA1BgROjuBHD1Qg"
TELEGRAM_CHAT_ID = "7397575620"
ALERT_COOLDOWN = 15  

# We use st.cache_resource so Streamlit doesn't reload the heavy 
# AI model every time the screen refreshes.
@st.cache_resource
def load_yolo_model():
    return YOLO("best.pt") # point to your 'best.pt' if using custom weights

model = load_yolo_model()

# Track the last alert time across frames using Streamlit's session state
if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0

# ===================================================
# 2. TELEGRAM ALERT FUNCTION
# ===================================================
def send_telegram_alert(image_path, timestamp):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    caption = f"⚠️ INTRUDER DETECTED! ⚠️\nTime: {timestamp}"
    try:
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            requests.post(url, files=files, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

# ===================================================
# 3. THE CALLBACK HANDLER (Just a function inside this file!)
# ===================================================
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    # Convert the incoming browser WebRTC frame into an OpenCV image array
    img = frame.to_ndarray(format="bgr24")
    
    # Run YOLOv11 inference
    results = model(img, verbose=False)
    intruder_detected = False

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            
            if class_id == 0 and confidence > 0.5:  # Person/Intruder class
                intruder_detected = True
                
                # Draw the bounding boxes using OpenCV
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(img, f"Intruder: {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Cooldown check for Telegram alerts
    current_time = time.time()
    if intruder_detected and (current_time - st.session_state.last_alert_time > ALERT_COOLDOWN):
        st.session_state.last_alert_time = current_time
        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
        
        # Save snapshot frame and trigger alert
        snapshot_filename = f"intruder_{int(current_time)}.jpg"
        cv2.imwrite(snapshot_filename, img)
        send_telegram_alert(snapshot_filename, readable_time)

    # Return the annotated frame back to the browser screen stream
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# ===================================================
# 4. WEB INTERFACE COMPONENT
# ===================================================
webrtc_streamer(
    key="intruder-detection", 
    video_frame_callback=video_frame_callback,
    # This configuration helps traverse strict network firewalls
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {"urls": ["stun:stun1.l.google.com:19302"]}
        ]
    }
)