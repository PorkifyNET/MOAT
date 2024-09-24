import ctypes
import os
import subprocess
import time
import threading
import tkinter as tk
from tkinter import N, PhotoImage, ttk, messagebox, simpledialog
import sys
import webbrowser
import re
from PIL import Image, ImageTk

def run_command(cmd):
    # Use SW_HIDE (0) to hide the console window
    SW_HIDE = 0
    ctypes.windll.kernel32.WinExec(cmd.encode('utf-8'), SW_HIDE)

class OfficeActivationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Microsoft Office Activation Tool (MOAT)")
        self.root.iconbitmap("moat.ico")
        self.root.geometry("320x240")
        self.root.resizable(False, False)
        
        self.script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

        # Build the path to the ADB binary on the USB stick
        self.adb_path = os.path.join(os.getcwd(), '..', 'adb', 'adb.exe')
        
        # Load the icons for each stage
        self.icons = {
            "start": ImageTk.PhotoImage(Image.open("icons/start.png")),
            "recording": ImageTk.PhotoImage(Image.open("icons/decline_recording.png")),
            "code": ImageTk.PhotoImage(Image.open("icons/enter_code.png")),
            "select": ImageTk.PhotoImage(Image.open("icons/dropper.png")),
            "confirm": ImageTk.PhotoImage(Image.open("icons/confirm.png")),
            "sms": ImageTk.PhotoImage(Image.open("icons/send_sms.png")),
            "notification": ImageTk.PhotoImage(Image.open("icons/notification.png")),
            "end": ImageTk.PhotoImage(Image.open("icons/end.png")),
        }

        self.setup_welcome_screen()
        
    def get_microsoft_sms():
        try:
            # Query SMS inbox for messages containing 'Microsoft'
            result = subprocess.check_output(
                ["adb", "shell", "content query --uri content://sms/inbox --projection address,body --where \"body LIKE '%Microsoft%'\""],
                universal_newlines=True
            )

            # Search for the activation link in the message body
            match = re.search(r'http[s]?://\S+', result)
            if match:
                return match.group(0)  # Return the URL
            else:
                return None
        except subprocess.CalledProcessError:
            return None
        
    def open_activation_link(link):
        # Open the activation link in the phone's browser
        subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", link])

    def update_stage_icon(self, stage):
        """Update the displayed stage icon."""
        try:
            self.stage_icon_label.config(image=self.icons[stage])
        except Exception as e:
            print(e)

    def setup_welcome_screen(self):
        """Sets up the welcome screen."""
        self.clear_screen()
        run_command(f'"{self.adb_path}" devices')

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
        version_label = tk.Label(self.root, text="A PorkifyNET product, Version 1.0", fg="grey", font=("Arial", 8))
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
        webbrowser.open("https://github.com/PorkifyNET/MOAT/blob/main/README.md")  # Replace with the actual URL you want to open
        

    def start_call_process(self):
        """Starts the call process."""

        self.clear_screen()

        self.stage_icon_label = tk.Label(self.root,image=ImageTk.PhotoImage(Image.open("icons/start.png")))
        self.stage_icon_label.pack(padx=10,pady=10,anchor=N)

        # Display status label and progress bar
        self.status_label = tk.Label(self.root, text="Starting process...")
        self.status_label.pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=20, fill=tk.X, padx=20)
        
        self.update_stage_icon("start")

        # Run the process in a separate thread
        threading.Thread(target=self.run_process).start()

    def enable_speakerphone(self):
        """Enable speakerphone mode by simulating a tap on the speaker button."""
        run_command(f'"{self.adb_path}" shell input tap 280 1600')  # Correct coordinates for speakerphone on the device
        self.update_stage_icon("recording")

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
        self.update_stage_icon("recording")
        self.update_status("Decline Recording (Step 1)", 21)
        self.decline_recording()

        # Step 2: Notify user to enter 3-digit code manually
        self.update_stage_icon("code")
        self.update_status("Input Security Code (Step 2)", 13)
        self.input_3digit_code()

        # Step 3: Select 'Other Office Products'
        self.update_stage_icon("select")
        self.update_status("Select 'Other Office Products' (Step 3)", 15)
        self.select_other_office_products()

        # Step 4: Confirm Activation Wizard
        self.update_stage_icon("confirm")
        self.update_status("Confirm Activation Wizard (Step 4)", 7)
        self.confirm_activation_wizard()

        # Step 5: Send SMS
        self.update_stage_icon("sms")
        self.update_status("Send SMS (Step 5)", 27)
        self.send_sms()

        self.end_process()

    def dial_microsoft(self):
        """Dial Microsoft's activation number."""
        run_command(f'"{self.adb_path}" shell am start -a android.intent.action.CALL -d tel:+318000233487')
        time.sleep(1)  # Wait for the call to connect

    def decline_recording(self):
        """Decline the recording (press 2)."""
        run_command(f'"{self.adb_path}" shell input text 2')

    def show_numberpad(self):
        """Tap to show the numberpad."""
        run_command(f'"{self.adb_path}" shell input tap 800 1600')  # Tap the numberpad button

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
        run_command(f'"{self.adb_path}" shell input text {code}')
        time.sleep(1)  # Wait to ensure the input is processed

        # Update status after entering the code
        self.update_status("Code Entered", 0)

    def select_other_office_products(self):
        """Select 'Other Office Products' by pressing 3."""
        run_command(f'"{self.adb_path}" shell input text 3')

    def confirm_activation_wizard(self):
        """Confirm that the Activation Wizard is open (press 1)."""
        run_command(f'"{self.adb_path}" shell input text 1')

    def send_sms(self):
        """Agree to receive an SMS for activation and handle premature call ending."""
        # Agree on being sent an SMS (press 1).
        run_command(f'"{self.adb_path}" shell input text 1')

        # Create a label explaining that the call can be ended once the SMS has been received
        sms_info_label = tk.Label(self.root, text="The call can be ended once the SMS has been received.", pady=1)
        sms_info_label.pack()

        # Create a button to end the call prematurely
        self.end_call_button = ttk.Button(self.root, text="End Call Early", command=self.end_call_early)
        self.end_call_button.pack(pady=1)

        # Activate the end call button 3 seconds after starting the SMS stage
        threading.Timer(3, self.activate_end_call_button).start()
        self.update_stage_icon("notification")

        # Simulate waiting for SMS to be received
        time.sleep(25)  # Adjust as needed for the duration of the SMS wait

        # Remove the end call button if it's still there
        if hasattr(self, 'end_call_button'):
            self.end_call_button.destroy()

        # Proceed to end the process
        self.end_process()

    def activate_end_call_button(self):
        """Activate the end call button."""
        try:
            if hasattr(self, 'end_call_button'):
                self.end_call_button.config(state=tk.NORMAL)
        except Exception as e:
            print(e)

    def end_call_early(self):
        """End the call early and proceed to the end screen."""
        run_command(f'"{self.adb_path}" shell input keyevent 6')  # Simulate tapping to end the call
        self.end_process()

    def end_process(self):
        """Show end screen with options to start over or open link."""
        self.clear_screen()

        time.sleep(0.2)
        
        self.end_icon_label = tk.Label(self.root,image=ImageTk.PhotoImage(Image.open("icons/end.png")))
        self.end_icon_label.pack(padx=10,pady=5,anchor=N)

        end_message = tk.Label(self.root, text="The SMS should have been received. Please check your phone for the link.\n"
                               "\n"
                               "Thank you for using MOAT!", wraplength=300, padx=20)
        end_message.pack(pady=10)
        
        start_over_button = ttk.Button(self.root, text="Start Over", command=self.setup_welcome_screen)
        start_over_button.pack(side=tk.LEFT, padx=20)

        # The link should be opened on the phone, not on the computer.
        open_link_button = ttk.Button(self.root, text="Open Link on Phone", command=self.open_link_on_phone)
        open_link_button.pack(side=tk.RIGHT, padx=20)

    def open_link_on_phone(self):
        """Placeholder function to open a link on the phone."""
        # Note: This function is a placeholder and should be replaced with actual implementation to open the link on the phone.
        # For now, it shows a message indicating that this is not implemented.
        
        
        #run_command(f'"{self.adb_path}" shell am start -a android.intent.action.SENDTO -d sms:Microsoft')
        #time.sleep(1)
        #run_command(f'"{self.adb_path}" shell input tap 350 2100')
        
        # Retrieve the activation link from the SMS and open it
        activation_link = self.get_microsoft_sms()
        if activation_link:
            print(f"Opening activation link: {activation_link}")
            self.open_activation_link(activation_link)
        else:
            print("No activation link found in SMS.")
        
        # Rest of the code needs to be implemented later on.


if __name__ == "__main__":
    root = tk.Tk()
    app = OfficeActivationApp(root)
    root.mainloop()
