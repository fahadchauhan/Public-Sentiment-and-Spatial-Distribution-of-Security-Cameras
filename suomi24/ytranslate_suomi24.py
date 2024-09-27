import pandas as pd
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def create_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 10)

    effective_page_width = pdf.w - 2*pdf.l_margin

    for index, row in data.iterrows():
        text = f"{row['title']} || {row['topic_name_top']} || {row['topic_name_leaf']} || {row['thread_text']} || {row['thread_id']}"
        pdf.multi_cell(effective_page_width, 10, txt = text)
    pdf.output(filename)

def translate_pdf_with_selenium(filepath):
    driver = webdriver.Chrome()  # Adjust if you're using a different browser/driver
    driver.get("https://translate.google.com/?sl=fi&tl=en&op=docs")
    # upload_button = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="tlid-file-input"]'))
    # )
    time.sleep(15)

    # Wait for the Accept All button to be clickable
    accept_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Accept all']"))
    )
    accept_button.click()  # Click the Accept All button

    time.sleep(2)


    file_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    pre_path = 'C:/Users/user/Documents/Public-Sentiment-on-Security-Cameras/' + filepath
    file_input.send_keys(pre_path)  # Send file path directly to the input.


     # Wait for the Translate button to be clickable
    translate_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Translate')]/ancestor::button"))
    )
    translate_button.click()  # Click the Translate button

    # Wait for the translation to complete or for a certain time period
    time.sleep(20)  # This is an arbitrary wait; adjust as needed based on the expected translation time
    
    download_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Download translation')]/ancestor::button"))
    )
    download_button.click()  # Click the Download translation button
    time.sleep(120)  # This is an arbitrary wait; adjust as needed based on the expected translation time

    # Closing the browser
    driver.quit()

# Load CSV file
data = pd.read_csv("C:/Users/user/Documents/suomi24/Data/filtered/s24_2006.csv", usecols=["title", "topic_name_top", "topic_name_leaf", "thread_text", "thread_id"])

# Process each chunk of 1500 rows
for i in range(0, 100, 10):
    chunk = data.iloc[i:i+10]
    pdf_filename = f"chunk_{i//10 + 1}.pdf"
    create_pdf(chunk, pdf_filename)
    translate_pdf_with_selenium(pdf_filename)
    break
    # Further processing to convert translated PDF back to CSV

# Cleanup and finalization code here
