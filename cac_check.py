from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
from time import sleep, time

# GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
# CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'


def get_token(api_key, url, driver):
    method = "userrecaptcha"
    site_key = "6LdLdSATAAAAAEQbhjzklHtmcPds-hJMT51aHC9m"
    api_url="http://2captcha.com/in.php?key={}&method={}&googlekey={}&pageurl={}".format(api_key, method, site_key, url)
    
    driver.get(api_url) # making api request to 2captcha
    response = driver.page_source # api request response
    # removing html tags from response
    if 'OK' in response:
        captcha_id = re.sub('<[\w]+>*|<\/[\w]+>*', '', response).split('|')[1]
        # start_time = time()
        # url to get captcha token
        fetch_url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(api_key, captcha_id)
        for i in range(1, 20):
            sleep(5) # wait 5 sec.
            driver.get(fetch_url)
            reply = driver.page_source
            if 'OK' in reply:
                break
        token = re.sub('<[\w]+>*|<\/[\w]+>*', '', reply).split('|')[1]
        # print('Time to solve: ', time() - start_time)
        return token
    else:
        print("response Error")

def browser(api_key, url, company_name, driver):
    token = get_token(api_key, url, driver) #function to get api
    driver.get(url) # open cac website
    search = driver.find_element_by_name('search_value')
    search.clear()
    search.send_keys(company_name)
    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{}';".format(token))
    button = driver.find_element_by_name('search').click()
    return driver.page_source



def scraper(company_name):
    # chrome_path = 'C:\\Users\\BUCHI\\Downloads\\Programs\\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    # options.binary_location = GOOGLE_CHROME_PATH
    options.set_headless()
    # driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
    api_key = "5050a1bdffcfe8fb69583c08263fc4f3"
    url = "https://publicsearch.cac.gov.ng/ComSearch/"
    page_source = browser(api_key, url, company_name, driver)
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()
    table = soup.find_all('table')[0]
    if str(table):
        df = pd.read_html(str(table), header=0)
        data = df[0]
        return data
    else:
        return 0