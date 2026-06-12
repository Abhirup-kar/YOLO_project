import streamlit as st
import cv2
import time
import requests
from ultralytics import YOLO

st.title("🛡️ Local Intruder Detection Test")
st.write("This app runs entirely on your machine using your local webcam.")

# ===================================================
# CONFIGURATION & INITIALIZATION
# ===================================================
TELEGRAM_TOKEN = "8658774188:AAHnM_cVZHDMPZH_PCbiUA1BgROjuBHD1Qg"
TELEGRAM_CHAT_ID = "7397575620"
ALERT_COOLDOWN = 15  

@st.cache_resource
def load_model():
    # Uses standard model. Replace with "best.pt" if testing your Roblox weights!
    return YOLO("best.pt") 

model = load_model()

def send_telegram_alert(image_path, timestamp):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    caption = f"⚠️ LOCAL TEST: INTRUDER DETECTED! ⚠️\nTime: {timestamp}"
    try:
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            requests.post(url, files=files, data=data)
            print("Telegram alert sent successfully!")
    except Exception as e:
        print(f"Telegram error: {e}")

# ===================================================
# STREAMLIT INTERFACE & CAMERA LOOP
# ===================================================
# A simple checkbox to turn the system on/off
run_system = st.checkbox("Turn On Webcam System", value=False)
FRAME_WINDOW = st.image([]) # A placeholder to render video frames in the UI

if "local_last_alert" not in st.session_state:
    st.session_state.local_last_alert = 0

if run_system:
    # Open local webcam (0 is default built-in camera)
    cap = cv2.VideoCapture(0)
    
    while run_system:
        success, frame = cap.read()
        if not success:
            st.error("Failed to read from webcam.")
            break
            
        # Run YOLOv11 inference
        results = model(frame, verbose=False)
        intruder_detected = False
        
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                if class_id == 0 and confidence > 0.5: # Person detected
                    intruder_detected = True
                    
                    # Draw box on frame
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, f"Intruder: {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Check cooldown and trigger alert
        current_time = time.time()
        if intruder_detected and (current_time - st.session_state.local_last_alert > ALERT_COOLDOWN):
            st.session_state.local_last_alert = current_time
            readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
            
            # Save frame snapshot locally and send alert
            snapshot_filename = f"local_intruder_{int(current_time)}.jpg"
            cv2.imwrite(snapshot_filename, frame)
            send_telegram_alert(snapshot_filename, readable_time)
            
        # Convert frame from BGR (OpenCV format) to RGB (Streamlit format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Render the updated frame directly into the browser dashboard placeholder
        FRAME_WINDOW.image(frame_rgb)
        
    cap.release()
else:
    st.info("System is currently offline. Check the box above to start.")