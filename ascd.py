import asyncio
import csv
import time
from fake_useragent import UserAgent
from pyppeteer.errors import TimeoutError as PyppeteerTimeoutError
from pyppeteer_stealth import stealth
from screeninfo import get_monitors

from utils import page_load
from webdriver import pyppeteerBrowserInit
import pyppeteer

LOGINURL = "https://abcbiz.abc.ca.gov/login"  # URL for licensing reports
HEADLESS = True  # Whether to run the app in headless mode (no GUI)
# Screen Resolution Settings
width = get_monitors()[0].width  # Width of the primary monitor
height = get_monitors()[0].height  # Height of the primary monitor


# Async function to automate tasks in the browser


async def main(service_number=None, last_name=None, username=None, password=None):
    # Initialize a new event loop
    start_time = time.time()
    loop = asyncio.new_event_loop()
    print("browser init")
    # Initialize the browser
    user_agent = UserAgent().random
    print(f"Using user agent: {user_agent}")
    browser = await pyppeteerBrowserInit(HEADLESS, width, height, user_agent)
    print("browser init completed")
    page = await browser.newPage() # type: ignore
    # Use stealth plugin to bypass bot detection
    await stealth(page)
    await page.setViewport({'width': width, 'height': height})
    await page.setUserAgent(user_agent)
    try:
        load_page = await page_load(page, LOGINURL)
        if load_page:
            print(f"Page loaded successfully")
            await asyncio.sleep(7)
            # Perform login
            username_xpath = '//*[@id="username"]'
            await page.waitForXPath(username_xpath)
            username_element = await page.xpath(username_xpath)
            print(f"username_element  found: {username_element}")
            await username_element[0].type(username)
            print(f"enter user name ..............! and type {username}")
            await asyncio.sleep(3)
            password_xpath = '//*[@id="password"]'
            await page.waitForXPath(password_xpath)
            password_element = await page.xpath(password_xpath)
            # await password_element[0].type('19MichaelBrewer68!')
            await password_element[0].type(password)
            print(f"enter password ........!")
            await asyncio.sleep(3)
            login_button_xpath = '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/form/div[1]/button/span[1]'
            await page.waitForXPath(login_button_xpath)
            login_button_element = await page.xpath(login_button_xpath)
            await login_button_element[0].click()
            print("Clicked the login button...")
            await asyncio.sleep(7)
            popup_xpath = '//*[@role="alertdialog"]'  # XPath for the popup message container
            popup_element = await page.xpath(popup_xpath)
            print('popup_element', popup_element)
            print("service id, service name", service_number, last_name)
            if popup_element:
                popup_text = await (await popup_element[0].getProperty('textContent')).jsonValue()
                print('Popup Message:', popup_text.strip())  # Print and handle the popup message text
            else:

                # Perform further actions after login (example: clicking a button)
                target_button_xpath = '//*[@id="root"]/div/div[3]/div/div[2]/div[1]/h1/div[2]/div/button/span/span'
                await page.waitForXPath(target_button_xpath)
                target_button_element = await page.xpath(target_button_xpath)
                await target_button_element[0].click()
                await asyncio.sleep(5)
                print("nexe button .....1")
                target_element_xpath = '//*[@id="long-menu"]/div[2]/ul/li'
                await page.waitForXPath(target_element_xpath)
                target_element = await page.xpath(target_element_xpath)
                await target_element[0].click()
                await asyncio.sleep(15)
                print("nexe button .....2")
                await asyncio.sleep(15)
                if service_number and last_name:
                    last_name_xpath = '//*[@id="lastName"]'
                    await page.waitForXPath('//*[@id="serverId"]')
                    await page.waitForXPath(last_name_xpath)
                    server_id_element = await page.xpath('//*[@id="serverId"]')
                    print('server_id_element', server_id_element)
                    await server_id_element[0].type(service_number)
                    print(f"enter the service id...........!  {service_number}")
                    last_name_element = await page.xpath(last_name_xpath)
                    print('last_name_element', last_name_element)
                    await last_name_element[0].type(last_name)
                    print(f"enter the full name ...........! {last_name}")
                    # Click the search button
                    search_button_xpath = '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div[2]/button[2]/span[1]'
                    await page.waitForXPath(search_button_xpath)
                    search_button_element = await page.xpath(search_button_xpath)
                    print('search_button_element', search_button_element)
                    await search_button_element[0].click()
                    print('search_button_element is clicked ')
                    await asyncio.sleep(5)
                    viewport_height = await page.evaluate("window.innerHeight")
                    print("viewport_height element is found")
                    scroll_distance = int(viewport_height * 0.2)
                    print(f"scroll_distance is  {scroll_distance}")
                    await page.evaluate(f"window.scrollBy(0, {scroll_distance})")
                    print(f"scroll_distance progress")
                    check_script = """
                        () => {
                            const div = document.querySelector('div.sc-gAnuJb.gzDMq');
                            if (div) {
                                const pElement = div.querySelector('p');
                                if (pElement && pElement.textContent.trim() === 'There are no records by selected search parameters') {
                                    return true;
                                }
                            }
                            return false;
                        }
                    """
                    element_exists = await page.evaluate(check_script)
                    if element_exists:
                        print('There are no records by selected search parameters')
                    else:
                        table_data = await page.evaluate('''() => {
                                        const nameElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div > p > span');
                                        const serviceElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > p');
                                        const trainingElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(3) > div > div > p');
                                        const statusElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(4) > div > div > p');
                                        const expireDateElement = document.querySelector('#root > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > div > div:nth-child(1) > div > div:nth-child(5) > div > div > p');

                                        return {
                                            name: nameElement ? nameElement.innerText.trim() : '',
                                            service: serviceElement ? serviceElement.innerText.trim() : '',
                                            training: trainingElement ? trainingElement.innerText.trim() : '',
                                            status: statusElement ? statusElement.innerText.trim() : '',
                                            expirationDate: expireDateElement ? expireDateElement.innerText.trim() : ''
                                        };
                                    }''')
                        csv_filename = 'table_data.csv'
                        csv_headers = table_data
                        with open(csv_filename, mode='w', newline='') as csv_file:
                            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                            writer.writeheader()
                            writer.writerow(table_data)

                        print(f"Data has been extracted and saved to {csv_filename}")

                        await asyncio.sleep(9)
                else:
                    print('Please enter the vaid service number nad last name  ')
    except PyppeteerTimeoutError as timeout_error:
        print(f'timeout_error {timeout_error}')
    except pyppeteer.errors.NetworkError as NetworkError:
        print(f'NetworkError {NetworkError}')
    except Exception as e:
        print(f'NetworkError {e}')
    finally:
        await browser.close()
        end_time = time.time()
        total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
