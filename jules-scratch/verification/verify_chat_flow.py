import os
import json
from playwright.sync_api import sync_playwright, expect

def run_test(playwright):
    # Get the absolute path to the HTML file
    absolute_file_path = "file://" + os.path.abspath("Index.html")

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # --- Test 1: Guest User Experience ---
    print("\n--- Running Test 1: Guest User Experience ---")

    # Go to the local HTML file and ensure a clean state
    page.goto(absolute_file_path)
    page.evaluate("() => localStorage.clear()")
    page.reload()
    page.wait_for_load_state("domcontentloaded")
    print("Page loaded with cleared localStorage.")

    # Wait for the app to initialize by checking for the login button
    expect(page.locator("#user-profile-container .new-chat-btn")).to_be_visible(timeout=10000)
    print("App initialized in guest mode (Login button visible).")

    # Now that the app is ready, verify the welcome screen is visible
    expect(page.locator("#welcomeScreen")).to_be_visible()
    print("Welcome screen is visible.")

    # Send a message as a guest
    page.locator("#chatInput").fill("Hello as Guest")
    page.locator("#sendBtn").click()

    # Wait for bot response and then assert both messages
    expect(page.locator(".message-text").last).to_have_text("Ini adalah respons dari bot. Fungsionalitas API belum terhubung.", timeout=5000)
    expect(page.locator(".message-text").nth(-2)).to_have_text("Hello as Guest")
    print("Guest message sent and verified.")

    # Check that the conversation was saved to localStorage
    local_storage_data = page.evaluate("() => localStorage.getItem('sanepAI_userProfile')")
    assert local_storage_data is not None
    profile = json.loads(local_storage_data)
    assert "Hello as Guest" in profile['conversations'][list(profile['conversations'].keys())[0]]['messages'][0]['content']
    print("Guest conversation saved to localStorage.")

    # Reload the page
    page.reload()
    page.wait_for_load_state("domcontentloaded")

    # Verify that the chat history is loaded from localStorage
    expect(page.locator(".message-text").first).to_have_text("Hello as Guest")
    print("Guest chat history reloaded successfully from localStorage.")

    # Take a screenshot of the guest view
    page.screenshot(path="jules-scratch/verification/guest_chat_history.png")
    print("Screenshot 'guest_chat_history.png' taken.")

    # --- Test 2: Authentication Flow & Authenticated User Experience ---
    print("\n--- Running Test 2: Authenticated User Experience ---")

    # **THE DEFINITIVE FIX:** Intercept the firebase-config.js request
    # to prevent the real SDK from initializing and overwriting our mock.
    page.route("**/firebase-config.js", lambda route: route.fulfill(
        status=200,
        content_type="application/javascript",
        body="" # Provide an empty script
    ))
    print("Network interception for 'firebase-config.js' is active.")

    # Define a mock user and their data
    mock_user = {"uid": "mock-user-123", "displayName": "Jules"}
    mock_user_profile = {
        "name": "Jules",
        "email": "jules@example.com",
        "conversations": {
            "chat_firestore_1": {
                "id": "chat_firestore_1", "title": "Old Firestore Chat...", "timestamp": "2023-10-27T10:00:00.000Z",
                "messages": [{"role": "user", "content": "This is an old message from Firestore."}]
            }
        }
    }

    # Reload the page to ensure the network interception is applied
    page.reload()
    page.wait_for_load_state("domcontentloaded")

    # Now, inject the mock firestore object and simulate the login
    page.evaluate(
        """async (params) => {
            window.firestore = {
                collection: () => ({
                    doc: () => ({
                        set: () => Promise.resolve(true),
                    }),
                }),
            };
            window.currentUser = params.mock_user;
            window.userProfile = params.mock_user_profile;
            localStorage.removeItem('sanepAI_userProfile');
            await window.updateUserProfileUI(window.currentUser);
        }""",
        {"mock_user": mock_user, "mock_user_profile": mock_user_profile}
    )
    print("Injected mock firestore and simulated login.")

    # Verify the UI updated to the logged-in user's state
    expect(page.locator(".user-name").first).to_have_text("Jules")
    print("Sidebar UI updated to show logged-in user.")

    # Verify the chat history from the mocked "Firestore" data is displayed
    expect(page.locator(".message-text").first).to_have_text("This is an old message from Firestore.")
    print("Chat history from mocked Firestore data is displayed.")

    # Send a new message as the authenticated user
    page.locator("#chatInput").fill("A new message as a logged-in user")
    page.locator("#sendBtn").click()

    # Wait for the bot's response, then assert both messages are correct
    expect(page.locator(".message-text").last).to_have_text("Ini adalah respons dari bot. Fungsionalitas API belum terhubung.", timeout=5000)
    expect(page.locator(".message-text").nth(-2)).to_have_text("A new message as a logged-in user")
    print("New message from authenticated user is verified.")

    # Take a final screenshot
    page.screenshot(path="jules-scratch/verification/auth_chat_history.png")
    print("Screenshot 'auth_chat_history.png' taken.")

    # Close browser
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run_test(p)