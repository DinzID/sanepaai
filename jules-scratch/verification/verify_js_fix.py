import asyncio
import re
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("--- Verifying JavaScript Core Functionality ---")

        # We will collect all console errors
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        # Mock Firebase to isolate the app's JS and prevent external failures
        await page.route(re.compile(r"https://www.gstatic.com/firebasejs/.*"),
                         lambda route: route.fulfill(status=200, body=" "))
        await page.route("**/firebase-config.js",
                         lambda route: route.fulfill(status=200, body="const firebaseConfig = {};"))

        # Go to the local server
        await page.goto("http://localhost:8000/Index.html", timeout=15000)

        # The key verification: Does the chat container become visible?
        # This implies that the initial scripts, including loadChatHistory, ran without fatal errors.
        try:
            await expect(page.locator("#chatContainer")).to_be_visible(timeout=10000)
            print("✅ SUCCESS: The chat container is visible, indicating no fatal JS errors on startup.")
        except Exception as e:
            print(f"❌ FAILED: The chat container did not become visible. Error: {e}")
            await page.screenshot(path="jules-scratch/verification/js_fix_error.png")
            await browser.close()
            return

        # Check if the specific error we were trying to fix appeared
        specific_error_found = any("loadChatHistory is not defined" in error for error in errors)
        if specific_error_found:
            print("❌ FAILED: The error 'loadChatHistory is not defined' was found in the console.")
        else:
            print("✅ SUCCESS: The error 'loadChatHistory is not defined' was NOT found in the console.")

        await browser.close()

        # Final check
        if not specific_error_found:
            print("\n--- ✅ JavaScript Functionality Verification Passed ---")
        else:
            print("\n--- ❌ JavaScript Functionality Verification Failed ---")


if __name__ == "__main__":
    asyncio.run(main())