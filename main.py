import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time

# ---------------------------------------------------------------------------- #
#                                   SSO LOGIN                                  #
# ---------------------------------------------------------------------------- #

driver = webdriver.Chrome()
driver.get("https://moodle.hm.edu/hmsso")

load_dotenv()

if os.getenv("SSO_USERNAME") is None or os.getenv("SSO_PASSWORD") is None:
    raise ValueError("SSO_USERNAME or SSO_PASSWORD environment variable not set")

driver.find_element(By.ID, "username").send_keys(os.getenv("SSO_USERNAME"))
driver.find_element(By.ID, "password").send_keys(os.getenv("SSO_PASSWORD"))
driver.find_element(By.NAME, "_eventId_proceed").click()

# ---------------------------------------------------------------------------- #
#                              COURSES ID SCRAPING                             #
# ---------------------------------------------------------------------------- #

driver.get("https://moodle.hm.edu/my/courses.php")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list-group"))
)
time.sleep(1)

course_list = driver.find_element(By.CSS_SELECTOR, "ul.list-group")
courses = course_list.find_elements(By.CLASS_NAME, "list-group-item")
course_ids = []
for course in courses:
    course_id = course.get_attribute("data-course-id")
    course_ids.append(course_id)
    print(course_id)
print("Found " + str(len(course_ids)) + " courses")

# ---------------------------------------------------------------------------- #
#                      COURSE PDF SCRAPING and DOWNLOADING                     #
# ---------------------------------------------------------------------------- #

for course_id in course_ids:
    driver.get("https://moodle.hm.edu/course/view.php?id=" + course_id)

    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "page-header"))
    # )
    print("Scraping course " + course_id + " : " + driver.title)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "section-0"))
    )
    time.sleep(1)

    course_sections = driver.find_elements(By.CLASS_NAME, "section")
    for course_section in course_sections:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sectionname"))
            )
            section_name = element.text
        except:
            section_name = None

        print("Scraping section " + section_name)
        section_resources = course_section.find_elements(By.CLASS_NAME, "activity")

# ---------------------------------------------------------------------------- #
#                                  END CLEANUP                                 #
# ---------------------------------------------------------------------------- #

print("THE END")
time.sleep(5)
driver.quit()
