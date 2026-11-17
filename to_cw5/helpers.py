
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import SKLEPTO_URL


def wait_for(driver, by, value, timeout=10):
    """Wait until an element appears."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def open_page(driver, url, by, value):
    """Open the page and wait for its marker."""
    driver.get(url)
    return wait_for(driver, by, value)


def log_in(driver, login, password):
    """Log in and return the flash message."""
    open_page(
        driver,
        f"{SKLEPTO_URL}/logowanie.php",
        By.ID,
        "form-logowanie"
    )

    driver.find_element(By.ID, "login").send_keys(login)
    driver.find_element(By.ID, "haslo").send_keys(password)
    driver.find_element(By.ID, "zaloguj").click()

    return wait_for(driver, By.ID, "flash")
