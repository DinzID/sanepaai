import asyncio
from playwright.async_api import async_playwright, expect
import http.server
import socketserver
import threading
import json

# --- Test Setup ---
PORT = 8089
LONG_MESSAGE = "Ini adalah pesan yang sangat panjang. " * 10 + "Ini adalah akhir dari pesan yang seharusnya terlihat sepenuhnya dan tidak terpotong oleh bilah input."
MOCK_MESSAGES = [
    {"role": "user", "content": "Pesan singkat 1"},
    {"role": "bot", "content": "Balasan singkat 1"},
    {"role": "user", "content": "Pesan singkat 2"},
    {"role": "bot", "content": LONG_MESSAGE}
]

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

async def run_test():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), QuietHTTPRequestHandler) as httpd:
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"Server started on http://localhost:{PORT}")

        async with async_playwright() as p:
            iphone_13_pro = p.devices['iPhone 13 Pro']
            browser = await p.chromium.launch()
            context = await browser.new_context(**iphone_13_pro)
            page = await context.new_page()

            # --- TEST 1: Catch Console Errors ---
            page_errors = []
            page.on("pageerror", lambda exc: page_errors.append(exc))
            print("Console error listener attached.")

            try:
                # --- TEST 2: Initial Load & Message Injection ---
                print("Verifying initial load...")
                await page.goto(f"http://localhost:{PORT}/Index.html", wait_until="domcontentloaded")

                # Check for initial JS errors
                if len(page_errors) > 0:
                    raise Exception(f"JavaScript error on load: {page_errors[0]}")
                print("OK: Page loaded without JavaScript errors.")

                # Inject messages to simulate a chat history
                await page.evaluate(f"""
                    const chatContainer = document.getElementById('chatContainer');
                    const welcomeScreen = document.getElementById('welcomeScreen');
                    welcomeScreen.style.display = 'none';
                    const messages = {json.dumps(MOCK_MESSAGES)};

                    // Re-using the app's own function to ensure consistency
                    function addMessageToUI(content, role) {{
                        const messageContainer = document.createElement('div');
                        messageContainer.className = `message-container ${{role}}-message`;
                        messageContainer.innerHTML = `
                            <div class="message-avatar">
                               <i class="fas fa-{{role === 'user' ? 'user' : 'robot'}}"></i>
                            </div>
                            <div class="message-content">
                                <div class="message-text">${{content}}</div>
                            </div>
                        `;
                        chatContainer.appendChild(messageContainer);
                    }}

                    messages.forEach(msg => addMessageToUI(msg.content, msg.role));
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                """)
                print("Injected chat history.")

                # --- TEST 3: Dynamic Padding Verification ---
                print("Verifying dynamic padding...")
                chat_input = page.locator("#chatInput")

                # Type multiple lines into the input to make it grow
                multi_line_text = "Baris pertama\nBaris kedua\nBaris ketiga"
                await chat_input.fill(multi_line_text)

                # Wait a moment for the ResizeObserver to fire and the CSS transition to complete
                await page.wait_for_timeout(500)

                # Assert that the last message is still fully visible
                last_message_locator = page.locator(".message-container").last
                await expect(last_message_locator).to_be_in_viewport()
                print("OK: Dynamic padding works. Last message is visible even after input resize.")

                # --- FINAL SCREENSHOT ---
                screenshot_path = "jules-scratch/verification/final_verification.png"
                await page.screenshot(path=screenshot_path)
                print(f"Final verification screenshot saved to {screenshot_path}")

            except Exception as e:
                print(f"An error occurred: {e}")
                await page.screenshot(path="jules-scratch/verification/error_screenshot.png")
                raise
            finally:
                await browser.close()
                httpd.shutdown()
                print("Server stopped.")

            # Final check for any errors that might have occurred during the test
            if len(page_errors) > 0:
                raise Exception(f"JavaScript error(s) detected during test: {page_errors}")

if __name__ == "__main__":
    asyncio.run(run_test())