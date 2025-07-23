
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import mediapipe as mp
import cv2
import time
import numpy as np
from bicep_counter import BicepCurlCounter
import pyttsx3
import os

st.set_page_config(page_title="Bicep Curl Trainer", layout="wide")

st.title("💪 Interactive Bicep Curl Trainer")

# Session state setup
if 'counter_obj' not in st.session_state:
    st.session_state.counter_obj = BicepCurlCounter()
if 'goal_reached' not in st.session_state:
    st.session_state.goal_reached = False

st.sidebar.header("Customize Your Session")
target_reps = st.sidebar.number_input("🎯 Set your target reps", min_value=1, max_value=100, value=10)
voice_enabled = st.sidebar.checkbox("🔊 Enable Voice Feedback", value=True)

# Function to generate and play voice feedback
def speak(text):
    if voice_enabled:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.save_to_file(text, "voice.mp3")
        engine.runAndWait()
        st.audio("voice.mp3", format="audio/mp3", autoplay=True)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class CurlVideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.last_feedback_time = 0

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        counter = st.session_state.counter_obj

        if results.pose_landmarks:
            angle = counter.process_landmarks(results.pose_landmarks.landmark, time.time())
            elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            coords = tuple(np.multiply([elbow.x, elbow.y], [img.shape[1], img.shape[0]]).astype(int))
            cv2.putText(img, str(int(angle)), coords, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            now = time.time()
            if now - self.last_feedback_time > 2:  # throttle feedback every 2 seconds
                if counter.posture_feedback:
                    speak(counter.posture_feedback)
                elif counter.speed_feedback in ["Too fast, slow down", "Too slow, speed up"]:
                    speak(counter.speed_feedback)
                self.last_feedback_time = now

        if counter.counter >= target_reps and not st.session_state.goal_reached:
            st.session_state.goal_reached = True
            speak("You hit your goal! Nice work!")

        # Info overlay
        cv2.rectangle(img, (0, 0), (400, 130), (245, 117, 16), -1)
        cv2.putText(img, f"Reps: {counter.counter}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        cv2.putText(img, f"Stage: {counter.stage}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        cv2.putText(img, f"Breath: {counter.breath_stage}", (200, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(img, f"Tempo: {counter.speed_feedback}", (200, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        if counter.posture_feedback:
            cv2.putText(img, counter.posture_feedback, (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        return img

webrtc_streamer(key="enhanced-bicep", video_transformer_factory=CurlVideoTransformer)
