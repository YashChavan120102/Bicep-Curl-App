
# 💪 Real-Time Bicep Curl Tracker

This is an interactive, webcam-based bicep curl counter app built with **Streamlit** and **MediaPipe**. It not only counts your reps in real-time but also gives you **form feedback, tempo suggestions, breathing guidance**, and **voice alerts**. You can even set target reps and track your session dynamically.

---

## 🚀 Features

- 🎯 **Set target reps** for your workout
- 🗣️ **Voice feedback** for posture, speed, and encouragement
- 🧠 Real-time form analysis using **MediaPipe**
- 🧘 Breathing cue: Inhale/Exhale indicators
- ⚡ Speed check: "Too fast", "Too slow", or "Good pace"
- 📈 Session memory using `st.session_state`
- ✅ Fully deployable on Streamlit Cloud or local machine

---

## 📂 Folder Structure

```
📁 enhanced_bicep_app/
├── app.py              # Main Streamlit app
├── bicep_counter.py    # Pose detection, angle calculation, feedback logic
├── requirements.txt    # All dependencies
└── README.md           # This file
```

---

## 🧪 Installation

### ✅ Requirements:
- Python 3.8–3.10 recommended

### ⚙️ Steps:
```bash
git clone <repo-url>
cd enhanced_bicep_app
pip install -r requirements.txt
streamlit run app.py
```

> For voice feedback to work properly on all systems, ensure you have audio drivers and necessary TTS packages (like `espeak` on Linux).

---

## 🌐 Deploy to Streamlit Cloud

Just upload the `enhanced_bicep_app/` folder with all files to your [Streamlit Cloud workspace](https://streamlit.io/cloud) and click **Deploy**.

---

## 🧠 How It Works

- Uses `streamlit-webrtc` for webcam feed
- `mediapipe` tracks pose landmarks in real-time
- Calculates elbow angle to count reps
- Monitors shoulder alignment and movement speed
- Provides audible feedback via `pyttsx3`

---

## 🛠️ Future Ideas

- 🎤 Voice commands: start/stop/set goals
- 🏋️ Add more exercise support (squats, push-ups, etc.)
- 🏆 Leaderboard or personal workout log
- 🌍 Cloud-based user profiles and progress tracking

---

## 🧑‍💻 Author

Built with 💪 by **Vinayak Kumbhar**

---

## 📃 License

MIT — feel free to use and modify!
