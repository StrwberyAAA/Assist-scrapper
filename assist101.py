from selenium import webdriver; from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options; from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait; from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO

# starting up
options = Options()
options.add_argument("--log-level=3")
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://assist.org"); WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//awc-omniselect//input[@id='governing-institution-select']")))


# 4 year uni selector 
uni = driver.find_element(By.XPATH, "//awc-omniselect//input[@id='governing-institution-select']")
uni.send_keys(input("Enter University: ").strip())
uni.send_keys(Keys.RETURN)

# cc selector 
CC = driver.find_element(By.XPATH, "//awc-omniselect//input[@id='agreement-institution-select']")
CC.send_keys(input("Enter community college: ").strip())
CC.send_keys(Keys.RETURN) 

# loads into the new page where you now choose department i.e. English or Accounting
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and @class='btn btn-primary']"))).click()
Department = input("Enter Department: ").strip()
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search' and @aria-label='Search for Department']"))).send_keys(Department)
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'viewByRowColText')]"))).click()


# look for the course number 
course = input("Enter the course prefix or number to search: ").strip()
driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((
        By.XPATH, f"//div[@class='prefixCourseNumber' and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{course.lower()}')]"
    ))
))

# take screenshot
page_screenshot = driver.get_screenshot_as_png()
img = Image.open(BytesIO(page_screenshot)).show()

print(f"Successfully found {course}")
print("Agreement results loaded. Current URL:", driver.current_url)
driver.quit() 
