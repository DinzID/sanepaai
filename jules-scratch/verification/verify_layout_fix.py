import asyncio
import re
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Mock Firebase SDKs to prevent them from running and interfering.
        # This allows testing the app's own JS and layout in isolation.
        # This is crucial because the repo is missing the actual firebase-config.js
        await page.route(re.compile(r"https://www.gstatic.com/firebasejs/.*"),
                         lambda route: route.fulfill(status=200, body=" "))
        await page.route("**/firebase-config.js",
                         lambda route: route.fulfill(status=200, body="const firebaseConfig = {};"))


        # Listen for any console events and print them
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))

        # Set a mobile viewport
        await page.set_viewport_size({"width": 375, "height": 667})

        # Go to the local server, explicitly requesting Index.html
        # The simple python server is case-sensitive.
        await page.goto("http://localhost:8000/Index.html", timeout=10000)

        # The app should now initialize correctly.
        # We'll wait for the chat container to be visible.
        try:
            await expect(page.locator("#chatContainer")).to_be_visible(timeout=10000)
            print("✅ Chat container is visible.")
        except Exception as e:
            print(f"FATAL: Error waiting for #chatContainer: {e}")
            await page.screenshot(path="jules-scratch/verification/error_screenshot.png")
            await browser.close()
            return

        # Inject a very long message from the AI to simulate the bug
        long_message = "This is a very long message to test the scrolling behavior. " * 20
        await page.evaluate(f"""() => {{
            const chatContainer = document.getElementById('chatContainer');
            const messageContainer = document.createElement('div');
            messageContainer.classList.add('message-container', 'bot-message'); // Using bot-message for styling

            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.innerHTML = '<img src="https://files.catbox.moe/70gv96.png" alt="AI" style="width:20px;height:20px;">';

            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.innerHTML = `<div class="message-text">{long_message}</div>`;

            messageContainer.appendChild(avatar);
            messageContainer.appendChild(messageContent);
            chatContainer.appendChild(messageContainer);

            // Scroll to the bottom to see the effect
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }}""")
        print("✅ Injected long message and scrolled to bottom.")

        # The input bar should be visible at the bottom and not obscure the text
        await expect(page.locator(".input-container")).to_be_visible()
        print("✅ Input container is visible.")

        # Take a screenshot to verify the fix
        await page.screenshot(path="jules-scratch/verification/mobile-layout-fix-final.png")
        print("📸 Screenshot captured.")

        await browser.close()
        print("✅ Verification script completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())