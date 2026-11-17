
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import SKLEPTO_URL


def reset_database(driver):
    """Restore initial SklepTO data."""
    driver.get(f"{SKLEPTO_URL}/install.php?reset=1")

    status = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "install-status")
        )
    )

    assert status.text.strip() == "OK"


@pytest.fixture(scope="session")
def driver():
    """Create one browser for the test session."""
    browser = webdriver.Chrome()
    browser.implicitly_wait(0)

    try:
        reset_database(browser)
        yield browser
    finally:
        browser.quit()


@pytest.fixture(autouse=True)
def no_cookies(driver):
    """Clear login session before every test."""
    driver.delete_all_cookies()


@pytest.fixture
def clean_db(driver):
    """Reset database before tests changing data."""
    reset_database(driver)
