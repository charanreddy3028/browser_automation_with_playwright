import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()
email = os.getenv("GYANDHAN_EMAIL")
password = os.getenv("GYANDHAN_PASSWORD")

# Dummy data for application
dummy_data = {
    "program_name": "Smart",
    "requsted_loan_amount": 110762,
    "tenure": "30",
    "student_first_name": "KANAKALAKSHMI",
    "student_last_name": "NANDAMURI",
    "mobile_number": "9550471236",
    "student_email": "Kanakalakshminandamuri17@gmail.com",
    "applicant_dob": "1983-02-04",
    "pan_number": "AVOPN9285F",
    "zip_code": "521105"
}

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("🚀 Logging into GyanDhan...")
        await page.goto("https://nbfc.gyandhan.com/institute-employees/sign-in")
        await page.fill('input#institute_employee_email', email)
        await page.fill('input#institute_employee_password', password)
        await page.click('button[type="submit"]')
        await page.wait_for_selector("text=Dashboard")

        print("➕ Navigating to loan application page...")
        await page.click('a[href="/skill_training/institute_employees/loans/new"]')
        await page.wait_for_selector('#new_skill_training_loan')
        await page.screenshot(path="01_after_navigation.png")

        print("🎯 Selecting program name from dropdown...")
        try:
            await page.click('div[data-type="select-one"] div.choices__inner')
            await page.wait_for_selector('div.choices__list--dropdown.is-active')

            option_selector = f'div.choices__list--dropdown div.choices__item >> text={dummy_data["program_name"]}'
            if await page.query_selector(option_selector):
                await page.click(option_selector)
                print(f"✅ Program '{dummy_data['program_name']}' selected.")
            else:
                print(f"❌ Program '{dummy_data['program_name']}' not found!")
                await page.screenshot(path="02_program_not_found.png")
        except Exception as e:
            print(f"🔥 Error selecting program: {e}")
            await page.screenshot(path="02_program_selection_error.png")

        print("📝 Filling out loan form fields...")
        try:
            await page.fill('#skill_training_loan_amount_needed', str(dummy_data["requsted_loan_amount"]))
            await page.select_option('#skill_training_loan_tenure_requested_in_months', dummy_data["tenure"])
            await page.fill('#skill_training_loan_applicant_attributes_profile_attributes_first_name', dummy_data["student_first_name"])
            await page.fill('#skill_training_loan_applicant_attributes_profile_attributes_last_name', dummy_data["student_last_name"])
            await page.fill('#skill_training_loan_applicant_attributes_profile_attributes_mobile_number', dummy_data["mobile_number"])
            await page.fill('#skill_training_loan_applicant_attributes_email', dummy_data["student_email"])
            await page.fill('#skill_training_loan_applicant_attributes_profile_attributes_birth_date', dummy_data["applicant_dob"])
            await page.fill('#skill_training_loan_applicant_attributes_profile_attributes_pan_card_number', dummy_data["pan_number"])
            await page.fill('#skill_training_loan_applicant_attributes_current_address_attributes_address_attributes_zip_code', dummy_data["zip_code"])
        except Exception as e:
            print(f"⚠️ Error while filling form: {e}")
            await page.screenshot(path="03_form_fill_error.png")

        print("📡 Waiting for 'Create' button to become enabled...")
        try:
            await page.wait_for_selector('#submit_form:not([disabled])', timeout=10000)

            print("🚀 Submitting the application form...")
            # await page.click('#submit_form')
            # await page.wait_for_timeout(5000)
            # await page.screenshot(path="05_post_submission.png")
            print("✅ Application submitted.")
        except Exception as e:
            print(f"❌ Submit button error: {e}")
            await page.screenshot(path="04_submit_button_error.png")

        await browser.close()

asyncio.run(run())
