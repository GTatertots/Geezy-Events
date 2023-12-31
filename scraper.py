from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pathlib import PurePath
import sqlite3
import addToLatLong

DB_FILE_NAME = PurePath("db", "events.db")

driver = webdriver.Chrome()

TEST = False

WEEKS_TO_SCRAPE = 2


def main():
    Events = []
    if TEST:
        return
    Events = StGeorgeWebsite(Events)
    Events = GreaterZionWebsite(Events)
    InsertEventsIntoDatabase(Events)
    print()

def InsertEventsIntoDatabase(Events):
    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    for event in Events:
        cur.execute("INSERT INTO events (title, date, start_time, end_time, location, description, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (event["title"], event["date"], event["start_time"], event["end_time"], event["location"], event["description"], event["latitude"], event["longitude"]))
    con.commit()

def GenerateEventObject(event_title, event_date, event_start_time, event_end_time, event_location, event_description, event_lat, event_long):
    event_object = {
        "title": event_title,
        "date": event_date,
        "start_time": event_start_time,
        "end_time": event_end_time,
        "location": event_location,
        "description": event_description,
        "latitude": event_lat,
        "longitude": event_long
    }
    return event_object

def StGeorgeWebsite(Events):
    driver.get("https://www.sgcity.org/eventcalendar/")
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
            event_start_time = CleanUpEventTime(event_start_time)
            print(event_start_time)
            event_end_time = time_text.split("-")[1].strip()
            event_end_time = CleanUpEventTime(event_end_time)
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
            event_lat, event_long = LatAndLong(event_location)
            print(event_lat, event_long)
            event_date_data = model_body.find_element(by=By.ID, value="viewDate").text.strip()
            event_date = event_date_data.split(" ")[1:4]
            event_date = " ".join(event_date)
            event_date = CleanUpEventDate(event_date)
            print(event_date)
            event_description = model_body.find_element(by=By.ID, value="viewDescription").text.strip()
            print(event_description)
            Events.append(GenerateEventObject(event_title, event_date, event_start_time, event_end_time, event_location, event_description, event_lat, event_long))
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

def GreaterZionWebsite(Events):
    driver.get("https://greaterzion.com/events/today/")
    time.sleep(1)
    for i in range(WEEKS_TO_SCRAPE * 7):
        events_web = driver.find_elements(by=By.CLASS_NAME, value="tribe-events-calendar-day__event")
        if len(events_web) == 0:
            next_button = driver.find_element(by=By.CLASS_NAME, value="tribe-common-c-btn-icon--caret-right")
            next_button.click()
            time.sleep(3)
            continue
        for event_web in events_web:
            event_date = event_web.find_element(by=By.CLASS_NAME, value="tribe-events-calendar-day__event-datetime")
            event_date = event_date.get_attribute("datetime")
            print(event_date)
            event_time = event_web.find_element(by=By.CLASS_NAME, value="tribe-event-date-start").text.strip()
            event_start_time = event_time.split(" ")
            event_start_time = event_start_time[-2:]
            event_start_time = "".join(event_start_time)
            event_start_time = CleanUpEventTime(event_start_time)
            print(event_start_time)
            event_end_time = event_web.find_element(by=By.CLASS_NAME, value="tribe-event-time").text.strip()
            event_end_time = event_end_time.replace(" ", "")
            event_end_time = CleanUpEventTime(event_end_time)
            print(event_end_time)
            event_title = event_web.find_element(by=By.CLASS_NAME, value="tribe-events-calendar-day__event-title-link").text.strip()
            print(event_title)
            event_venue = event_web.find_element(by=By.CLASS_NAME, value="tribe-events-calendar-day__event-venue-title").text.strip()
            event_address = event_web.find_element(by=By.CLASS_NAME, value="tribe-events-calendar-day__event-venue-address").text.strip() + ", UT"
            event_venue += " " + event_address
            print(event_venue)
            print(event_address)
            event_lat, event_long = LatAndLong(event_address)
            print(event_lat, event_long)
            event_description = event_web.find_element(by=By.CLASS_NAME, value="tribe-events-calendar-day__event-description")
            event_description = event_description.find_element(by=By.TAG_NAME, value="p").text.strip()
            print(event_description)
            Events.append(GenerateEventObject(event_title, event_date, event_start_time, event_end_time, event_venue, event_description, event_lat, event_long))
        next_button = driver.find_element(by=By.CLASS_NAME, value="tribe-common-c-btn-icon--caret-right")
        next_button.click()
        time.sleep(3)


        
    # print(len(events_web))
    return Events

def LatAndLong(location):
    location = CleanerEvent(location)
    lat, long = addToLatLong.getLatitudeLongitude(location)
    if lat is None and long is None:
        lat = 0
        long = 0
    return lat, long

def CleanerEvent(event_location):
    if ":" in event_location and not "kayenta" in event_location.lower():
        event_location = event_location.split(":")[1].strip()
    elif "kayenta" in event_location.lower():
        event_location = "881 Coyote Gulch Ct, Ivins, UT 84738"
    if "st. george" in event_location.lower():
        event_location = event_location.replace("st.", "Saint")
    if "st george" in event_location.lower():
        event_location = event_location.replace("st", "Saint")
    if not "ut" in event_location.lower() and not "utah" in event_location.lower():
        event_location += ", Saint George, UT"
    return event_location

def CleanUpEventTime(event_time):
    time_elements = event_time.split(" ")
    time = time_elements[0]
    time = time.lower()
    if time[-2] == "a" or time[:2] == "12":
        time = time[:-2]
    elif time[-2] == "p":
        time = time[:-2]
        time = time.split(":")
        time[0] = str(int(time[0]) + 12)
        time = ":".join(time)
    return time

def CleanUpEventDate(event_date):
    date_elements = event_date.split(" ")
    month = date_elements[0]
    month = month[:3]
    month = MonthToNumber(month)
    day = date_elements[1].strip(",")
    year = date_elements[2]
    return f"{year}-{month}-{day}"

def MonthToNumber(month):
    month = month.lower()
    if month == "jan":
        return "01"
    elif month == "feb":
        return "02"
    elif month == "mar":
        return "03"
    elif month == "apr":
        return "04"
    elif month == "may":
        return "05"
    elif month == "jun":
        return "06"
    elif month == "jul":
        return "07"
    elif month == "aug":
        return "08"
    elif month == "sep":
        return "09"
    elif month == "oct":
        return "10"
    elif month == "nov":
        return "11"
    elif month == "dec":
        return "12"
    else:
        return "00"


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