import calendar
import configparser
from datetime import datetime

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getConfig():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config

def createDriver():
	options = Options()
	options.add_experimental_option("detach", True)
	options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
	options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
	options.add_experimental_option("useAutomationExtension", False)
	options.add_argument('--disable-blink-features=AutomationControlled')

	# create driver
	driver = webdriver.Chrome(options=options) 
	return driver

def login(driver, config):
	try:
		driver.get('https://www.seongnam.go.kr/member/login.do?menuIdx=1000437&returnURL=%2Fmain.do')

		driver.find_element(By.NAME, 'member_id').send_keys(config.get('account', 'id'))
		driver.find_element(By.NAME, 'pwd').send_keys(config.get('account', 'passwd'))
		driver.find_element(By.ID, 'loginBtn').click()
	except KeyError as e:
		raise e

def checkDate(driver):
	targetDate = config.get('reservation', 'date')
	targetTime = config.get('reservation', 'time')
	date = datetime.strptime(targetDate, '%Y-%m-%d')
	weekday = ((calendar.weekday(date.year, date.month, date.day) + 1) % 7) + 1
	driver.execute_script(f"selectWrite('{targetDate}', '{targetTime}', 'false', '{weekday}');")

def makeRequest(driver, config):
	driver.find_element(By.XPATH, '//*[@id="rent_club_nm"]').send_keys(config.get('reservation', 'club_nm'))
	driver.find_element(By.XPATH, '//*[@id="rent_mobile2"]').send_keys(config.get('reservation', 'rent_mobile').split('-')[1])
	driver.find_element(By.XPATH, '//*[@id="rent_mobile3"]').send_keys(config.get('reservation', 'rent_mobile').split('-')[2])
	driver.find_element(By.XPATH, '//*[@id="rent_amount"]').send_keys('10')
	driver.find_element(By.XPATH, '//*[@id="rent_ceo_nm"]').send_keys(config.get('reservation', 'ceo_nm'))
	driver.find_element(By.XPATH, '//*[@id="rent_ceo_mobile2"]').send_keys(config.get('reservation', 'ceo_mobile').split('-')[1])
	driver.find_element(By.XPATH, '//*[@id="rent_ceo_mobile3"]').send_keys(config.get('reservation', 'ceo_mobile').split('-')[2])
	driver.find_element(By.XPATH, '//*[@id="uploadFile1"]').send_keys(config.get('reservation', 'trainingPlan'))
	driver.find_element(By.XPATH, '//*[@id="uploadFile2"]').send_keys(config.get('reservation', 'participanList'))

if __name__ == "__main__":

	# init 
	config = getConfig()
	driver = createDriver() 
	
	# login
	login(driver, config)

	# go to page for reservation
	driver.get('https://www.seongnam.go.kr/rent/rentParkDataCal.do?menuIdx=1001981&returnURL=%2Fmain.do')

	# chanePark
	driver.execute_script(f"changePark('13', '황새울공원');")
	driver.find_element(By.XPATH, '//*[@id="listForm"]/div[1]/div/span/a').click();

	# check date 
	checkDate(driver)

	# # Agree to the usage
	driver.find_element(By.ID, 'agree_yn').click()
	driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div[4]/span[2]/a').click()

	# # Reservation request
	makeRequest(driver, config)

	# ## Agree to Usage
	# driver.find_element(By.XPATH, '//*[@id="agree_yn"]').click()
	# driver.find_element(By.XPATH, '//*[@id="contents"]/div[4]/span[2]/a').click()

	## alert
	# wait = WebDriverWait(driver, 10)
	# wait.until(EC.alert_is_present())
	# alert = Alert(driver)
	# alert.accept()

	#driver.close()


