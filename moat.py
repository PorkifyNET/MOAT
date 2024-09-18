import os
import time
import threading
import tkinter as tk
from tkinter import N, ttk, messagebox, simpledialog
import sys
import webbrowser

class OfficeActivationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Microsoft Office Activation Tool (MOAT)")
        self.root.geometry("320x240")
        self.root.resizable(False, False)
        
        self.script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

        # Build the path to the ADB binary on the USB stick
        if os.name == 'nt':  # Windows
            self.adb_path = os.path.join(self.script_dir, 'adb', 'adb.exe')
        else:  # macOS/Linux
            self.adb_path = os.path.join(self.script_dir, 'adb', 'adb')

        self.setup_welcome_screen()

    def setup_welcome_screen(self):
        """Sets up the welcome screen."""
        self.clear_screen()
        os.system(f'"{self.adb_path}" devices')

        welcome_label = tk.Label(self.root, text="Welcome to MOAT (Microsoft Office Activation Tool)!\n\n"
                                                "This tool automates the process of activating Microsoft Office via telephone. "
                                                "Make sure your Android phone is plugged into the computer using USB and that USB debugging is enabled.\n"
                                                "Click 'Start' to begin the activation process.\n"
                                                "\n"
                                                "NOTE: Microsoft will block incoming calls for the day if you call 10 times.", padx=20, pady=5, wraplength=300)
        welcome_label.pack()

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_call_process)
        self.start_button.pack(pady=10)

        # Version number label
        version_label = tk.Label(self.root, text="Version 1.0", fg="grey", font=("Arial", 8))
        version_label.pack(side=tk.BOTTOM, pady=10)

        # Bind F1 key to open the URL only on this screen
        self.root.bind('<F1>', self.open_help_url)

    def clear_screen(self):
        """Clears the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_status(self, stage, progress=None):
        """Update the status label and progress bar."""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Current Stage: {stage}")
        if progress is not None:
            if hasattr(self, 'progress_var'):
                self.progress_var.set(progress)

    def open_help_url(self, event):
        """Opens the help URL when F1 is pressed."""
        webbrowser.open("https://example.com/help")  # Replace with the actual URL you want to open


    def start_call_process(self):
        """Starts the call process."""
        if not self.check_adb_device():
            messagebox.showerror("Error", "No ADB device connected. Please connect a device and try again.")
            return

        self.clear_screen()

        # Display status label and progress bar
        self.status_label = tk.Label(self.root, text="Starting process...")
        self.status_label.pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=20, fill=tk.X, padx=20)

        # Run the process in a separate thread
        threading.Thread(target=self.run_process).start()

    def enable_speakerphone(self):
        """Enable speakerphone mode by simulating a tap on the speaker button."""
        os.system(f'"{self.adb_path}" shell input tap 280 1600')  # Correct coordinates for speakerphone on the device

    def update_status(self, stage, duration):
        """Update the status label and dynamically update the progress bar."""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Current Stage: {stage}")

        self.progress_var.set(0)
        for i in range(duration):
            time.sleep(1)  # Wait 1 second at a time
            if hasattr(self, 'progress_var'):
                self.progress_var.set((i + 1) * 100 / duration)  # Update the progress bar
            self.root.update_idletasks()  # Ensure the UI updates during the wait

    def run_process(self):
        """Run the call process with dynamic progress updates."""
        self.dial_microsoft()
        time.sleep(1)  # Wait for the call to connect
        
        # Enable speakerphone mode
        self.enable_speakerphone()
        time.sleep(1)

        # Show the numberpad
        self.show_numberpad()
        
        # Step 1: Decline Recording
        self.update_status("Decline Recording (Step 1)", 21)
        self.decline_recording()

        # Step 2: Notify user to enter 3-digit code manually
        self.update_status("Input Security Code (Step 2)", 13)
        #self.notify_enter_code()
        self.input_3digit_code()

        # Step 3: Select 'Other Office Products'
        self.update_status("Select 'Other Office Products' (Step 3)", 10)
        self.select_other_office_products()

        # Step 4: Confirm Activation Wizard
        self.update_status("Confirm Activation Wizard (Step 4)", 7)
        self.confirm_activation_wizard()

        # Step 5: Send SMS
        self.update_status("Send SMS (Step 5)", 27)
        self.send_sms()

        self.end_process()

    def dial_microsoft(self):
        """Dial Microsoft's activation number."""
        os.system(f'"{self.adb_path}" shell am start -a android.intent.action.CALL -d tel:+318000233487')
        time.sleep(1)  # Wait for the call to connect

    def decline_recording(self):
        """Decline the recording (press 2)."""
        os.system(f'"{self.adb_path}" shell input text 2')

    def show_numberpad(self):
        """Tap to show the numberpad."""
        os.system(f'"{self.adb_path}" shell input tap 800 1600')  # Tap the numberpad button

    def input_3digit_code(self):
        """Prompt the user to input the 3-digit code and use adb to input the code."""
        # Ask for the 3-digit code
        codewin = tk.Tk()
        codewin.withdraw()
        code = simpledialog.askstring("Input Required", "Please enter the 3-digit code:", parent=codewin)
        codewin.destroy()
    
        if code is None or not code.isdigit() or len(code) != 3:
            messagebox.showerror("Input Error", "Please enter a valid 3-digit code.")
            return  # Exit if invalid input

        # Input the 3-digit code using adb shell input text
        os.system(f'"{self.adb_path}" shell input text {code}')
        time.sleep(1)  # Wait to ensure the input is processed

        # Update status after entering the code
        self.update_status("Code Entered", 0)

    def select_other_office_products(self):
        """Select 'Other Office Products' by pressing 3."""
        os.system(f'"{self.adb_path}" shell input text 3')

    def confirm_activation_wizard(self):
        """Confirm that the Activation Wizard is open (press 1)."""
        os.system(f'"{self.adb_path}" shell input text 1')

    def send_sms(self):
        """Agree to receive an SMS for activation and handle premature call ending."""
        # Agree on being sent an SMS (press 1).
        os.system(f'"{self.adb_path}" shell input text 1')

        # Create a label explaining that the call can be ended once the SMS has been received
        sms_info_label = tk.Label(self.root, text="The call can be ended once the SMS has been received.", pady=10)
        sms_info_label.pack()

        # Create a button to end the call prematurely
        self.end_call_button = ttk.Button(self.root, text="End Call Early", command=self.end_call_early)
        self.end_call_button.pack(pady=10)

        # Activate the end call button 3 seconds after starting the SMS stage
        threading.Timer(3, self.activate_end_call_button).start()

        # Simulate waiting for SMS to be received
        time.sleep(25)  # Adjust as needed for the duration of the SMS wait

        # Remove the end call button if it's still there
        if hasattr(self, 'end_call_button'):
            self.end_call_button.destroy()

        # Proceed to end the process
        self.end_process()

    def activate_end_call_button(self):
        """Activate the end call button."""
        if hasattr(self, 'end_call_button'):
            self.end_call_button.config(state=tk.NORMAL)

    def end_call_early(self):
        """End the call early and proceed to the end screen."""
        os.system(f'"{self.adb_path}" shell input keyevent 6')  # Simulate tapping to end the call
        self.end_process()

    def open_link_on_phone(self):
        """Placeholder function to open a link on the phone."""
        messagebox.showinfo("Info", "Functionality to open link on phone is not implemented.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OfficeActivationApp(root)
    root.mainloop()
