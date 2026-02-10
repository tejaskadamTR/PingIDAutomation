"""
Automatic PingID window inspector - No user input required
Launches PingID and displays all controls
"""

import time
from pingid_automation import PingIDAutomation


def main():
    print("=" * 60)
    print("PingID Window Inspector (Automatic)")
    print("=" * 60)

    pingid = PingIDAutomation()

    # Launch PingID
    print("\n[1/3] Launching PingID...")
    if not pingid.launch_pingid():
        print("❌ Failed to launch PingID. Check exe_path in config.py")
        return

    # Connect to window
    print("\n[2/3] Connecting to PingID window...")
    time.sleep(3)  # Give extra time for window to fully load

    if not pingid.connect_to_pingid_window():
        print(" Failed to connect to PingID window")
        return

    # Print window information
    print("\n[3/3] Inspecting window controls...")
    print("=" * 60)
    pingid.print_window_info()
    print("=" * 60)

    print("\n Inspection complete!")
    print("\nLook for controls with these types:")
    print("  - Edit (for PIN input)")
    print("  - Button (for Next and Copy buttons)")
    print("\nUse the control identifiers to update pingid_automation.py")


if __name__ == "__main__":
    main()
