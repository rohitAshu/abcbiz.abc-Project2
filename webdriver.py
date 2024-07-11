import asyncio
from pyppeteer import launch

from utils import find_chrome_path


async def pyppeteerBrowserInit(headless, width, height, user_agent):
    """
    initializes a Pyppeteer browser instance with the specified parameters.

    Args:
        loop (asyncio.AbstractEventLoop): The event loop to use for asynchronous operations.
        headless (bool): Whether to run the browser in headless mode.
        width (int): The width of the browser window.
        height (int): The height of the browser window.

    Returns:
        browser (pyppeteer.browser.Browser or None): The initialized browser instance, or None if an error occurred.
        :param height:
        :param width:
        :param headless:
        :param user_agent:
    """
    # Find the path to the Chrome executable
    executable_path = find_chrome_path()
    print("executable_path", executable_path)
    print(f"window size: {width}x{height}")
    try:
        # Launch the browser with the specified arguments
        browser = await launch(executablePath=executable_path, headless=headless, args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars",
            f'--user-agent={user_agent}'
            "--disable-dev-shm-usage",
            "--disable-accelerated-2d-canvas",
            "--disable-gpu",
            f"--window-size={width},{height}",
            "--start-maximized",
            "--disable-notifications",
            "--disable-popup-blocking",
            "--ignore-certificate-errors",
            "--allow-file-access",
        ])
        return browser
    except Exception as e:
        # Print the error and return None if an exception occurs
        print(f"Error initializing browser: {e}")
        return None
