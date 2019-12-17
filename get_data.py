from selenium import webdriver
# 1st import: Allows you to launch/initiate a browser
from selenium.webdriver.common.by import By
# 2nd import: Allows you to search for things using specific parameters.
from selenium.webdriver.support.ui import WebDriverWait
# 3rd import: Allows you to wait for a page to load.
from selenium.webdriver.support import expected_conditions as EC
# 4th import: Specify what you are looking for on a specific page in order to determine that the webpage has loaded.
from selenium.common.exceptions import TimeoutException
# 5th import: Handling a timeout situation
from selenium.webdriver.common.proxy import Proxy, ProxyType
# from selenium.webdriver import ActionChains as Action
# from selenium.webdriver.common.keys import Keys
import re, pymongo, time
from pymongo import MongoClient
def init_browser():
    # driver = webdriver.Chrome('/Users/hh/Documents/Pratt/PFCH/StockX_project/chromedriver')
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = "http://localhost:8118"
    prox.ssl_proxy = "http://localhost:8118"
    
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
    
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    # options.add_argument('headless')
    # set the window size
    options.add_argument('window-size=1881x1280')
    
    # initialize the driver
    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)
    return driver
def sign_in(driver, login_url):
    driver.get(login_url)
    user = 'rimhoho@gmail.com'
    pass_w = 'rim11hoho!'
    
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email-login')))
    username.send_keys(user)
    password = driver.find_element_by_id('password-login')
    password.send_keys(pass_w)
    
    sign_in_button = driver.find_element_by_id('login-button-text')
    sign_in_button.click()
    return 
def click_for_week(driver, collection):
    # avoid = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="om-md1cc1x0pdrcptwxfzur-optin"]/div/button')))
    # time.sleep(1) 
    # if avoid:
    #     avoid.click()
    #     time.sleep(1) 
    keep_looping = True
    table = driver.find_element_by_class_name('activity-table')      
    count = 0
    data = []
    
    while keep_looping:
        rows = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        # for rows in tbody: #rows = tbody.find_elements_by_tag_name('tr') 
        last_date_in_tbody = rows[len(rows)-1].find_element_by_tag_name('td').text
        # print('last_date_in_tbody: ', last_date_in_tbody)
        if 'October 29' not in last_date_in_tbody:
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.button.button-block.button-white')))
            time.sleep(2)
            button.click()
        else:       
            keep_looping = False
             
    for row in rows:
        sneaker = {}
        sneaker['name'] = collection
        sneaker['date'] = row.find_elements_by_tag_name('td')[0].text
        sneaker['time'] = row.find_elements_by_tag_name('td')[1].text
        sneaker['size'] = row.find_elements_by_tag_name('td')[2].text
        sneaker['price'] = row.find_elements_by_tag_name('td')[3].text
        data.append(sneaker)
    # print('='*30)
    # print(data)
    return data

def product_lists(driver, collections):
    products = ['https://stockx.com/' + url for url in collections]

    for product in products:
        driver.get(product)
        collection = re.sub('(https:\/\/stockx.com\/)', '',product)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="market-summary"]/div[1]/div/div/div[1]/button'))) 
        driver.find_element_by_xpath('//*[@id="market-summary"]/div[1]/div/div/div[1]/button').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="market-summary"]/div[1]/div/div/div[2]/div[2]/ul/li[1]/div').click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".gauge-value")))
        time.sleep(1)
        name = driver.find_element_by_class_name('name').text
        style_code = driver.find_element_by_xpath("//span[@data-testid='product-detail-style']").text
        color = driver.find_element_by_xpath("//span[@data-testid='product-detail-colorway']").text
        retaile_price = driver.find_element_by_xpath("//span[@data-testid='product-detail-retail price']").text
        release_date = driver.find_element_by_xpath("//span[@data-testid='product-detail-release date']").text
        img_src = driver.find_element_by_xpath("//img[@data-testid='product-detail-image']").get_attribute('src')
        num_sales = driver.find_elements_by_class_name('gauge-value')[0].text
        price_premium = driver.find_elements_by_class_name('gauge-value')[1].text
        average_sale_price = driver.find_elements_by_class_name('gauge-value')[2].text
        button_sale_history = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div[10]/div/div/div/div[2]/div/div[1]/div[2]/a')))
        button_sale_history.click()      
        sale_history = click_for_week(driver, collection)
        # print('='*30)
        # print('|start', name, '|', style_code, '|', color, '|', retaile_price, '|', release_date, '|', average_sale_price, 'end|')
        collections[collection].insert_many([
            { 'name' : name,
              'style_code' : style_code,
              'color' : color,
              'retaile_price' : retaile_price,
              'release_date' : release_date,
              'img_src' : img_src,
              'num_sales' : num_sales,
              'price_premium' : price_premium,
              'average_sale_price' : average_sale_price,
              'sale_history' : sale_history
        }])
        # bottom_banner = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".irvine-CloseButton")))
        # bottom_banner.click()
    return                  
def access_db(dbname, collectionnames):
    cluster = MongoClient('mongodb+srv://rimho:0000@cluster0-yehww.mongodb.net/test?retryWrites=true&w=majority')
    db = cluster[dbname]
    collections = {c:db[c] for c in collectionnames}
    return db, collections
    
def main():
    db, collections = access_db('stockX_db', ['adidas-yeezy-boost-350-v2-cloud-white', 'adidas-yeezy-500-soft-vision', 'adidas-yeezy-boost-700-inertia','air-jordan-6-retro-travis-scott','air-jordan-1-retro-high-shattered-backboard-3', 'air-jordan-11-retro-playoffs-2019'])
    driver = init_browser()
    login_url = 'https://stockx.com/login'
    sign_in(driver, login_url)
    time.sleep(3) 
    product_lists(driver, collections)
    print('Mission has been completed! Go to your DB and get data!')
    return 
main()