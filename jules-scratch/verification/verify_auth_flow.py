import os
from playwright.sync_api import Page, expect

def test_auth_flow_and_admin_button(page: Page):
    """
    Verifies that the login modal appears and the admin button is hidden by default.
    """
    # 1. Arrange: Go to the local index.html file.
    # Get the absolute path to the file.
    file_path = os.path.abspath('index.html')
    page.goto(f"file://{file_path}")

    # 2. Act & Assert (Part 1): Check that the admin button is hidden for guests.
    # Open the settings menu to check for the button.
    settings_button = page.locator("#settings-menu-button")
    settings_button.click()

    # The "Edit Jadwal Pelajaran" button should NOT be visible.
    edit_schedule_btn = page.locator("#edit-schedule-btn")
    expect(edit_schedule_btn).not_to_be_visible()

    # Close the settings menu
    settings_button.click()

    # 3. Act & Assert (Part 2): Trigger and verify the login modal.
    # Click the user profile icon in the sidebar footer.
    user_profile_button = page.locator("#userProfile")
    user_profile_button.click()

    # The authentication modal should now be visible.
    auth_modal = page.locator("#auth-modal")
    expect(auth_modal).to_be_visible()

    # The modal title should be "Login" by default.
    modal_title = page.locator("#auth-modal-title")
    expect(modal_title).to_have_text("Login")

    # 4. Screenshot: Capture the final result for visual verification.
    page.screenshot(path="jules-scratch/verification/verification.png")