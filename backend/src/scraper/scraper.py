import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import signal
from dotenv import load_dotenv
import os
import concurrent.futures

import dataframe

# Global variables
job_titles = []
company_names = []
post_dates = []
number_applicants = []
role_locations = []
job_type = []
job_desc = []
experience_level = []


def find_element(element, by, locator):
    try:
        result = element.find_element(by, locator).text
        return result
    except:
        pass
        # print("pass test")
        return ''


# Function to login
def login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    print("Selenium running on Docker")
    # driver.quit()

    # with open('backend/assets/user_credentials.txt', 'r', encoding="utf-8") as file:
    #     user_credentials = file.readlines()
    #     user_credentials = [line.rstrip() for line in user_credentials]
    
    load_dotenv()
    user_name = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    # user_name = user_credentials[0]
    # password = user_credentials[1]

    driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(user_name)
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
    driver.implicitly_wait(30)

# Function to get to jobs page and search for job specified
def go_to_jobs(driver, job_name, job_location):

    print("On jobs page")

    driver.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a').click()
    time.sleep(2) 

    driver.find_element(By.XPATH, "//div[@class='scaffold-finite-scroll__content']/div/div/div/div/section/div[2]/a").click()

    driver.find_element(By.XPATH, "//div[@id='global-nav-search']/div/div[contains(@class, 'jobs-search-box__container')]/div[contains(@class, 'jobs-search-box__input--keyword')]/div/div/input[1]").send_keys(job_name)
    driver.find_element(By.XPATH, "//div[@id='global-nav-search']/div/div[contains(@class, 'jobs-search-box__container')]/div[contains(@class, 'jobs-search-box__input--location')]/div/div/input[1]").send_keys(job_location)

    time.sleep(1)
    # Searh Button click
    driver.find_element(By.XPATH, "//div[@id='global-nav-search']/div/div[2]/button[contains(@class, 'jobs-search-box__submit-button')]").click()

# Function to collect job links
def collect_job_links(driver):
    print("Collecting job links")
    links = []
    try: 
        for page in range(2,3):
            time.sleep(2)
            jobs_block = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container') 
            jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
        
            for job in jobs_list:
                all_links = job.find_elements(By.TAG_NAME, 'a')
                for a in all_links:
                    if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                        links.append(a.get_attribute('href'))
                    else:
                        pass
                # scroll down for each job element
                driver.execute_script("arguments[0].scrollIntoView();", job)
            
            print(f'Collecting the links in the page: {page-1}')
            # go to next page:
            driver.find_element("xpath", f"//button[@aria-label='Page {page}']").click()
            time.sleep(3)
    except:
        pass

    return links

# Function to scrape job details
def scrape_job_details(driver, links):
    i = 0
    j = 1
    # Visit each link one by one to scrape the information
    print('Visiting the links and collecting information just started.')
    for i in range(len(links)):
        
        # This is in-case the "see more" explandable is there
        try:
            driver.get(links[i])
            i=i+1
            time.sleep(1)
            # Click See more.
            driver.find_element("class name", "jobs-description__footer-button").click()
            time.sleep(1)
        except:
            pass

        # Get general information of the job postings
        content = driver.find_element("class name", 'p5')
        job_details = content.find_element("class name", 'mb2')

        try:
            job_titles.append(content.find_element("tag name", 'h1').text)
        except:
            job_titles.append('')
            pass

        # try:
        #     company_names.append(job_details.find_element("tag name", 'a').text)
        # except:
        #     company_names.append('')
        #     pass
        company_names.append(find_element(job_details, By.TAG_NAME, 'a'))

        # try:
        #     post_dates.append(job_details.find_element(By.XPATH, "//span[3]/span").text)
        #     # //div[@class='job-details-jobs-unified-top-card__primary-description-container']/div/span[5]
        # except:
        #     post_dates.append('')
        #     pass
        post_dates.append(find_element(job_details, By.XPATH, '//span[3]/span'))

        # try:
        #     number_applicants.append(job_details.find_element(By.XPATH, "//span[5]").text)
        # except:
        #     number_applicants.append('')
        #     pass
        number_applicants.append(find_element(job_details, By.XPATH, '//span[5]'))


        # try:
        #     span_text = content.find_element(By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span").text

        #     if span_text not in ['On-site', 'Hybrid', 'Remote']:
        #         span_text = content.find_element(By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[2]").text
            
        #     role_locations.append(span_text)
        # except:
        #     role_locations.append('')
        #     pass
        span_text = find_element(content, By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span")
        if span_text not in ['On-site', 'Hybrid', 'Remote']:
            span_text = find_element(content, By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[2]")
        role_locations.append(span_text)
        

        # try:
        #     span_text = content.find_element(By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[2]").text

        #     if span_text not in ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Volunteer', 'Other']:
        #         span_text = content.find_element(By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[3]").text

        #     job_type.append(span_text)
        # except:
        #     job_type.append('')
        #     pass
        span_text = find_element(content, By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[2]")
        if span_text not in ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Volunteer', 'Other']:
            span_text = find_element(content, By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[3]")
        job_type.append(span_text)
        


        # try:
        #     span_text = content.find_element(By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[3]").text

        #     if span_text not in ['Internship', 'Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']:
        #         span_text = content.find_element(By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[4]").text

        #     experience_level.append(span_text)
        # except:
        #     experience_level.append('')
        #     pass
        span_text = find_element(content, By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[3]")
        if span_text not in ['Internship', 'Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']:
            span_text = find_element(content, By.XPATH, "//div[@class='mt3 mb2']/ul/li[1]/span/span[4]")
        experience_level.append(span_text)

        print(f'Scraping Job Posting {j} DONE.')
        j = j + 1
            
        time.sleep(0.5)

        # Scraping the job description
        job_description = driver.find_elements("class name", 'jobs-description__content')
        for description in job_description:
            job_text = description.find_element("class name", "jobs-description-content__text").text
            job_desc.append(job_text)
            print(f'Scraping Job Posting {j}')        


def main():

    # Consts
    job_name = sys.argv[1]
    job_location = sys.argv[2]
    # job_name = "Software Engineer"
    # job_location = "Ottawa, ON"


    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)

    driver.maximize_window()

    # 2 second timeout
    driver.implicitly_wait(1)

    login(driver)
    time.sleep(2)

    go_to_jobs(driver, job_name, job_location)
    time.sleep(1)

    # Search for jobs and collect links
    job_links = collect_job_links(driver)


    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     results = list(executor.map(lambda job_links: scrape_job_details(driver, job_links), job_links))




    # Scrape job details using collected links
    scrape_job_details(driver, job_links)

    # Delete previous output files
    if not os.path.exists("./output"):
        os.mkdir("./output")

    if os.path.exists("./output/jobs.csv"):
        os.remove("./output/jobs.csv")
    if os.path.exists("./output/jobs_cleaned.csv"):
        os.remove("./output/jobs_cleaned.csv")

    # Create pandas dataframe and output to CSV
    df = dataframe.create_data_frame(job_titles, company_names, role_locations, job_type, experience_level, post_dates, number_applicants)
    df.to_csv('backend/output/jobs.csv', index=False)

    # Clean and output cleaned dataframe
    df = dataframe.clean_data_frame(df)
    df.to_csv('backend/output/jobs_cleaned.csv', index=False)

    # # Send the CSV file to the Flask endpoint
    # files = {'file': open(csv_file_path, 'rb')}  # 'file' should match the key expected by your Flask endpoint
    # response = requests.post(flask_endpoint_url, files=files)

    driver.quit()

if __name__ == "__main__":
    main()
