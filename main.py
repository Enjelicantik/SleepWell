import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
from models.user import User
from models.sleep_record import SleepRecord
from models.profile_manager import ProfileManager

class SleepTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SLEEP WELL - Sleep & Skin Condition Tracker")
        self.root.geometry("900x700")
        self.center_window(self.root, 900, 700)
        self.root.configure(bg='#f0f0f0')
        
        # Initialize profile manager
        self.profile_manager = ProfileManager()
        self.current_user = None
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create widgets before checking reminder (so reminder_var exists)
        self.create_widgets()
        self.load_profiles()
        self.check_sleep_reminder()
        
    def center_window(self, window, width, height):
        """Center a window on the screen."""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="SLEEP WELL - Sleep & Skin Condition Tracker", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Profile selection frame
        profile_frame = ttk.LabelFrame(main_frame, text="Profile Selection", padding="10")
        profile_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(profile_frame, text="Select Profile:").grid(row=0, column=0, padx=(0, 10))
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(profile_frame, textvariable=self.profile_var, 
                                         state="readonly", width=20)
        self.profile_combo.grid(row=0, column=1, padx=(0, 10))
        self.profile_combo.bind('<<ComboboxSelected>>', self.on_profile_selected)
        
        ttk.Button(profile_frame, text="New Profile", 
                  command=self.create_new_profile).grid(row=0, column=2, padx=(10, 0))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(settings_frame, text="Sleep Reminder Time:").grid(row=0, column=0, padx=(0, 10))
        self.reminder_var = tk.StringVar(value="21:00")
        reminder_combo = ttk.Combobox(settings_frame, textvariable=self.reminder_var, 
                                     values=[f"{i:02d}:00" for i in range(20, 24)], 
                                     state="readonly", width=10)
        reminder_combo.grid(row=0, column=1, padx=(0, 10))
        reminder_combo.bind('<<ComboboxSelected>>', self.update_reminder_time)
        
        # Sleep tracking frame
        self.tracking_frame = ttk.LabelFrame(main_frame, text="Sleep Tracking", padding="10")
        self.tracking_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Skin condition selection
        ttk.Label(self.tracking_frame, text="Skin Condition:").grid(row=0, column=0, padx=(0, 10))
        self.skin_var = tk.StringVar(value="normal")
        skin_combo = ttk.Combobox(self.tracking_frame, textvariable=self.skin_var, 
                                 values=["kering", "normal", "berjerawat"], 
                                 state="readonly", width=15)
        skin_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Sleep/Wake buttons
        self.sleep_btn = ttk.Button(self.tracking_frame, text="Start Sleep", 
                                   command=self.start_sleep, state="disabled")
        self.sleep_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.wake_btn = ttk.Button(self.tracking_frame, text="Wake Up", 
                                  command=self.wake_up, state="disabled")
        self.wake_btn.grid(row=0, column=3)
        
        # Sleep records frame
        records_frame = ttk.LabelFrame(main_frame, text="Sleep Records", padding="10")
        records_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview for records
        columns = ('Date', 'Sleep Time', 'Wake Time', 'Duration', 'Skin Before', 'Skin After')
        self.tree = ttk.Treeview(records_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        records_frame.columnconfigure(0, weight=1)
        records_frame.rowconfigure(0, weight=1)
        
    def load_profiles(self):
        """Load existing profiles into combobox"""
        profiles = self.profile_manager.get_all_profiles()
        self.profile_combo['values'] = profiles
        if profiles:
            self.profile_combo.set(profiles[0])
            self.on_profile_selected()
    
    def create_new_profile(self):
        """Create new user profile"""
        def save_profile():
            name = name_entry.get().strip()
            if name:
                if self.profile_manager.create_profile(name):
                    messagebox.showinfo("Success", f"Profile '{name}' created successfully!")
                    self.load_profiles()
                    dialog.destroy()  # Close dialog immediately after creation
                    self.profile_combo.set(name)
                    self.on_profile_selected()
                else:
                    messagebox.showerror("Error", "Profile name already exists!")
            else:
                messagebox.showerror("Error", "Please enter a name!")
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Profile")
        self.center_window(dialog, 300, 150)
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter your name:").pack(pady=20)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        ttk.Button(dialog, text="Create", command=save_profile).pack(pady=10)
        
        dialog.bind('<Return>', lambda e: save_profile())
    
    def on_profile_selected(self, event=None):
        """Handle profile selection"""
        selected_profile = self.profile_var.get()
        if selected_profile:
            self.current_user = self.profile_manager.get_profile(selected_profile)
            self.sleep_btn['state'] = 'normal'
            # Enable wake_btn if there is an active sleep session
            if self.current_user and self.current_user.is_sleeping():
                self.wake_btn['state'] = 'normal'
                self.sleep_btn['state'] = 'disabled'
            else:
                self.wake_btn['state'] = 'disabled'
            self.update_records_display()
    
    def start_sleep(self):
        """Start sleep tracking"""
        if not self.current_user:
            messagebox.showerror("Error", "Please select a profile first!")
            return
        
        skin_condition = self.skin_var.get()
        
        if self.current_user.start_sleep(skin_condition):
            self.sleep_btn['state'] = 'disabled'
            self.wake_btn['state'] = 'normal'
            messagebox.showinfo("Sleep Started", f"Sleep tracking started at {datetime.now().strftime('%H:%M')}")
            self.update_records_display()
        else:
            messagebox.showerror("Error", "You already have an active sleep session!")
    
    def wake_up(self):
        """End sleep tracking"""
        if not self.current_user:
            messagebox.showerror("Error", "Please select a profile first!")
            return
        
        skin_condition = self.skin_var.get()
        
        result = self.current_user.wake_up(skin_condition)
        if result:
            self.sleep_btn['state'] = 'normal'
            self.wake_btn['state'] = 'disabled'
            
            duration_hours = result['duration_hours']
            duration_minutes = result['duration_minutes']
            
            if duration_hours < 6:
                messagebox.showwarning("Sleep Warning", 
                                     f"You only slept for {duration_hours}h {duration_minutes}m!\n"
                                     "It's recommended to sleep at least 6-8 hours per night.")
            else:
                messagebox.showinfo("Good Sleep", 
                                   f"You slept for {duration_hours}h {duration_minutes}m. Good job!")
            
            self.update_records_display()
        else:
            messagebox.showerror("Error", "No active sleep session found!")
    
    def update_records_display(self):
        """Update the records display in treeview"""
        # Clear existing records
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.current_user:
            return
        
        # Add records to treeview
        for record in self.current_user.sleep_records:
            if record.wake_time:  # Only show completed records
                duration_str = f"{record.duration_hours}h {record.duration_minutes}m"
                date_str = record.sleep_time.strftime('%Y-%m-%d')
                sleep_time_str = record.sleep_time.strftime('%H:%M')
                wake_time_str = record.wake_time.strftime('%H:%M')
                
                item = self.tree.insert('', 'end', values=(
                    date_str, sleep_time_str, wake_time_str, duration_str,
                    record.skin_before, record.skin_after
                ))
                
                # Highlight short sleep in red
                if record.duration_hours < 6:
                    self.tree.item(item, tags=('short_sleep',))
        
        # Configure tag colors
        self.tree.tag_configure('short_sleep', background='#ffcccc')
    
    def check_sleep_reminder(self):
        """Check if it's time for sleep reminder"""
        current_time = datetime.now().time()
        reminder_time = datetime.strptime(self.reminder_var.get(), "%H:%M").time()
        
        if current_time >= reminder_time:
            messagebox.showinfo("Sleep Reminder", 
                               f"It's {current_time.strftime('%H:%M')} - Time to sleep!")
    
    def update_reminder_time(self, event=None):
        """Update reminder time setting"""
        # Save reminder time to user settings if needed
        pass

def main():
    root = tk.Tk()
    app = SleepTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()