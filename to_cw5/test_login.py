
import pytest
from selenium.webdriver.common.by import By

from config import SKLEPTO_URL
from helpers import log_in, open_page, wait_for


def test_valid_login(driver, clean_db):
    """REQ-LOG-02: Valid credentials allow login."""
    message = log_in(driver, "jan", "Haslo123")

    assert message.text == "Zalogowano jako jan."
    assert driver.current_url.endswith("index.php")

    user = driver.find_element(By.ID, "zalogowany")
    assert user.text == "Zalogowano: jan"


@pytest.mark.parametrize(
    "login,password,expected",
    [
        (
            "jan",
            "wrongpassword",
            "Błędny login lub hasło. Pozostało prób: 2."
        ),
        (
            "unknown",
            "Haslo123",
            "Błędny login lub hasło."
        ),
        (
            "zablokowany",
            "Haslo123",
            "Konto jest zablokowane. "
            "Skontaktuj się z administratorem."
        ),
    ]
)
def test_invalid_login(
    driver, clean_db, login, password, expected
):
    """REQ-LOG-03/05/06: Invalid login is rejected."""
    message = log_in(driver, login, password)

    assert message.text == expected


def test_account_lockout(driver, clean_db):
    """REQ-LOG-04: Three failures lock an account."""
    expected_messages = [
        "Błędny login lub hasło. Pozostało prób: 2.",
        "Błędny login lub hasło. Pozostało prób: 1.",
        "Konto zostało zablokowane po 3 nieudanych próbach.",
    ]

    for expected in expected_messages:
        message = log_in(driver, "jan", "badpassword")
        assert message.text == expected

    open_page(
        driver,
        f"{SKLEPTO_URL}/admin.php",
        By.ID,
        "uzytkownicy"
    )

    row = driver.find_element(
        By.CSS_SELECTOR,
        "tr[data-login='jan']"
    )

    status = row.find_element(
        By.CSS_SELECTOR,
        "td.status"
    )

    assert status.text == "LOCKED"


def test_logout(driver, clean_db):
    """REQ-LOG-07: Logout terminates the user session."""
    log_in(driver, "jan", "Haslo123")

    driver.find_element(By.ID, "nav-wyloguj").click()

    message = wait_for(driver, By.ID, "flash")

    assert message.text == "Wylogowano."
    assert driver.find_element(
        By.ID, "nav-logowanie"
    ).is_displayed()


@pytest.mark.xfail(
    reason="DEF-01: Failed attempts are not reset after successful login",
    strict=True
)
def test_login_resets_failed_attempts(driver, clean_db):
    """REQ-LOG-02: Valid login resets failed attempts."""
    log_in(driver, "jan", "wrongpassword")
    log_in(driver, "jan", "Haslo123")

    open_page(
        driver,
        f"{SKLEPTO_URL}/admin.php",
        By.ID,
        "uzytkownicy"
    )

    row = driver.find_element(
        By.CSS_SELECTOR,
        "tr[data-login='jan']"
    )

    attempts = row.find_element(
        By.CSS_SELECTOR,
        "td.proby"
    )

    assert attempts.text == "0"
