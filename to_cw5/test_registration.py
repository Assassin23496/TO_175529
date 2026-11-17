
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import SKLEPTO_URL
from helpers import open_page, log_in


def open_registration(driver):
    """Open the SklepTO registration form."""
    return open_page(
        driver,
        f"{SKLEPTO_URL}/rejestracja.php",
        By.ID,
        "form-rejestracja"
    )


def register(
    driver,
    login="nowyuser",
    email="nowy@example.com",
    age="25",
    password="Haslo123",
    confirmation=None,
    accept_terms=True
):
    """Fill out and submit the registration form."""
    form = open_registration(driver)

    values = {
        "login": login,
        "email": email,
        "wiek": age,
        "haslo": password,
        "haslo2": (
            password if confirmation is None else confirmation
        )
    }

    for field_id, value in values.items():
        driver.find_element(By.ID, field_id).send_keys(value)

    if accept_terms:
        driver.find_element(By.ID, "regulamin").click()

    driver.find_element(By.ID, "zarejestruj").click()

    WebDriverWait(driver, 10).until(
        EC.staleness_of(form)
    )


def get_errors(driver):
    """Return validation errors indexed by field name."""
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        "#bledy li.blad"
    )

    return {
        element.get_attribute("data-pole"): element.text
        for element in elements
    }


def test_registration_fields(driver):
    """REQ-REJ-01: All required form controls exist."""
    open_registration(driver)

    fields = [
        "login", "email", "wiek",
        "haslo", "haslo2", "regulamin"
    ]

    for field_id in fields:
        driver.find_element(By.ID, field_id)

        labels = driver.find_elements(
            By.CSS_SELECTOR,
            f"label[for='{field_id}']"
        )
        assert len(labels) == 1

    driver.find_element(By.ID, "zarejestruj")


def test_valid_registration(driver, clean_db):
    """REQ-REJ-10: A valid account can be created."""
    register(driver)

    success = driver.find_element(By.ID, "sukces")

    assert success.text == (
        "Konto zostało utworzone. Możesz się zalogować."
    )

    for field_id in ("login", "email", "wiek"):
        field = driver.find_element(By.ID, field_id)
        assert field.get_attribute("value") == ""

    message = log_in(driver, "nowyuser", "Haslo123")

    assert message.text == "Zalogowano jako nowyuser."



@pytest.mark.parametrize(
    "login",
    [
        pytest.param(
            "Abcd",
            marks=pytest.mark.xfail(
                reason="DEF-07: Uppercase login is accepted",
                strict=True
            )
        ),
        "ab",
        "a" * 21,
        "bad-login"
    ]
)

def test_invalid_login_format(driver, clean_db, login):
    """REQ-REJ-02: Login must match lowercase rules."""
    register(driver, login=login)

    errors = get_errors(driver)

    assert errors.get("login") == (
        "Login musi mieć od 3 do 20 znaków "
        "(małe litery, cyfry, _)."
    )


def test_duplicate_login(driver, clean_db):
    """REQ-REJ-03: Existing login must be rejected."""
    register(driver, login="jan")

    errors = get_errors(driver)

    assert errors.get("login") == "Login jest już zajęty."


def test_invalid_email(driver, clean_db):
    """REQ-REJ-04: Invalid email must be rejected."""
    register(driver, email="invalid-email")

    errors = get_errors(driver)

    assert errors.get("email") == (
        "Niepoprawny adres e-mail."
    )



@pytest.mark.parametrize(
    "age",
    [
        "17",
        pytest.param(
            "100",
            marks=pytest.mark.xfail(
                reason="DEF-08: Age 100 is incorrectly accepted",
                strict=True
            )
        ),
        "101"
    ]
)

def test_invalid_age(driver, clean_db, age):
    """REQ-REJ-05: Age must be between 18 and 99."""
    register(driver, age=age)

    errors = get_errors(driver)

    assert errors.get("wiek") == (
        "Wiek musi być liczbą całkowitą "
        "z zakresu 18–99."
    )


@pytest.mark.parametrize(
    "password",
    [
        "short1",
        "onlyletters",
        "1234567890"
    ]
)
def test_invalid_password(driver, clean_db, password):
    """REQ-REJ-06: Password must meet security rules."""
    register(driver, password=password)

    errors = get_errors(driver)

    assert errors.get("haslo") == (
        "Hasło musi mieć od 8 do 20 znaków "
        "i zawierać literę oraz cyfrę."
    )


def test_password_mismatch(driver, clean_db):
    """REQ-REJ-07: Password confirmation must match."""
    register(
        driver,
        password="Haslo123",
        confirmation="Other123"
    )

    errors = get_errors(driver)

    assert errors.get("haslo2") == (
        "Hasła nie są identyczne."
    )


def test_terms_required(driver, clean_db):
    """REQ-REJ-08: Terms must be accepted."""
    register(driver, accept_terms=False)

    errors = get_errors(driver)

    assert errors.get("regulamin") == (
        "Musisz zaakceptować regulamin."
    )


def test_all_errors_and_preserved_values(driver, clean_db):
    """REQ-REJ-09: Show all errors and preserve inputs."""
    register(
        driver,
        login="A",
        email="invalid",
        age="17",
        password="abc",
        confirmation="different",
        accept_terms=False
    )

    errors = get_errors(driver)

    expected_fields = {
        "login", "email", "wiek",
        "haslo", "haslo2", "regulamin"
    }

    assert set(errors) == expected_fields

    assert driver.find_element(
        By.ID, "login"
    ).get_attribute("value") == "A"

    assert driver.find_element(
        By.ID, "email"
    ).get_attribute("value") == "invalid"

    assert driver.find_element(
        By.ID, "wiek"
    ).get_attribute("value") == "17"

    assert not driver.find_elements(By.ID, "sukces")

