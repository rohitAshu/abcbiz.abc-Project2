from datetime import datetime
import json
from config import *
from utils import is_valid_json, parse_json, print_the_output_statement, page_load
from webdriver import pyppeteerBrowserInit
from fake_useragent import UserAgent
from pyppeteer.errors import TimeoutError as PyppeteerTimeoutError
import asyncio
import pyppeteer
from pyppeteer_stealth import stealth
from utils import print_the_output_statement


async def abiotic_login(browser, user_agent, username, password, output_text):
    print("Login Processing.........................")
    page = await browser.newPage()  # type: ignore
    await stealth(page)
    await page.setViewport({"width": WIDTH, "height": HEIGHT})
    await page.setUserAgent(user_agent)
    Response = ""
    try:
        print_the_output_statement(output_text, f"Logging in to the website {LOGINURL}")
        load_page = await page_load(page, LOGINURL)
        if load_page:
            await asyncio.sleep(7)
            # Select the element using XPath
            element_404_error = await page.xpath(
                '//span[@style="margin-left: 450px; margin-top: 120px; font-size: 120px; color: rgb(122, 124, 125); font-weight: 900; display: inline; position: absolute;"]'
            )
            print(f"element_404_error  found: {element_404_error}")
            if element_404_error:
                text = "Internal Error Occurred while running application. Please Try Again!!"
                print(f"error {text}")
                return False, text, "", ""
            else:
                # Username Elements
                username_xpath = '//*[@id="username"]'
                await page.waitForXPath(username_xpath)
                username_element = await page.xpath(username_xpath)
                await username_element[0].type(username)
                print(f"Enter the username with type {username}")
                await asyncio.sleep(3)
                password_xpath = '//*[@id="password"]'
                await page.waitForXPath(password_xpath)
                password_element = await page.xpath(password_xpath)
                # await password_element[0].type('19MichaelBrewer68!')
                await password_element[0].type(password)
                print(f'Enter the password with secure password {"*" * len(password)}')
                await asyncio.sleep(3)
                login_button_xpath = '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/form/div[1]/button/span[1]'
                await page.waitForXPath(login_button_xpath)
                login_button_element = await page.xpath(login_button_xpath)
                await login_button_element[0].click()
                print("Clicked the login button...")
                await asyncio.sleep(7)
                popup_xpath = '//*[@role="alertdialog"]'
                popup_element = await page.xpath(popup_xpath)
                if popup_element:
                    popup_text = await (
                        await popup_element[0].getProperty("textContent")
                    ).jsonValue()
                    print("popup_text", popup_text)
                    return False, popup_text, "", ""
                else:
                    # Perform further actions after login (example: clicking a button)
                    target_button_xpath = '//*[@id="root"]/div/div[3]/div/div[2]/div[1]/h1/div[2]/div/button/span/span'
                    await page.waitForXPath(target_button_xpath)
                    target_button_element = await page.xpath(target_button_xpath)
                    await target_button_element[0].click()
                    await asyncio.sleep(5)
                    print("target_button_element element is clickwed")
                    target_element_xpath = '//*[@id="long-menu"]/div[2]/ul/li'
                    await page.waitForXPath(target_element_xpath)
                    target_element = await page.xpath(target_element_xpath)
                    await target_element[0].click()
                    await asyncio.sleep(10)
                    print("nexe button .....2")
                    Response = f"Login Successfully with username={username}"
                    return True, Response, browser, page
        else:
            text = (
                "Internal Error Occurred while running application. Please Try Again!!"
            )
            return False, text, "", ""
    except PyppeteerTimeoutError as timeout_error:
        print(f"timeout_error {timeout_error}")
    except pyppeteer.errors.NetworkError as NetworkError:
        print(f"NetworkError {NetworkError}")
    except Exception as e:
        # Handle exceptions gracefully
        print(f"Exception occurred during login: {e}")
        print_the_output_statement(output_text, f"Login Process Failed: {str(e)}")


async def scrapping_data(browser, page, json_data, output_text):
    print("scrapping_data")
    json_object = parse_json(json_data)
    Response = []

    try:
        for record in json_object:
            service_number = int(record["Server_ID"])
            last_name = record["Last_Name"]
            print("last_name", last_name)
            if service_number and last_name:
                print(
                    f"scrapping of the data {service_number} and last name {last_name}"
                )
                last_name_xpath = '//*[@id="lastName"]'
                await page.waitForXPath('//*[@id="serverId"]')
                await page.waitForXPath(last_name_xpath)
                server_id_element = await page.xpath('//*[@id="serverId"]')
                await server_id_element[0].type(str(service_number))
                last_name_element = await page.xpath(last_name_xpath)
                await last_name_element[0].type(last_name)
                # Click the search button
                search_button_xpath = '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div[2]/button[2]/span[1]'
                await page.waitForXPath(search_button_xpath)
                search_button_element = await page.xpath(search_button_xpath)
                await search_button_element[0].click()
                await asyncio.sleep(5)
                viewport_height = await page.evaluate("window.innerHeight")
                print("viewport_height element is found")
                scroll_distance = int(viewport_height * 0.2)
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
                    log_entry(
                        "ERROR",
                        service_number,
                        last_name,
                        f"No data found",
                    )
                    print(
                        f"There are no records by selected search parameters on the service_number {service_number} and last name {last_name}",
                    )

                else:
                    print(
                        f"data found on the {service_number}",
                    )
                    log_entry("INFO", service_number, last_name, "success")
                    print(
                        f"Getting data from table for {service_number } and {last_name}"
                    )
                    table_data = await page.evaluate(
                        """() => {
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
                                    }"""
                    )
                    if table_data:
                        table_data["reportDate"] = datetime.now().strftime("%Y-%m-%d")
                        table_data["lastName"] = (
                            last_name  # Replace with actual last name
                        )
                        Response.append(table_data)
                await page.waitForXPath(
                    '//button[contains(@class, "search-box-container_action-clear")]'
                )

                clear_button = await page.xpath(
                    '//button[contains(@class, "search-box-container_action-clear")]'
                )

                await clear_button[0].click()
            else:
                print("error")
    except PyppeteerTimeoutError as timeout_error:
        print(f"timeout_error {timeout_error}")
    except pyppeteer.errors.NetworkError as NetworkError:
        print(f"NetworkError {NetworkError}")
    except Exception as e:
        print(f"NetworkError {e}")
    finally:
        await browser.close()
    # print_the_output_statement(output_text, Response)
    return True, Response
