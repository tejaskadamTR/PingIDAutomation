# PingID Automation

Automation scripts for PingID MFA authentication with Playwright tests.

## Files

- **pingid_automation.py** - Core automation module for handling PingID MFA
- **inspect_pingid.py** - Utility for inspecting PingID application elements
- **FileroomLogin.py** - Playwright test for Fileroom login with PingID MFA

## Setup

1. Clone this repository
2. Copy `config.example.py` to `config.py`
3. Update `config.py` with your credentials and settings:
   - PingID executable path
   - PingID PIN
   - SSO credentials (email, employee ID, password)
4. Install dependencies:
   ```bash
   pip install playwright pytest pytest-playwright allure-pytest pywinauto
   ```

## Configuration

The `config.py` file (not tracked in git) should contain:

```python
# PingID Configuration
PINGID_CONFIG = {
    "exe_path": r"C:\Program Files (x86)\Ping Identity\PingID\PingID.exe",
    "pin": "YOUR_PIN_HERE",
    "wait_timeout": 10
}

# SSO Credentials
SSO_CREDENTIALS = {
    "email": "YOUR_EMAIL@DOMAIN.COM",
    "employee_id": "YOUR_EMPLOYEE_ID",
    "password": "YOUR_PASSWORD"
}

# Browser Configuration
BROWSER_CONFIG = {
    "headless": False,
    "slow_mo": 500
}
```

## Usage

Run the Fileroom login test:
```bash
pytest FileroomLogin.py --headed
```

Run with Allure reporting:
```bash
pytest FileroomLogin.py --headed --alluredir=allure-results
allure serve allure-results
```

## Security

⚠️ **Important**: Never commit `config.py` to version control as it contains sensitive credentials.
