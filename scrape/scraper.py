from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

TEST = False

def main():
    if TEST:
        init_test()
        return
    print(StGeorgeWebsite())

def GenerateEventObject(event_title, event_date, event_start_time, event_end_time, event_location, event_description):
    event_object = {
        "title": event_title,
        "date": event_date,
        "start_time": event_start_time,
        "end_time": event_end_time,
        "location": event_location
    }
    if event_description != "":
        event_object["description"] = event_description
    return event_object

def StGeorgeWebsite():
    WEEKS_TO_SCRAPE = 12
    driver.get("https://www.sgcity.org/eventcalendar/")
    Events = []
    week_button_container = driver.find_elements(by=By.CLASS_NAME, value="fc-button-group")
    for possible_container in week_button_container:
        if possible_container.text == "MONTH\nWEEK\nDAY":
            week_button = possible_container
    week_button = week_button.find_element(by=By.CLASS_NAME, value="fc-listWeek-button")
    week_button.click()

    toolbar_container = driver.find_elements(by=By.CLASS_NAME, value="fc-toolbar")[1]
    next_button = toolbar_container.find_element(by=By.CLASS_NAME, value="fc-next-button")

    for i in range(WEEKS_TO_SCRAPE):
        
        if len(driver.find_elements(by=By.CLASS_NAME, value="fc-list-table")) < 2:
            next_button.click()
            time.sleep(1)
            continue
        fc_list_table = driver.find_elements(by=By.CLASS_NAME, value="fc-list-table")[1]
        fc_list_table = fc_list_table.find_element(by=By.TAG_NAME, value="tbody")
        event_containers = fc_list_table.find_elements(by=By.CLASS_NAME, value="fc-list-item")
        for event in event_containers:
            time_element = event.find_element(by=By.CLASS_NAME, value="fc-list-item-time")
            time_text = time_element.text.strip()
            event_start_time = time_text.split("-")[0].strip()
            print(event_start_time)
            event_end_time = time_text.split("-")[1].strip()
            print(event_end_time)
            clickable_title = event.find_element(by=By.CLASS_NAME, value="fc-list-item-title").find_element(by=By.TAG_NAME, value="a")
            event_title = clickable_title.text.strip()
            print(event_title)
            clickable_title.click() 
            time.sleep(1)
            model_container = driver.find_element(by=By.ID, value="view")
            model_header = model_container.find_element(by=By.CLASS_NAME, value="modal-header")
            model_body = model_container.find_element(by=By.CLASS_NAME, value="modal-body")
            event_location = model_body.find_element(by=By.ID, value="viewLocation").text.strip()
            print(event_location)
            event_date_data = model_body.find_element(by=By.ID, value="viewDate").text.strip()
            event_date = event_date_data.split(" ")[1:4]
            event_date = " ".join(event_date)
            print(event_date)
            event_description = model_body.find_element(by=By.ID, value="viewDescription").text.strip()
            print(event_description)
            Events.append(GenerateEventObject(event_title, event_date, event_start_time, event_end_time, event_location, event_description))
            exit_button = model_header.find_element(by=By.CLASS_NAME, value="close")
            exit_button.click()
            print("\n\n\n\n")
            time.sleep(1)
            # time.sleep(10)

        # actions = webdriver.ActionChains(driver).move_to_element(next_button).click(next_button).perform()
        next_button.click()
        time.sleep(1)
    print(i)
    time.sleep(10)
    return Events

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