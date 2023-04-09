from message_parser import parse_messages
from driver_funcs import *
from file_funcs import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import time

def scrape_airbnb(output_format):
    # Get login information from user
    username = input("Enter your Airbnb username: ")
    password = getpass.getpass("Enter your Airbnb password: ")

    # Set up Chrome webdriver
    driver = webdriver.Chrome()
    page_url = "https://www.airbnb.com/hosting/inbox/folder/"

    # Log in to Airbnb
    # Enter your username and password in the fields below
    driver.get("https://www.airbnb.com/login")  # Navigate to the login page

    # Click the "Continue with email" button
    continue_with_email_button = driver.find_element(By.XPATH, "//button[@data-testid='social-auth-button-email']")
    continue_with_email_button.click()

    # Wait for the email input to appear
    driver.implicitly_wait(5)

    username_input = driver.find_element(By.XPATH, "//input[@data-testid='email-login-email']")
    username_input.send_keys(username)
    continue_button_click = driver.find_element(By.XPATH, "//button[@data-testid='signup-login-submit-btn']")
    continue_button_click.click()
    password_input = driver.find_element(By.XPATH, "//input[@data-testid='email-signup-password']")
    password_input.send_keys(password)
    continue_button_click = driver.find_element(By.XPATH, "//button[@data-testid='signup-login-submit-btn']")
    continue_button_click.click()

    # Wait for the page to load
    time.sleep(5)

    driver.get(page_url)  # Navigate to the messages page after logging in
    html = driver.page_source

    # Wait for the messages to load on the page
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label*='Conversation with ']")))

    # Initialize variables
    num_conversations = 0
    conversation_xpath = '//*[@id="host-inbox-threads"]/li'

    # Scroll to load a bunch of conversations
    scroll_bar_actions(driver)

    # Wait for all conversations to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, conversation_xpath)))

    # Get all the conversation elements
    conversations = driver.find_elements(By.XPATH, conversation_xpath)

    for index, conversation in enumerate(conversations):
        # only get guests that we are planning to host, have hosted, or are currently hosting
        status_span = conversation.find_element(By.XPATH, './/div[2]//span[1]')
        status_text = status_span.text

        if status_text not in ['Confirmed', 'Currently hosting', 'Past guest']:
            continue
        a_element = conversation.find_element(By.XPATH, f'//*[@id="host-inbox-threads"]/li[{index+1}]/div/a')
        cid = a_element.get_attribute("data-threadid")

        # Click on the conversation to load the messages
        conversation.click()
        time.sleep(2)

        # Extract messages and parse them
        messages_elements = driver.find_elements(By.CSS_SELECTOR, "div[aria-label*=' sent']")
        raw_messages = [message.get_attribute("aria-label") for message in messages_elements]
        raw_messages_string = "\n".join(raw_messages)
        messages = parse_messages(raw_messages_string, cid)

        # write to csv what we have so far
        if output_format == 'csv':
            write_messages_to_csv(messages)
        else:
            # write to json for openai model what we have so far
            write_messages_to_openai_format_json(messages)

