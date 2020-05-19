# Requirements:
# pip install selenium
# pip install python-anticaptcha
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys

# VARIABLES
num_of_accs = 1 # This expects you to have X number of accs in the twitch and rs acc text files
proxy = 'http://proxyip:proxyport' # Your proxy IP to run chrome with. Should rotate every ~2 minutes to avoid twitch captchas
apikey = "anticaptchaAPIkeyhere"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy}")

sitekey = "6Lcsv3oUAAAAAGFhlKrkRb029OHio098bbeyi_Hv"
client = AnticaptchaClient(apikey)


def login_to_twitch(username, password):
	"""Login to twitch"""
	try:
		# Click the login button
		wait.until(
			EC.presence_of_element_located((By.XPATH, "//button[@data-a-target='login-button']"))
				).click()
	except Exception:
		print(Exception)
		print("\nProbably couldn't find the login button. Send full error to Gavin")
	else:
		# Wait until we can see the username field and then enter our twitch username
		wait.until(
			EC.presence_of_element_located((By.XPATH, "//input[@id='login-username']"))
				).send_keys(username)
		# Enter our twitch password
		wait.until(
			EC.presence_of_element_located((By.XPATH, "//input[@id='password-input']"))
				).send_keys(password)
		# Click the Login button
		wait.until(
			EC.presence_of_element_located((By.XPATH, "//button[@data-a-target='passport-login-button']"))
				).click()

def claim_loot(rs_username, rs_password):
	"""Goes through the twitch prime loot claiming process"""
	sleep(15)

	# Cicks the 'prime loot' button
	print("Clicking the prime loot drop down button")
	wait.until(
		EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label,'Prime offers')]"))
			).click()

	
	print("Finding claim offer button")
	try:
		# Define the claim offer button for runescape
		claim_offer_button = wait.until(
			EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'prime-offer tw-relative') and contains(., 'RuneScape')]//button[@data-a-target='prime-claim-button']"))
			)
	except Exception:
		print("Claim offer button not found. It's probably already been clicked on this account.")

		print("Finding claim offer hyperlink")
		link_button = wait.until(
			EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Link your Twitch and RuneScape')]"))
				)
		print("Scrolling to claim offer hyperlink")
		driver.execute_script("arguments[0].scrollIntoView();", link_button)
		sleep(3)
		print("Clicking hyperlink")
		link_button.click()

		# Switching Selenium's focus to our second tab(authorize page and then runescape's page after)
		driver.switch_to_window(driver.window_handles[1])
		# Clicking Authorize on new page
		wait.until(
			EC.presence_of_element_located((By.XPATH, "//button[@class='button button--large js-authorize']"))
				).click()

	else:
		print("Claim offer button found")

		# Scroll down to the claim offer button
		print("Scrolling down to the claim offer button")
		driver.execute_script("arguments[0].scrollIntoView();", claim_offer_button)
		sleep(2)

		wait.until(
			EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Link your Twitch and RuneScape')]"))
				).click()

		# Click the claim offer button
		print("Clicking claim offer")
		claim_offer_button.click()

		# Switching Selenium's focus to our second tab(authorize page and then runescape's page after)
		driver.switch_to_window(driver.window_handles[1])
		# Clicking Authorize on new page
		wait.until(
			EC.presence_of_element_located((By.XPATH, "//button[@class='button button--large js-authorize']"))
				).click()


	# Click the "Got It" button for runescape cookies
	print("Clicking button to accept cookies on runescape site")
	wait.until(
		EC.presence_of_element_located((By.XPATH, "/html/body[@id='p-']/div[@class='c-cookie-consent']/div[@class='c-cookie-consent__options']/a[@class='a-button c-cookie-consent__dismiss']"))
			).click()

	# Click the "YES - LOG IN" button to login to runescape account
	print("Clicking the 'YES - LOG IN' button to take us to the runescape login page")
	wait.until(
		EC.presence_of_element_located((By.XPATH, "/html/body[@id='p-']/main[@class='l-vista ']/div[@class='l-vista__central']/div[@id='l-vista__container']/div[@class='m-choices']/div[@class='m-choices__option'][1]/a[@class='a-button a-button--size-full']"))
			).click()

	sleep(5)
	invisible_captcha = True
	print("Solving captcha")
	token = get_token(driver.current_url, sitekey, invisible_captcha)
	print(f"Captcha solved:\n{token}")

	
	# Enter our runescape username into the username field
	print("Entering our runescape username")
	wait.until(
		EC.presence_of_element_located((By.XPATH, "//input[@id='login-username']"))
			).send_keys(rs_username)

	# Enter our runescape password into the password field
	print("Entering our runescape password")
	wait.until(
		EC.presence_of_element_located((By.XPATH, "//input[@id='login-password']"))
			).send_keys(rs_password)

	# click the login button on the runescape page
	print("Clicking the runescape login button to get membership")
	wait.until(
		EC.presence_of_element_located((By.XPATH, "/html/body[@id='p-login']/main[@class='l-vista l-vista--size-narrow']/div[@class='l-vista__central']/div[@id='l-vista__container']/form[@id='login-form']/button[@id='du-login-submit']"))
			).click()

	# Injecting captcha response
	print("Injecting captcha response")
	driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{}';".format(token))
	# Submit our login form once the captcha is injected into the page
	print("response injected. Submitting form")
	driver.execute_script("document.getElementById('login-form').submit()")

	print("Membership has been attached. Exiting window in 5 seconds.")
	sleep(5)
	driver.quit()


def get_token(website_url, site_key, invisible):
	"""Gets captcha solution"""
	task = NoCaptchaTaskProxylessTask(
		website_url=website_url,
		website_key=site_key,
		is_invisible=invisible
	)
	while True:
		try:
			job = client.createTask(task)
			job.join()
			response = job.get_solution_response
		except Exception:
			print(Exception)
			print("Captcha service failed.. Retrying")
			continue
		break

	return job.get_solution_response()

def open_files():
	try:
		twitch_acc_list = open("twitch_info.txt", "r")
	except FileNotFoundError:
		sys.exit("twitch_info.txt wasn't found. "
			"Make sure it's in the same directory.")
	else:
		try:
			rs_acc_list = open("rs_acc_info.txt", "r")
		except FileNotFoundError:
			sys.exit("rs_acc_info.txt wasn't found. "
				"Make sure it's in the same directory.")
	finally:
		return twitch_acc_list, rs_acc_list


def get_twitch_acc(acc_list):
	"""Gets twitch acc info from file"""
	try:
		acc = (next(acc_list))
	except StopIteration:
		sys.exit("\nWe're out of twitch accounts.")
	else:
		username = acc.split(':', 1)[0]
		password = acc[acc.index(':')+1:acc.index('\n')]
		return username, password   

def get_rs_acc(acc_list):
	"""Gets our runescape acc info from file"""
	try:
		acc = (next(acc_list))
	except StopIteration:
		sys.exit("\nWe're out of runescape accounts.")
	else:
		username = acc.split(':', 1)[0]
		password = acc[acc.index(':')+1:acc.index('\n')]
		return username, password


twitch_acc_list, rs_acc_list = open_files()
counter = 0
while counter < num_of_accs:
	counter += 1

	twitch_username, twitch_password = get_twitch_acc(twitch_acc_list)
	rs_username, rs_password = get_rs_acc(rs_acc_list)

	print(f"Using twitch info: {twitch_username}, {twitch_password}")
	print(f"Using rs info: {rs_username}, {rs_password}")

	driver = webdriver.Chrome(chrome_options=chrome_options)
	wait = WebDriverWait(driver, 30) # 30 is the timeout threshold in seconds
	driver.get("https://www.twitch.tv/me")

	login_to_twitch(twitch_username, twitch_password)
	claim_loot(rs_username, rs_password)

print("Finished creating accounts.")
