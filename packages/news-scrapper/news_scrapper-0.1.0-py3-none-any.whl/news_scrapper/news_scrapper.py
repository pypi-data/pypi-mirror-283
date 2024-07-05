from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import os
import sys

def scrape_news(chrome_driver_path, website_url):
    application_path = os.path.dirname(sys.executable)
    path = chrome_driver_path

    now = datetime.now()
    month_day_year = now.strftime("%m%d%Y")

    # We add options.headless = True for Backend automation
    options = Options()
    options.headless = True

    service = Service(executable_path=path)

    # with headless
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(website_url)

    tag_list = []
    sub_headline_list = []

    news_headlines = driver.find_elements(By.XPATH, value='//div[@class="card__content "]')

    for headlines in news_headlines:
        tag = headlines.get_attribute("data-tag")
        sub_headline = headlines.find_element(by='xpath', value='./span/span').text
        tag_list.append(tag)
        sub_headline_list.append(sub_headline)

    news_data = {'Category': tag_list, 'headline': sub_headline_list}
    df_news_data = pd.DataFrame(news_data)

    filename = f'news_headlines{month_day_year}.csv'
    final_path = os.path.join(application_path, filename)
    df_news_data.to_csv(final_path)

    driver.quit()
    return final_path
