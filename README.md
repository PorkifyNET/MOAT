# MOAT
A simple tool to semi-automate the responses in the tedious Office Activation calls.

## What is MOAT?
MOAT is a simple tool that will give answers to the questions given to you by the Microsoft Activation Call Center. It will lead the call to the Activation Website using automated responses. This makes it much less tedious to sit in a call with a Microsoft robot for 2 minutes, giving the same answers again and again.

This tool normally is not useful for the average consumer, and tends to be more useful for people that do need to activate Office a lot of times by phone, think of PC refurbishing or other IT companies.

## How to use MOAT

### Requirements
- The computer you want to activate Office on.
- An Android Phone with:
   - USB debugging enabled
   - An activated SIM card
- A USB cable to plug said phone into your computer

### How to Prepare Your Phone for Use with MOAT

To automate the Microsoft Office activation process with MOAT, you'll need to enable **USB Debugging** on your phone. USB Debugging allows MOAT to interact with your phone using **ADB (Android Debug Bridge)**. Follow this step-by-step guide to prepare your Android device.

#### Step 1: Enable Developer Mode on Your Phone
To access the **USB Debugging** option, you'll first need to enable **Developer Mode** on your phone.

> [!CAUTION]
> Incorrect use of the USB debugging feature, or the incorrect use of the Developer Mode, can cause security risks or potential damage to your phone. Make sure to disable Developer Mode once you are finished using MOAT.

1. **Open the Settings app** on your phone.
2. **Scroll down and select "About phone"** (or "About device").
3. **Find "Build Number"** (it might be under "Software Information").
4. **Tap "Build Number" seven times** quickly. You may need to enter your phone's PIN or password if prompted.
5. You’ll see a message saying "**You are now a developer!**" or "**Developer mode has been enabled.**"

#### Step 2: Enable USB Debugging
Once Developer Mode is enabled, follow these steps to turn on USB Debugging:

1. **Go back to the Settings app** and scroll down to find **"Developer Options."**
   - This is usually under **System** or **Additional Settings** on some devices.
2. **Open Developer Options.**
3. Scroll down and **find the "USB Debugging" option**.
4. **Toggle USB Debugging ON.**
5. Confirm by pressing **OK** on the dialog box that appears.

#### Step 3: Connect Your Phone to Your Computer
1. Use a **USB cable** to connect your phone to the computer where MOAT is installed (you can run MOAT from a USB stick if needed).
2. A prompt will appear on your phone asking, "**Allow USB Debugging?**"
3. Check the box for **"Always allow from this computer"** and press **OK** to confirm.


#### Troubleshooting
- **No Device Detected**: If your device doesn't show up, ensure that:
  - USB Debugging is enabled.
  - The correct USB connection mode is selected (some phones need to be in **File Transfer (MTP)** mode).
  - Your USB cable is working and supports data transfer (not just charging).

- **Unauthorized Device**: If your device shows as **unauthorized**, disconnect and reconnect your phone. You may need to re-allow USB Debugging from the computer.

---

### How to Use MOAT (Microsoft Office Activation Tool)

MOAT is designed to simplify the process of activating Microsoft Office via telephone. Here’s a simple guide to get you started:

#### Step 1: Start the Tool
- **Launch MOAT** by double-clicking the application (from a USB stick if needed).
- On the welcome screen, click the **"Start"** button to begin the activation process.

#### Step 2: Follow the On-Screen Prompts
MOAT will guide you through the different stages of the activation call. Here’s what to expect:

1. **Call Microsoft**: MOAT will automatically dial the Microsoft activation center and put your phone on speaker.
2. **Decline Recording**: The system will ask if you want the call recorded. MOAT will automatically decline this for you.
3. **Manual Code Entry**: When prompted to enter a 3-digit code, pay attention to the instructions on your phone. **Enter the code manually** when MOAT asks you to.
4. **Confirm Options**: MOAT will automatically select the right options (e.g., confirming that the Activation Wizard is open).

#### Step 3: Receive the SMS
- Once you confirm the Activation Wizard, Microsoft will send you an SMS.
- **After receiving the SMS**, you can end the call early by pressing the **"End Call"** button or let MOAT handle it automatically.

#### Step 4: Complete the Process
Once the call ends, MOAT will show a message confirming that the SMS should have been received. You will then have the option to:
- **Start Over** if needed.
- Open the SMS link on your phone (if configured).

---

That’s it! MOAT handles most of the activation process for you. Just follow the prompts and you’ll have Office activated in no time.
