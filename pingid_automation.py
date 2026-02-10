"""
PingID Desktop Automation Module
Handles PingID.exe automation for MFA code retrieval
"""

import time
import subprocess
import pyperclip
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError
from config import PINGID_CONFIG


class PingIDAutomation:
    """Automates PingID desktop application for MFA"""

    def __init__(self, exe_path=None, pin=None, timeout=None):
        """
        Initialize PingID automation

        Args:
            exe_path: Path to PingID.exe (optional, defaults to config)
            pin: PIN code (optional, defaults to config)
            timeout: Wait timeout in seconds (optional, defaults to config)
        """
        self.exe_path = exe_path or PINGID_CONFIG["exe_path"]
        self.pin = pin or PINGID_CONFIG["pin"]
        self.timeout = timeout or PINGID_CONFIG["wait_timeout"]
        self.app = None

    def launch_pingid(self):
        """Launch PingID application"""
        try:
            print(f"Launching PingID from: {self.exe_path}")
            subprocess.Popen(self.exe_path)
            time.sleep(2)  # Wait for application to start
            return True
        except Exception as e:
            print(f"Error launching PingID: {str(e)}")
            return False

    def connect_to_pingid_window(self):
        """Connect to the PingID application window"""
        try:
            # Wait for PingID window to appear
            for attempt in range(self.timeout):
                try:
                    # Try to find PingID window by title (adjust title if needed)
                    desktop = Desktop(backend="uia")
                    windows = desktop.windows()

                    # Find PingID window (you may need to adjust the window title)
                    pingid_window = None
                    for window in windows:
                        window_text = window.window_text()
                        if "PingID" in window_text or "Ping" in window_text:
                            pingid_window = window
                            break

                    if pingid_window:
                        self.app = Application(backend="uia").connect(handle=pingid_window.handle)
                        print(f"Connected to PingID window: {window_text}")
                        return True

                    time.sleep(1)
                except ElementNotFoundError:
                    time.sleep(1)
                    continue

            print("PingID window not found within timeout period")
            return False

        except Exception as e:
            print(f"Error connecting to PingID window: {str(e)}")
            return False

    def enter_pin_and_get_code(self):
        """
        Enter PIN in PingID and retrieve the MFA code

        Returns:
            str: The MFA code copied from PingID, or None if failed
        """
        try:
            # Wait for window to fully load
            time.sleep(1)

            # Get the main window
            dlg = self.app.top_window()

            # Find and fill the PIN input field - try multiple methods
            print("Looking for PIN input field...")
            pin_input = None

            # Method 1: Try by found_index (most reliable - gets first Edit control)
            try:
                pin_input = dlg.child_window(control_type="Edit", found_index=0)
                print("Found PIN input by found_index")
            except Exception as e1:
                print(f"Method 1 failed: {str(e1)}")

                # Method 2: Try by auto_id
                try:
                    pin_input = dlg.child_window(auto_id="JavaFX42", control_type="Edit")
                    print("Found PIN input by auto_id")
                except Exception as e2:
                    print(f"Method 2 failed: {str(e2)}")

                    # Method 3: Try getting all Edit controls
                    try:
                        edit_controls = dlg.descendants(control_type="Edit")
                        if edit_controls:
                            pin_input = edit_controls[0]
                            print("Found PIN input from descendants")
                        else:
                            print("No Edit controls found")
                    except Exception as e3:
                        print(f"Method 3 failed: {str(e3)}")

            if pin_input is None:
                raise Exception("Could not find PIN input field with any method")

            # Enter the PIN
            try:
                pin_input.set_focus()
                time.sleep(0.3)
                pin_input.type_keys(self.pin, with_spaces=False, pause=0.1)
                print(f"Entered PIN successfully")
                time.sleep(0.5)
            except Exception as e:
                print(f"Error entering PIN: {str(e)}")
                raise

            # Find and click Next button - try multiple methods
            print("Looking for Next button...")
            next_button = None

            # Try by title first (most reliable for buttons)
            try:
                next_button = dlg.child_window(title="Next", control_type="Button")
                print("Found Next button by title")
            except Exception as e1:
                print(f"Method 1 failed: {str(e1)}")

                # Try by auto_id
                try:
                    next_button = dlg.child_window(auto_id="JavaFX49", control_type="Button")
                    print("Found Next button by auto_id")
                except Exception as e2:
                    print(f"Method 2 failed: {str(e2)}")

            if next_button is None:
                raise Exception("Could not find Next button")

            next_button.click()
            print("Clicked Next button")
            time.sleep(3)  # Wait for code to be generated

            # Find and click Copy button - try multiple methods
            print("Looking for Copy button...")
            copy_button = None

            # Try by title first (most reliable for buttons)
            try:
                copy_button = dlg.child_window(title="Copy", control_type="Button")
                print("Found Copy button by title")
            except Exception as e1:
                print(f"Method 1 failed: {str(e1)}")

                # Try by auto_id
                try:
                    copy_button = dlg.child_window(auto_id="JavaFX32", control_type="Button")
                    print("Found Copy button by auto_id")
                except Exception as e2:
                    print(f"Method 2 failed: {str(e2)}")

            if copy_button is None:
                raise Exception("Could not find Copy button")

            copy_button.click()
            print("Clicked Copy button")
            time.sleep(0.5)

            # Get the code from clipboard
            mfa_code = pyperclip.paste()
            print(f"Retrieved MFA code from clipboard: {mfa_code}")

            # Close PingID window (optional)
            try:
                dlg.close()
            except:
                pass

            return mfa_code

        except Exception as e:
            print(f"Error in enter_pin_and_get_code: {str(e)}")
            return None

    def get_mfa_code(self):
        """
        Complete workflow: Launch PingID, enter PIN, and retrieve MFA code

        Returns:
            str: The MFA code, or None if failed
        """
        try:
            # Launch PingID
            if not self.launch_pingid():
                return None

            # Connect to PingID window
            if not self.connect_to_pingid_window():
                return None

            # Enter PIN and get code
            mfa_code = self.enter_pin_and_get_code()

            return mfa_code

        except Exception as e:
            print(f"Error in get_mfa_code: {str(e)}")
            return None

    def print_window_info(self):
        """Debug helper: Print information about PingID window and controls"""
        try:
            if not self.app:
                print("App not connected. Run connect_to_pingid_window first.")
                return

            dlg = self.app.top_window()
            print("\n=== PingID Window Information ===")
            print(f"Window Title: {dlg.window_text()}")
            print("\nAll Controls:")
            dlg.print_control_identifiers()

        except Exception as e:
            print(f"Error printing window info: {str(e)}")


def automate_pingid_mfa():
    """
    Convenience function to automate PingID MFA

    Returns:
        str: The MFA code, or None if failed
    """
    pingid = PingIDAutomation()
    return pingid.get_mfa_code()


if __name__ == "__main__":
    # Test the automation
    print("Testing PingID automation...")
    code = automate_pingid_mfa()
    if code:
        print(f"\nSuccess! Retrieved MFA code: {code}")
    else:
        print("\nFailed to retrieve MFA code")
