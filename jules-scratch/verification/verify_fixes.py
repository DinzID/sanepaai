import os
from playwright.sync_api import sync_playwright, expect

def run_verification(page):
    # Get the absolute path to the HTML file
    file_path = os.path.abspath('index.html')
    page.goto(f'file://{file_path}')

    # --- Verification 1: Admin Button Visibility ---
    # The "Edit Jadwal Pelajaran" button should be hidden by default for non-admin/logged-out users
    edit_schedule_btn_container = page.locator("#edit-schedule-btn-container")
    expect(edit_schedule_btn_container).to_be_hidden()
    print("✅ Verification 1 Passed: 'Edit Jadwal' button is hidden for guest users.")

    # --- Verification 2: Send Button State Management ---
    chat_input = page.locator("#chatInput")
    send_btn = page.locator("#sendBtn")
    image_upload_input = page.locator("#imageUploadInput")

    # Initial state: Button should be disabled
    expect(send_btn).to_be_disabled()
    print("✅ Verification 2.1 Passed: Send button is initially disabled.")

    # Type text: Button should be enabled
    chat_input.fill("Hello, world!")
    expect(send_btn).to_be_enabled()
    print("✅ Verification 2.2 Passed: Send button is enabled after typing text.")

    # Clear text: Button should be disabled
    chat_input.fill("")
    expect(send_btn).to_be_disabled()
    print("✅ Verification 2.3 Passed: Send button is disabled after clearing text.")

    # Upload image: Button should be enabled
    # Use the dummy file we created
    image_path = os.path.abspath('jules-scratch/verification/test.png')
    image_upload_input.set_input_files(image_path)
    expect(send_btn).to_be_enabled()
    print("✅ Verification 2.4 Passed: Send button is enabled after selecting an image.")

    # Remove image: Button should be disabled again
    remove_image_btn = page.locator(".media-preview-btn")
    remove_image_btn.click()
    expect(send_btn).to_be_disabled()
    print("✅ Verification 2.5 Passed: Send button is disabled after removing the image.")

    # --- Final Screenshot ---
    screenshot_path = "jules-scratch/verification/verification.png"
    page.screenshot(path=screenshot_path)
    print(f"📸 Screenshot taken and saved to {screenshot_path}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        run_verification(page)
    except Exception as e:
        print(f"❌ Verification failed: {e}")
    finally:
        browser.close()