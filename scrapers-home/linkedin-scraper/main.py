import pandas as pd
import time
import urllib
from math import ceil
import pickle
import os

# import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# ignore warning
import warnings
warnings.filterwarnings("ignore")


# Extra details
time_out_each_element = 10
job_id  = 0

def SetupChrome():
    # set up chrome options
    global driver
    chrome_options = Options()

    # headless
    chrome_options.add_argument("--headless=new")
    # full screen 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    # set up driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # go to linkedin
    driver.get('https://www.linkedin.com/login')

    # load cookie
    with open('cookies.pkl', 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

        # refresh page
        driver.get('https://towardsdatascience.com/deploy-pycaret-and-streamlit-app-using-aws-fargate-serverless-infrastructure-8b7d7c0584c2')

        print('Cookie loaded')

    # wait for page to load
    return     

def GetTheFilterRight():
    # get all filter button
    all_filter_button = WebDriverWait(driver, time_out_each_element).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "all filters")]')))
    # click the button
    all_filter_button.click()
    
    time.sleep(1)

    # click the past_24_hour_filter
    past_24_hour_filter = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH,'//label[@for="advanced-filter-timePostedRange-r86400"]')))
    past_24_hour_filter.click()

    time.sleep(1)

    # click internship button
    internship_button = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//label[@for="advanced-filter-experience-1"]')))
    internship_button.click()

    time.sleep(1)

    # click apply button
    apply_button = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//div[@class="justify-flex-end display-flex mv3 mh2"]/button[contains(@aria-label,"Apply current filter")]')))
    print(apply_button.text)
    time.sleep(1)
    if (apply_button.text == 'Show 0 results'):
        print('bruh')
        return "Negative"
    else:
        apply_button.click()
        return "Positive"
        

def ScrapJobCard(title):
    # job title
    try:
        job_title = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//div[@class="jobs-unified-top-card__content--two-pane"]//a/h2'))).text
    except:
        job_title = ''
    # job link
    try:
        job_link = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//div[@class="jobs-unified-top-card__content--two-pane"]//a[@class="ember-view"]'))).get_attribute('href')
    except:
        job_link = ''

    # job location - company name - workplace type
    # company name
    try:
        company_name = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-primary-grouping t-black"]//span[@class="jobs-unified-top-card__company-name"]'))).text
    except:
        company_name = ''
    # company link
    try:
        company_link = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-primary-grouping t-black"]//span[@class="jobs-unified-top-card__company-name"]//a'))).get_attribute('href')
    except:
        company_link = ''
    # job location
    try:
        job_location = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-primary-grouping t-black"]//span[@class="jobs-unified-top-card__bullet"]'))).text
    except:
        job_location = ''
    # work place type
    try:
        workplace_type = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-primary-grouping t-black"]//span[@class="jobs-unified-top-card__workplace-type"]'))).text
    except:
        workplace_type = ''
    # Post date and number of applicants
    # post date
    try:
        post_date = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-secondary-grouping t-black--light"]//span[contains(@class, "jobs-unified-top-card__posted-date")]'))).text
    except:
        post_date = ''

    # number of applicants
    try:
        try:
            number_of_applicants = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-secondary-grouping t-black--light"]//span[contains(@class, "jobs-unified-top-card__applicant-count")]'))).text
        except:
            number_of_applicants = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//span[@class="jobs-unified-top-card__subtitle-secondary-grouping t-black--light"]//span[contains(@class, "jobs-unified-top-card__bullet")]'))).text
    except:
        number_of_applicants = ''
    # Skill Listed By Job Poster
    skill_list = []
    try:
        skills = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="app-aware-link  job-details-how-you-match__skills-item-subtitle t-14 overflow-hidden"]')))
        for skill_small in skills:
            skill = skill_small.text

            # remove the and in skill
            if 'and' in skill:
                skill = skill.replace(' and', '')

            # remove all the comma and add to list
            if ',' in skill:
                skill_list.extend(skill.split(', '))
            else:
                skill_list.append(skill)
    except:
        pass

    # Job Description
    try:
        description = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "jobs-description__content jobs-description-content")]'))).text
    except:
        description = ''

    # return a dictionary
    return {
        'job_title': job_title,
        'job_link': job_link,
        'description': description,
        'company_link': company_link,
        'job_location': job_location,
        'workplace_type': workplace_type,
        'post_date': post_date,
        'number_of_applicants': number_of_applicants,
        'skill_list': skill_list,
        
        'title': title
    }


# scroll for linkedin
def scroll(element):
    # Get the current height of the element
    initial_height = driver.execute_script("return arguments[0].scrollHeight", element)

    # Calculate the target scroll position (2/3 of the initial height)
    target_scroll_position = initial_height * 1/5
    # Define the duration of the scroll in seconds
    scroll_duration = 2

    # Define the number of steps for the smooth scroll
    num_steps = 30

    # Calculate the distance to scroll per step
    scroll_distance = (target_scroll_position - initial_height) / num_steps

    # Perform the smooth scroll
    for step in range(num_steps):
        scroll_amount = initial_height + (scroll_distance * step)
        driver.execute_script("arguments[0].scrollTop = arguments[1];", element, scroll_amount)
        time.sleep(scroll_duration / num_steps)

    # Set the final scroll position
    driver.execute_script("arguments[0].scrollTop = arguments[1];", element, target_scroll_position)


# Print the job card details
def PrintJobCard(job_detail):
    global job_id
    # print on one line, only job title and company and number of applicants
    print(f'{job_id} - {job_detail["job_title"]} - {job_detail["company_name"]} - {job_detail["number_of_applicants"]}')
    job_id += 1

def WriteResultToCSV(df, job_title):
    # check if there is a folder called result in the current directory
    if not os.path.exists('result'):
        os.makedirs('result')
        # create a new csv file
        df.to_csv(f'result/{job_title}.csv', index=False)

    # otherwise, just create a new csv file in the result folder
    else:
        df.to_csv(f'result/{job_title}.csv', index=False)

def main():
    job_titles = [
        # Analyzing Data
        "data scientist intern",
        "data intern",
        "business analyst intern",
        "data engineer intern",
        "quantitative analyst intern",
        "data analyst intern",
        
        # Working with Cloud and Building Cloud Architect
        "cloud architect intern",
        "cloud solutions intern",
        "cloud infrastructure architect intern",
        "cloud systems architect intern",
        "cloud engineer intern",
            
        # DevOps
        "devops engineer intern",
        "devops specialist intern",
        "devops architect intern",
    ]

    # set up chrome
    SetupChrome()

    print('start scraping that')

    # Go over Job title
    for title in job_titles:
        print('what the hell')
        encoded_title = urllib.parse.quote(title)
        print(encoded_title)
        # create a new df
        df = pd.DataFrame(columns=['job_title', 'job_link',  'description','company_name', 'company_link', 'job_location', 'workplace_type', 'post_date', 'number_of_applicants', 'skill_list', 'title'])
        print(df)
        # go to the url
        url = f'https://www.linkedin.com/jobs/search/?geoId=103644278&keywords={encoded_title}&location=United%20States&refresh=true&sortBy=R'
        print(url)
        
        # open another tab
        driver.execute_script("window.open('');")
        # switch to the new window
        driver.switch_to.window(driver.window_handles[1])

        # go to the url
        driver.get(url)
        time.sleep(3)

        # get the filter right
        status = GetTheFilterRight()
        time.sleep(4)
        if status == 'Negative':
            print('Found no Job')
            continue
        else:
            print('find job')
        # Now start scraping
        element = driver.find_elements(By.XPATH, '//div[contains(@class, "jobs-search-results-list")]')
        print(element)
        html = driver.page_source
        with open("output.html", "w") as f:
        # Write the HTML of the file to the file
            f.write(html)

        element = element[2]

        # scroll to the bottom of the page
        scroll(element)

        # now find the number of pages available for that job title
        try:
            print('--' * 20)
            print('Start on new page')
            navigate_bar = driver.find_element(By.XPATH, '//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]')
            current_active = navigate_bar.find_element(By.XPATH, './/li[@class="artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view"]')
            print('current active:',current_active.text + '/' + navigate_bar.text.split('\n')[-1])
        except:
            print('error reading page list or there is only one page')
            pass

        # Get all the job card containers on one page
        try:
            containers = WebDriverWait(driver, time_out_each_element).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "job-card-container relative job-card-list")]')))
            print(len(containers))
        except:
            break
        
        # if program still go on, then scrape the job card
        for job in containers:
            try:
                # click on the job card
                
                job.click()
                # wait for the job description to load
                time.sleep(1)

                # Get detail from the job card
                job_detail = ScrapJobCard(title=title)

                # print the job card (for debugging)
                PrintJobCard(job_detail)
                

                # append the job detail to the dataframe
                df = df.append(job_detail, ignore_index=True)
            except:
                print('error clicking on the job card. Skip Job')
                pass


        # return the result by save a csv file in a folder called 'result'
        WriteResultToCSV(df, title)


    driver.close()


if __name__ == '__main__':
    main()
    