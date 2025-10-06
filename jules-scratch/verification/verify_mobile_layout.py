import os
from playwright.sync_api import sync_playwright, expect

def run_mobile_test(playwright):
    # Get the absolute path to the HTML file
    absolute_file_path = "file://" + os.path.abspath("Index.html")

    # Define a mobile viewport (e.g., iPhone 12)
    iphone_12_viewport = {"width": 390, "height": 844}

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        viewport=iphone_12_viewport,
        is_mobile=True,
        device_scale_factor=3
    )
    page = context.new_page()

    print("--- Running Mobile Layout Verification Test ---")

    # Go to the local HTML file
    page.goto(absolute_file_path)
    page.wait_for_load_state("domcontentloaded")
    print("Page loaded in mobile viewport.")

    # Inject a large number of messages to ensure the content overflows
    page.evaluate("""() => {
        const chatContainer = document.getElementById('chatContainer');
        for (let i = 0; i < 20; i++) {
            const role = i % 2 === 0 ? 'user' : 'bot';
            const content = `This is message number ${i + 1} to test scrolling.`;
            addMessageToUI(content, role);
        }
    }""")
    print("Injected 20 messages to make the page scrollable.")

    # Verify that the last message is visible by scrolling down
    page.locator(".message-container").last.scroll_into_view_if_needed()
    expect(page.locator(".message-container").last).to_be_visible()
    print("Scrolled to the last message.")

    # Most importantly, verify that the input container at the bottom is visible
    expect(page.locator(".input-container")).to_be_visible()
    print("Input container is visible at the bottom of the screen.")

    # Take a screenshot to visually confirm the layout is correct
    screenshot_path = "jules-scratch/verification/mobile_layout_fix.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

    # Close browser
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run_mobile_test(p)