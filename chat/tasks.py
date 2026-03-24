from datetime import datetime

def send_daily_reminder(user_id, task_name):
    # This runs in the background. 
    # For now, we just print it to the console.
    print(f"--- 🔔 REMINDER ---")
    print(f"User ID: {user_id}")
    print(f"Task: {task_name}")
    print(f"Time: {datetime.now().strftime('%H:%M')}")