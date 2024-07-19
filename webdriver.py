import asyncio
from pyppeteer import launch
from fake_useragent import UserAgent
from config import HEADLESS, HEIGHT, WIDTH
from utils import find_chrome_path


def pyppeteerBrowserInit(loop):
    executable_path = find_chrome_path()
    print("executable_path", executable_path)
    print(f"window size: {WIDTH}x{HEIGHT}")
    user_agent = UserAgent().random
    print(f"Using user agent: {user_agent}")
    asyncio.set_event_loop(loop)
    try:
        browser = loop.run_until_complete(
            launch(
                executablePath=executable_path,
                headless=HEADLESS,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    f"--user-agent={user_agent}" "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu",
                    f"--window-size={WIDTH},{HEIGHT}",
                    "--start-maximized",
                    "--disable-notifications",
                    "--disable-popup-blocking",
                    "--ignore-certificate-errors",
                    "--allow-file-access",
                ],
            )
        )
        return browser, user_agent
    except Exception as e:
        # Print the error and return None if an exception occurs
        print(f"Error initializing browser: {e}")
        return None, None
