import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        file_path = os.path.abspath('index.html')
        await page.goto(f'file://{file_path}')

        # --- 1. Test Registration and Login ---
        print("Testing user registration...")

        import time
        timestamp = int(time.time())
        test_email = f"testuser{timestamp}@example.com"
        test_password = "password123"

        # Click the main button to open the authentication modal
        await page.get_by_role("button", name="Login & Daftar").click()
        await expect(page.locator("#auth-modal")).to_be_visible()

        # Fill in the registration form
        await page.locator("#auth-email").fill(test_email)
        await page.locator("#auth-password").fill(test_password)

        # Click the 'Daftar' (Register) button using its unique ID
        await page.locator("#register-btn").click()

        # First, wait for the modal to disappear, which signals a successful registration submission
        await expect(page.locator("#auth-modal")).not_to_be_visible(timeout=10000)

        # Then, assert that the user profile becomes visible, confirming successful registration and login
        user_profile_info = page.locator("#user-profile-info")
        await expect(user_profile_info).to_be_visible(timeout=10000)

        # Assert that the correct username is displayed
        await expect(user_profile_info.get_by_text(f"testuser{timestamp}")).to_be_visible()

        await page.screenshot(path="jules-scratch/verification/01_registration_success.png")
        print("Screenshot 1: Registration and login successful.")

        # --- 2. Test Chat Functionality ---
        print("Testing chat functionality...")
        chat_input = page.locator("#chatInput")
        test_message = "Halo, ini adalah pesan tes."
        await chat_input.fill(test_message)
        await page.locator("#sendBtn").click()

        # Wait for the user's message to appear in the chat container
        await expect(page.locator(".chat-container")).to_contain_text(test_message)

        # Wait for the bot's typing indicator and then its response
        await expect(page.locator("#typing-indicator")).to_be_visible(timeout=5000)
        print("Typing indicator appeared...")
        await expect(page.locator("#typing-indicator")).not_to_be_visible(timeout=30000) # Wait for response
        print("Bot responded.")

        # Verify there are now at least two messages (user's and bot's)
        message_containers = page.locator(".message-container")
        await expect(message_containers).to_have_count(2, timeout=5000)

        await page.screenshot(path="jules-scratch/verification/02_chat_works.png")
        print("Screenshot 2: Chat message sent and response received")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())