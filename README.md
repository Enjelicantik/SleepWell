# 🛌 SleepWell Sleep & Skin Condition Tracker

Track your sleep and monitor your skin — all in one simple desktop app.

## 🌟 About the Project

This app was born out of a personal need: I kept noticing changes in my facial skin depending on how well (or poorly) I slept. When I slept less than 6 hours, my skin would feel dry or break out the next day. But with 7–8 hours of rest, everything felt balanced again.

So, I built this tracker to monitor my sleep duration and compare it with my skin condition before and after sleep. It gives you insights, warnings, and helpful reminders so you can take better care of both your sleep and skin.

---

## 📆 Features

-   👥 **Multi-User Support** – Create and manage multiple user profiles
-   🛌 **Sleep Logging** – Record when you go to bed and wake up
-   😭 **Skin Condition Tracker** – Note your skin condition before & after sleep
-   ⏳ **Sleep Duration Calculation** – Automatic duration calculation
-   ⚠️ **Sleep Warning** – Alerts you if you sleep less than 6 hours
-   ⏰ **Sleep Reminder** – Get notified when it's time to go to bed
-   💾 **JSON Storage** – Data is stored locally in JSON files
-   🖼️ **Simple GUI** – Built with Tkinter

---

## 📂 Project Structure

```
SleepWell/
├── main.py                 # Main application entry point
├── models/                 # Folder for all model classes
│   ├── base_tracker.py     # Abstract base class
│   ├── user.py             # User model
│   ├── sleep_record.py     # Individual sleep record
│   └── profile_manager.py  # Manages all user profiles
├── data/                   # Stores all JSON data files
│   ├── profiles.json       # Index of user profiles
│   └── [username].json     # User-specific sleep data
└── README.md               # This file!
```

---

## 💻 Getting Started

### Requirements

-   Python 3.7 or newer
-   Tkinter (comes with most Python installations)

### How to Run

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/SleepWell.git
    ```

2. Navigate to the project folder:

    ```bash
    cd SleepWell
    ```

3. Run the app:

    ```bash
    python main.py
    ```

---

## 🕹 How to Use

1. **Create a Profile**: Click “New Profile” and enter your name.
2. **Select Profile**: Use the dropdown to choose your profile.
3. **Set a Reminder**: Pick your ideal bedtime.
4. **Start Sleeping**:

    - Select your skin condition (dry / normal / acne)
    - Click "Start Sleep"

5. **Wake Up**:

    - Select skin condition after waking
    - Click "Wake Up"

6. **View History**: All your logs appear in a table.

---

## 🎥 Demo Video (Youtube)

<video src="demo.mp4" />

## 📜 License

This project was created for learning purposes and as an academic project to explore OOP and GUI development in Python. Feel free to fork and modify it for personal use or experimentation.
