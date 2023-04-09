import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_bar_actions(driver):
    # Find the scrollable element
    scrollable_element = driver.find_element(By.XPATH, '//*[@id="inbox-scroll-content"]')

    # Get the current height of the scrollable element
    current_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

    # Keep scrolling until we have at least 25 conversations or we can't scroll anymore
    num_conversations = len(driver.find_elements(By.CSS_SELECTOR, "div[aria-label*='Conversation with ']"))
    while num_conversations < 100:
        # Scroll to the bottom of the element
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)

        # Wait for the element to load more conversations
        time.sleep(2)

        # Get the new height of the scrollable element
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

        # If we haven't scrolled, we can't scroll anymore, so break out of the loop
        if current_height == new_height:
            break

        # Update the current height to the new height
        current_height = new_height

        # Update the number of conversations
        num_conversations = len(driver.find_elements(By.CSS_SELECTOR, "div[aria-label*='Conversation with ']"))







def wait_for_new_conversations(driver, last_conversation_id, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, f"//*[@id='host-inbox-threads']/li[@data-threadid='{last_conversation_id}']/following-sibling::*"))
    )