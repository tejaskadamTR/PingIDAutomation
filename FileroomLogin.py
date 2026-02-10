from playwright.sync_api import Page, expect
import pytest
import allure
from pingid_automation import automate_pingid_mfa
from config import SSO_CREDENTIALS

@pytest.mark.smoke
@allure.feature('Authentication')
@allure.story('Fileroom Login')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Verify successful login to Fileroom application')
@allure.description('Test validates the complete login flow for Fileroom including SSO authentication and domain selection')
@allure.tag('smoke', 'authentication', 'fileroom')
def test_fileroomLogin(page: Page):
    """Test Fileroom login functionality with SSO"""

    with allure.step("Navigate to Fileroom production URL"):
        page.goto("https://production.sureprep.com/")
        allure.attach(page.url, name="Initial URL", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Click Continue button"):
        page.locator(".Cont-Btn").click()

    with allure.step("Enter email for SSO authentication"):
        page.locator("#username").fill(SSO_CREDENTIALS["email"])
        allure.attach(SSO_CREDENTIALS["email"],
                     name="Email Entered",
                     attachment_type=allure.attachment_type.TEXT)

    with allure.step("Submit email and proceed to credentials page"):
        page.locator("._button-login-id").click()

    with allure.step("Enter employee ID"):
        page.locator("#username").fill(SSO_CREDENTIALS["employee_id"])
        allure.attach(SSO_CREDENTIALS["employee_id"], name="Employee ID", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Enter password"):
        page.locator("#password").fill(SSO_CREDENTIALS["password"])

    with allure.step("Check 'Remember username' option"):
        page.locator(".remember-username").check()

    with allure.step("Click Sign On button"):
        page.wait_for_timeout(1000)  # Wait 1 second
        page.locator("#signOnButton").click(force=True)

    with allure.step("Handle PingID MFA authentication"):
        # Launch PingID.exe and get MFA code
        allure.attach("Launching PingID application",
                     name="PingID Status",
                     attachment_type=allure.attachment_type.TEXT)

        mfa_code = automate_pingid_mfa()

        if mfa_code:
            allure.attach(f"Retrieved MFA code: {mfa_code}",
                         name="MFA Code Retrieved",
                         attachment_type=allure.attachment_type.TEXT)

            # Wait for passcode input to be visible
            page.locator(".passcode-input").wait_for(state="visible", timeout=30000)

            # Paste the MFA code in the browser
            page.locator(".passcode-input").fill(mfa_code)
            allure.attach("MFA code entered in browser",
                         name="Browser Input",
                         attachment_type=allure.attachment_type.TEXT)

            # Click Sign On button
            page.locator("input[value='Sign On']").click()
            allure.attach("Clicked Sign On button after MFA",
                         name="Sign On Action",
                         attachment_type=allure.attachment_type.TEXT)
        else:
            raise Exception("Failed to retrieve MFA code from PingID")

    with allure.step("Select domain: Automation-01"):
        page.select_option("#SelectedDomainID", value="Automation-01")
        allure.attach("Automation-01", name="Selected Domain", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Submit domain selection"):
        page.locator("#btnSubmit").click()

    with allure.step("Verify successful navigation to Fileroom Listing page"):
        expect(page).to_have_url("https://production.sureprep.com/Fileroom/Fileroom/Listing")
        allure.attach(page.url, name="Final URL", attachment_type=allure.attachment_type.TEXT)

        # Take screenshot for visual confirmation
        screenshot = page.screenshot()
        allure.attach(screenshot,
                     name="Fileroom Listing Page",
                     attachment_type=allure.attachment_type.PNG)