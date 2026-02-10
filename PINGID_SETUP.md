# PingID Automation Setup Guide

This guide explains how to set up and use the PingID MFA automation for your Fileroom login tests.

## Overview

The PingID automation handles the complete MFA flow:
1. Launches PingID.exe
2. Enters your PIN
3. Clicks Next button
4. Copies the MFA code
5. Returns to browser and pastes the code
6. Clicks Sign On button

## Prerequisites

- Windows OS (PingID.exe is a Windows application)
- Python 3.8 or higher
- PingID desktop application installed

## Installation Steps

### 1. Install Required Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `playwright` - Browser automation
- `pytest` - Testing framework
- `allure-pytest` - Test reporting
- `pywinauto` - Desktop automation for PingID
- `pyperclip` - Clipboard handling

### 2. Configure PingID Settings

Edit [config.py](config.py) and update the following:

```python
PINGID_CONFIG = {
    "exe_path": r"C:\Program Files\PingID\PingID.exe",  # Update to your actual path
    "pin": "1234",  # Update with your actual PIN
    "wait_timeout": 10
}
```

**Important:**
- Replace `exe_path` with the actual location of your PingID.exe
- Replace `pin` with your actual PingID PIN
- Keep this file secure and don't commit it to version control

### 3. Test PingID Automation Separately

Before running the full test, verify PingID automation works:

```bash
python pingid_automation.py
```

This will:
- Launch PingID
- Enter your PIN
- Retrieve the MFA code
- Print the code to console

### 4. Debug PingID Window (If Needed)

If the automation fails to find the PIN input or buttons, run the debug script:

```bash
python debug_pingid.py
```

This will display all controls in the PingID window, helping you identify the correct control names.

## Usage

### Running the Full Test

```bash
pytest FileroomLogin.py -v
```

With Allure reporting:

```bash
pytest FileroomLogin.py --alluredir=./allure-results
allure serve ./allure-results
```

### Test Flow

The test now includes PingID MFA automation at [FileroomLogin.py:44-72](FileroomLogin.py#L44-L72):

1. Navigate to application
2. Enter credentials
3. Click Sign On
4. **[NEW] Automate PingID MFA**
   - Launch PingID.exe
   - Enter PIN
   - Copy MFA code
   - Paste in browser
   - Click Sign On
5. Select domain
6. Verify successful login

## Troubleshooting

### Issue: PingID window not found

**Solution:** Check if:
- PingID.exe path in config.py is correct
- PingID window appears after launching
- Run `debug_pingid.py` to see available windows

### Issue: PIN input or buttons not found

**Solution:**
1. Run `debug_pingid.py` to inspect controls
2. Update control identifiers in [pingid_automation.py](pingid_automation.py)
3. Look for the control names in the debug output
4. Update these sections:
   - PIN input: Line ~56-74
   - Next button: Line ~77-93
   - Copy button: Line ~96-112

### Issue: MFA code not copied

**Solution:**
- Ensure the Copy button is clicked successfully
- Check if clipboard permissions are granted
- Verify pyperclip is installed correctly

### Issue: Browser can't find passcode input

**Solution:**
- Verify the CSS selector `.passcode-input` is correct
- Check if the element has a different class name
- Inspect the browser element and update the locator in [FileroomLogin.py:61](FileroomLogin.py#L61)

## Security Notes

⚠️ **Important Security Considerations:**

1. **config.py contains sensitive data** (PIN)
   - Add `config.py` to `.gitignore`
   - Never commit credentials to version control

2. **Alternative: Use Environment Variables**
   ```python
   import os
   PINGID_CONFIG = {
       "pin": os.getenv("PINGID_PIN", ""),
   }
   ```

3. **Best Practice: Use a secrets manager**
   - Azure Key Vault
   - AWS Secrets Manager
   - HashiCorp Vault

## File Structure

```
PlawrightPythonTraining/
├── FileroomLogin.py          # Main test file (updated with PingID automation)
├── pingid_automation.py      # PingID automation module
├── config.py                 # Configuration (PIN, exe path)
├── debug_pingid.py          # Debug tool for PingID window inspection
├── requirements.txt          # Python dependencies
└── PINGID_SETUP.md          # This file
```

## Advanced Usage

### Custom Timeout

```python
from pingid_automation import PingIDAutomation

pingid = PingIDAutomation(timeout=20)  # 20 seconds timeout
code = pingid.get_mfa_code()
```

### Using Different PIN

```python
from pingid_automation import PingIDAutomation

pingid = PingIDAutomation(pin="5678")
code = pingid.get_mfa_code()
```

## Support

If you encounter issues:
1. Run `debug_pingid.py` to inspect window controls
2. Check the console output for error messages
3. Verify all configuration values in `config.py`
4. Ensure all dependencies are installed

## Future Enhancements

Potential improvements:
- Support for different PingID versions
- Automatic PIN retrieval from secure vault
- Screenshot capture on failure
- Retry logic for flaky controls
- Support for other MFA applications
