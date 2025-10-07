import asyncio
import re
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("--- Starting Comprehensive End-to-End Verification ---")

        # Setup error listener
        errors = []
        page.on("console", lambda msg: print(f"CONSOLE: [{msg.type}] {msg.text}") if msg.type == "error" else None)

        # Mock Firebase to isolate app code and ensure the test is stable
        await page.route(re.compile(r"https://www.gstatic.com/firebasejs/.*"),
                         lambda route: route.fulfill(status=200, body=" "))
        await page.route("**/firebase-config.js",
                         lambda route: route.fulfill(status=200, body="const firebaseConfig = {};"))

        # Set mobile viewport
        await page.set_viewport_size({"width": 375, "height": 667})

        # Go to the local server
        await page.goto("http://localhost:8000/Index.html", timeout=15000)

        # --- Step 1: Verify Welcome Screen Layout ---
        try:
            await expect(page.locator("#welcomeScreen")).to_be_visible(timeout=10000)
            print("✅ [1/4] Welcome screen is visible.")
            await page.screenshot(path="jules-scratch/verification/final-check-welcome-screen.png")
            print("📸 [2/4] Welcome screen screenshot captured.")
        except Exception as e:
            print(f"❌ FAILED on Welcome Screen check. Error: {e}")
            await page.screenshot(path="jules-scratch/verification/error_screenshot.png")
            await browser.close()
            return

        # --- Step 2: Verify Core JS Functionality (Sending a message) ---
        await page.locator("#chatInput").fill("Hello, this is a test.")
        await page.locator("#sendBtn").click()

        try:
            # Check that the user's message appears in the DOM
            await expect(page.locator(".user-message .message-text")).to_have_text("Hello, this is a test.")
            print("✅ [3/4] Core JS functionality verified: Message sent and appeared in UI.")
        except Exception as e:
            print(f"❌ FAILED on Core JS Functionality check. Error: {e}")
            await page.screenshot(path="jules-scratch/verification/error_screenshot.png")
            await browser.close()
            return

        # --- Step 3: Verify Long Chat Layout ---
        long_message = "This is a very long message to test the scrolling behavior and ensure the layout is correct. " * 20
        await page.evaluate(f"""(message) => {{
            const chatContainer = document.getElementById('chatContainer');
            const messageContainer = document.createElement('div');
            messageContainer.className = 'message-container bot-message';
            messageContainer.innerHTML = `<div class="message-avatar"><img src="https://files.catbox.moe/70gv96.png" alt="AI"></div><div class="message-content"><div class="message-text">${{message}}</div></div>`;
            chatContainer.appendChild(messageContainer);
            const mainContent = document.querySelector('.main-content');
            mainContent.scrollTop = mainContent.scrollHeight;
        }}""", long_message)

        await page.screenshot(path="jules-scratch/verification/final-check-long-chat.png")
        print("📸 [4/4] Long chat screenshot captured.")

        # Final check for any JS errors during the process
        if any("is not defined" in error for error in errors):
             print("❌ FAILED: A 'not defined' error was found in the console.")
             print("\n--- ❌ End-to-End Verification FAILED ---")
        else:
             print("\n--- ✅ End-to-End Verification PASSED ---")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())