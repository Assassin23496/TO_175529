import pytest
from selenium.webdriver.common.by import By

from config import SKLEPTO_URL
from helpers import open_page, wait_for


def open_contact(driver):
    """Open the contact form."""
    return open_page(
        driver,
        f"{SKLEPTO_URL}/kontakt.php",
        By.ID,
        "form-kontakt"
    )


def test_valid_contact(driver, clean_db):
    """REQ-KON-05: A valid message is accepted."""
    open_contact(driver)

    driver.find_element(By.ID, "imie").send_keys("Jan")
    driver.find_element(By.ID, "email").send_keys(
        "jan@example.com"
    )
    driver.find_element(By.ID, "wiadomosc").send_keys(
        "Test message from Selenium"
    )

    driver.find_element(By.ID, "wyslij").click()

    success = wait_for(driver, By.ID, "sukces")

    assert success.text == "Dziękujemy za wiadomość."


def test_empty_contact(driver, clean_db):
    """REQ-KON-02/03/04: Empty fields cause three errors."""
    open_contact(driver)

    driver.find_element(By.ID, "wyslij").click()

    errors = driver.find_elements(
        By.CSS_SELECTOR,
        "#bledy li.blad"
    )

    expected = [
        "Podaj imię.",
        "Niepoprawny adres e-mail.",
        "Wpisz treść wiadomości."
    ]

    actual = [error.text for error in errors]

    assert actual == expected


@pytest.mark.xfail(
    reason="DEF-02: Contact page has an empty title",
    strict=True
)

def test_contact_title(driver):
    """REQ-UI-02: Contact page has a descriptive title."""
    open_contact(driver)

    assert driver.title == "SklepTO – kontakt"


@pytest.mark.xfail(
    reason="DEF-03: Contact image has no alternative text",
    strict=True
)

def test_contact_image_alt(driver):
    """REQ-UI-03: Every image has non-empty alt text."""
    open_contact(driver)

    images = driver.find_elements(By.TAG_NAME, "img")

    assert images, "No images found on contact page"

    for image in images:
        alt = image.get_attribute("alt")
        assert alt is not None and alt.strip() != ""


@pytest.mark.xfail(
    reason="DEF-04: Email field has no associated label",
    strict=True
)

def test_contact_email_label(driver):
    """REQ-UI-04: Email field has a connected label."""
    open_contact(driver)

    labels = driver.find_elements(
        By.CSS_SELECTOR,
        "label[for='email']"
    )

    assert len(labels) == 1
    assert "E-mail" in labels[0].text


@pytest.mark.xfail(
    reason="DEF-05: Email input uses type text instead of email",
    strict=True
)

def test_contact_email_type(driver):
    """REQ-UI-05: Email input must have type email."""
    open_contact(driver)

    email = driver.find_element(By.ID, "email")

    assert email.get_attribute("type") == "email"
