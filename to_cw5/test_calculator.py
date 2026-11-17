
import pytest
from selenium.webdriver.common.by import By

from config import SKLEPTO_URL
from helpers import open_page, wait_for


def open_calculator(driver):
    """Open the SklepTO calculator."""
    open_page(
        driver,
        f"{SKLEPTO_URL}/kalkulator.php",
        By.ID,
        "form-kalkulator"
    )


def calculate(driver, amount, card=False, code="", shipping="kurier"):
    """Fill out and submit the calculator form."""
    open_calculator(driver)

    driver.find_element(By.ID, "wartosc").send_keys(amount)

    if card:
        driver.find_element(By.ID, "karta").click()

    if code:
        driver.find_element(By.ID, "kod").send_keys(code)

    driver.find_element(
        By.ID, f"dostawa-{shipping}"
    ).click()

    driver.find_element(By.ID, "oblicz").click()


@pytest.mark.parametrize(
    "amount,card,code,shipping,discount,delivery,total",
    [
        (
            "100", False, "", "kurier",
            "0%", "15.00 zł", "115.00 zł"
        ),
        (
            "100", True, "", "kurier",
            "10%", "0.00 zł", "90.00 zł"
        ),
        (
            "100", False, "STUDENT10", "paczkomat",
            "10%", "10.00 zł", "100.00 zł"
        ),

        # DEF-06: Calculator gives 20% instead of 15%
        pytest.param(
            "150", True, "student10", "kurier",
            "15%", "0.00 zł", "127.50 zł",
            marks=pytest.mark.xfail(
                reason="DEF-06: Calculator applies 20% instead of 15%",
                strict=True
            )
        ),

        (
            "200", False, "", "kurier",
            "0%", "0.00 zł", "200.00 zł"
        ),
        (
            "199.99", False, "", "paczkomat",
            "0%", "10.00 zł", "209.99 zł"
        ),
        (
            "100", False, "", "odbior",
            "0%", "0.00 zł", "100.00 zł"
        ),

        # DEF-06: Same bug with spaces around discount code
        pytest.param(
            "150", True, " STUDENT10 ", "kurier",
            "15%", "0.00 zł", "127.50 zł",
            marks=pytest.mark.xfail(
                reason="DEF-06: Calculator applies 20% instead of 15%",
                strict=True
            )
        ),
    ]
)
def test_calculator_results(
    driver, amount, card, code, shipping,
    discount, delivery, total
):
    """REQ-KAL-03/05/06/07/08: Verify calculation rules."""
    calculate(driver, amount, card, code, shipping)

    wait_for(driver, By.ID, "wynik")

    actual_discount = driver.find_element(
        By.ID, "rabat"
    ).text

    actual_delivery = driver.find_element(
        By.ID, "koszt-dostawy"
    ).text

    actual_total = driver.find_element(
        By.ID, "do-zaplaty"
    ).text

    assert actual_discount == discount
    assert actual_delivery == delivery
    assert actual_total == total


@pytest.mark.parametrize(
    "amount",
    ["0", "10000.01", "abc", "12.345"]
)
def test_invalid_amount(driver, amount):
    """REQ-KAL-02: Reject invalid order amounts."""
    calculate(driver, amount)

    errors = wait_for(driver, By.ID, "bledy")

    assert (
        "Wartość zamówienia musi być liczbą "
        "z zakresu 0,01–10000,00."
    ) in errors.text

    assert not driver.find_elements(By.ID, "wynik")


def test_invalid_discount_code(driver):
    """REQ-KAL-04: Reject an invalid discount code."""
    calculate(
        driver,
        amount="100",
        card=False,
        code="WRONGCODE",
        shipping="kurier"
    )

    message = wait_for(driver, By.ID, "kod-info")

    assert message.text == (
        "Nieprawidłowy kod rabatowy – został pominięty."
    )

    discount = driver.find_element(By.ID, "rabat")
    total = driver.find_element(By.ID, "do-zaplaty")

    assert discount.text == "0%"
    assert total.text == "115.00 zł"
