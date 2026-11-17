
from selenium.webdriver.common.by import By

from config import SKLEPTO_URL
from helpers import open_page


def test_home_page(driver):
    """REQ-UI-02: Home page has the correct title."""
    open_page(
        driver,
        f"{SKLEPTO_URL}/index.php",
        By.ID,
        "opis"
    )

    assert driver.title == "SklepTO – strona główna"


def test_main_menu(driver):
    """REQ-UI-01: Guest menu contains seven links."""
    open_page(
        driver,
        f"{SKLEPTO_URL}/index.php",
        By.ID,
        "menu"
    )

    links = driver.find_elements(
        By.CSS_SELECTOR,
        "#menu a"
    )

    assert len(links) == 7


def test_footer(driver):
    """REQ-UI-07: Footer shows application version."""
    open_page(
        driver,
        f"{SKLEPTO_URL}/index.php",
        By.ID,
        "stopka"
    )

    footer = driver.find_element(By.ID, "stopka")

    assert "Wersja 1.0" in footer.text
