# BEFORE USING THIS, PLEASE FOR THE LOVE OF GOD USE A VPN!

import string, random, requests, json, time, sqlite3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from guerrillamail import GuerrillaMailSession

db = sqlite3.connect("users.db")
db_cur = db.cursor()

table_exists = db_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchone()
if not table_exists:
    db_cur.execute("CREATE TABLE users(username, email, password, site)")

mode = input("[B]itView or [V]idLii: ").strip().lower()

if_usernames = input("Do you want to include the usernames and templates files? [y/N]: ").strip().lower()
if if_usernames == "y":
    usernames = open("usernames.txt").readlines()
    templates = open("templates.txt").readlines()

# NEEDED TO SOLVE THE SHITTY "KAPTCHA"S,
# VISIT https://truecaptcha.org/ TO GET THE KEY & USER ID
api_key = "FZBumZlZ8C3i4ZDCUcpF" 
api_uid = "trioptimum.rab64@simplelogin.com"

api_url = "https://api.apitruecaptcha.org/one/gettext"

options = Options()
# keeps the window open after the program
# has finished execution, don't reccomend
# setting this to true unless you're only
# making one account
options.add_experimental_option("detach", True)

# feel free to change this to whatever
# browser you're using
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

if mode == "b":
    driver.get("https://bitview.net/signup.php")
elif mode == "v":
    driver.get("https://vidlii.com/register")
driver.maximize_window()


def ran_string(length):
    letters = string.ascii_letters
    str = ''.join(random.choice(letters) for i in range(length))
    return str

# this is how you would find the sign
# up links manually, only keeping this
# here so I know how to do it
#
# links = driver.find_elements("xpath", "//a[@href]")
#
# for link in links:
#     if "Sign Up" in link.get_attribute("innerHTML"):
#         link.click()
#         break

if mode == "b":
    fields = driver.find_elements("xpath", "//td[@class='formFieldSmall']//input")
elif mode == "v":
    fields = driver.find_elements("xpath", "//form[@name='userform']//table//tbody//tr//td//input")

# creates a disposable email using GuerrillaMail's API
email = GuerrillaMailSession()
password = ran_string(10)
if if_usernames == "y":
    username = templates[random.randint(0, len(templates))].format(usernames[random.randint(0, len(usernames))])
else:
    username = ran_string(12)

for field in fields:
    if "email" in field.get_attribute("name"):
        field.send_keys(email.get_session_state()["email_address"])
    elif "password" in field.get_attribute("name") or "password_again" in field.get_attribute("name") or "password2" in field.get_attribute("name"):
        field.send_keys(password)
    elif "username" in field.get_attribute("name") or "vl_usernames" in field.get_attribute("name"):
        field.send_keys(username)

if mode == "v":
    vl_fields = driver.find_elements("xpath", "//form[@name='userform']//table//tbody//tr//td//select")
    for field in vl_fields:
        if "country" in field.get_attribute("name"):
            Select(field).select_by_value("US")
        elif "year" in field.get_attribute("name"):
            Select(field).select_by_value("2000")

# capture a screenshot of the "kaptcha"
# and save it in base64 so it can be
# sent over to the captcha API
kaptcha = driver.find_element("xpath", "//img[@alt='LOADING...']")
api_b64 = kaptcha.screenshot_as_base64

api_post = {
    "userid": api_uid,
    "apikey": api_key,
    "data": api_b64,
    "case": "mixed",
}

api_response = requests.post(api_url, json=api_post)

print(api_response.json())

if api_response.json()["success"] == True:
    kaptcha_field = driver.find_element("xpath", "//input[@class='ka_input']")
    kaptcha_field.send_keys(api_response.json()["result"])

db_cur.execute(f"INSERT INTO users VALUES ('{username}', '{email.get_session_state()['email_address']}', '{password}', '{mode}')")
db.commit()

time.sleep(1)

if mode == "b":
    driver.find_element("xpath", "//input[@name='terms_agreed']").click()
    driver.find_element("xpath", "//form[@id='register']").submit()
elif mode == "v":
    driver.find_element("xpath", "//input[@name='age']").click()
    driver.find_element("xpath", "//form[@name='userform']").submit()
