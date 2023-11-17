from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

TEST = False

def main():
    if TEST:
        init_test()
        return
    StGeorgeWebsite()

def StGeorgeWebsite():
    driver.get("https://www.sgcity.org/eventcalendar/")
    week_button_container = driver.find_elements(by=By.CLASS_NAME, value="fc-button-group")
    for possible_container in week_button_container:
        if possible_container.text == "MONTH\nWEEK\nDAY":
            week_button = possible_container
    week_button = week_button.find_element(by=By.CLASS_NAME, value="fc-listWeek-button")
    week_button.click()
    fc_list_table = driver.find_elements(by=By.CLASS_NAME, value="fc-list-table")[1]
    fc_list_table = fc_list_table.find_element(by=By.TAG_NAME, value="tbody")
    event_containers = fc_list_table.find_elements(by=By.CLASS_NAME, value="fc-list-item")
    for event in event_containers:
        time_element = event.find_element(by=By.CLASS_NAME, value="fc-list-item-time")
        time_text = time_element.text
        event_start_time = time_text.split("-")[0].strip()
        event_end_time = time_text.split("-")[1].strip()
        clickable_title = event.find_element(by=By.CLASS_NAME, value="fc-list-item-title").find_element(by=By.TAG_NAME, value="a")
        event_title = clickable_title.text
        clickable_title.click() 
        model_body = driver.find_elements(by=By.CLASS_NAME, value="modal-body")
        print(len(model_body))
        for elm in model_body:
            temp = elm.find_elements(by.CLASS_NAME, value="viewLocation")
            print(len(temp))
            print("\n\n\n")
            print(elm.tag_name)
            print("\nTREE\n\n")
        # time.sleep(10)
        return

    # time.sleep(10)    

def init_test():
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    text = message.text

    time.sleep(10)

if __name__ == "__main__":
    main()

driver.quit()