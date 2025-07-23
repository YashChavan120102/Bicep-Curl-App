
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

class BicepCurlCounter:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.rep_start_time = None
        self.speed_feedback = ""
        self.breath_stage = ""
        self.posture_feedback = ""

    def process_landmarks(self, landmarks, time):
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        angle = calculate_angle(shoulder, elbow, wrist)

        left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
        right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
        if abs(left_shoulder_y - right_shoulder_y) > 0.05:
            self.posture_feedback = "Align your shoulders!"
        else:
            self.posture_feedback = ""

        if angle > 160:
            if self.stage != "down":
                self.rep_start_time = time
            self.stage = "down"
            self.breath_stage = "Inhale"
        elif angle < 30 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            duration = time - self.rep_start_time if self.rep_start_time else 0
            if duration < 1:
                self.speed_feedback = "Too fast, slow down"
            elif duration > 4:
                self.speed_feedback = "Too slow, speed up"
            else:
                self.speed_feedback = "Good pace"
            self.breath_stage = "Exhale"

        return angle
