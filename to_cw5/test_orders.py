
import re
import pytest

from selenium.webdriver.common.by import By

from config import SKLEPTO_URL
from helpers import log_in, open_page, wait_for


def open_orders(driver):
    """Open the orders page."""
    return open_page(
        driver,
        f"{SKLEPTO_URL}/zamowienia.php",
        By.ID,
        "zamowienia"
    )


def login_as_jan(driver):
    """Log in as jan and open his orders."""
    message = log_in(driver, "jan", "Haslo123")
    assert message.text == "Zalogowano jako jan."
    open_orders(driver)


def get_order(driver, order_id):
    """Find an order row by its ID."""
    return driver.find_element(
        By.ID, f"zam-{order_id}"
    )


# REQ-ZAM-01
def test_orders_require_login(driver):
    """REQ-ZAM-01: Orders require authentication."""
    driver.get(f"{SKLEPTO_URL}/zamowienia.php")

    message = wait_for(driver, By.ID, "flash")

    assert message.text == (
        "Zaloguj się, aby zobaczyć zamówienia."
    )
    assert driver.current_url.endswith("logowanie.php")


# REQ-ZAM-02
def test_initial_orders(driver, clean_db):
    """REQ-ZAM-02: Jan has five initial orders."""
    login_as_jan(driver)

    expected = {
        1: ("100.00 zł", "Nowe"),
        2: ("250.00 zł", "Opłacone"),
        3: ("80.00 zł", "Wysłane"),
        4: ("40.00 zł", "Dostarczone"),
        5: ("60.00 zł", "Anulowane"),
    }

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "#zamowienia tr[id^='zam-']"
    )

    assert len(rows) == 5

    for order_id, (amount, status) in expected.items():
        row = get_order(driver, order_id)

        actual_amount = row.find_element(
            By.CSS_SELECTOR, "td.kwota"
        ).text

        actual_status = row.find_element(
            By.CSS_SELECTOR, "td.status"
        ).text

        assert actual_amount == amount
        assert actual_status == status


# REQ-ZAM-05
@pytest.mark.parametrize(
    "order_id,expected_actions",
    [
        (1, {"akcja-oplac", "akcja-anuluj"}),
        (2, {"akcja-wyslij", "akcja-anuluj"}),

        # DEF-09: Shipped orders must not have a cancel button.
        pytest.param(
            3,
            {"akcja-dostarcz"},
            marks=pytest.mark.xfail(
                reason=(
                    "DEF-09: Shipped order has "
                    "a forbidden cancel action"
                ),
                strict=True
            )
        ),

        (4, set()),
        (5, set()),
    ]
)
def test_available_actions(
    driver, clean_db, order_id, expected_actions
):
    """REQ-ZAM-05: Show only allowed order actions."""
    login_as_jan(driver)

    row = get_order(driver, order_id)

    buttons = row.find_elements(
        By.CSS_SELECTOR,
        "td.akcje button"
    )

    actual_actions = {
        button.get_attribute("class").split()[0]
        for button in buttons
    }

    assert actual_actions == expected_actions


# REQ-ZAM-03
def test_create_order(driver, clean_db):
    """REQ-ZAM-03: Create an order with NEW status."""
    login_as_jan(driver)

    amount = driver.find_element(By.ID, "kwota")
    amount.clear()
    amount.send_keys("123,45")

    driver.find_element(
        By.ID, "nowe-zamowienie"
    ).click()

    message = wait_for(driver, By.ID, "flash")

    match = re.fullmatch(
        r"Utworzono zamówienie #(\d+)\.",
        message.text
    )

    assert match is not None

    order_id = int(match.group(1))
    row = get_order(driver, order_id)

    assert row.get_attribute("data-status") == "NEW"

    assert row.find_element(
        By.CSS_SELECTOR, "td.kwota"
    ).text == "123.45 zł"


@pytest.mark.parametrize(
    "amount",
    ["0", "-10", "abc"]
)
def test_invalid_order_amount(driver, clean_db, amount):
    """REQ-ZAM-03: Reject invalid order amounts."""
    login_as_jan(driver)

    field = driver.find_element(By.ID, "kwota")
    field.clear()
    field.send_keys(amount)

    driver.find_element(
        By.ID, "nowe-zamowienie"
    ).click()

    message = wait_for(driver, By.ID, "flash")

    assert message.text == (
        "Kwota zamówienia musi być dodatnią liczbą."
    )

    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "#zamowienia tr[id^='zam-']"
    )
    assert len(rows) == 5


# REQ-ZAM-04 / REQ-ZAM-06
@pytest.mark.parametrize(
    "order_id,action,old_status,new_status,old_label,new_label",
    [
        (1, "oplac", "NEW", "PAID", "Nowe", "Opłacone"),
        (1, "anuluj", "NEW", "CANCELLED", "Nowe", "Anulowane"),
        (2, "wyslij", "PAID", "SHIPPED", "Opłacone", "Wysłane"),
        (2, "anuluj", "PAID", "CANCELLED", "Opłacone", "Anulowane"),
        (3, "dostarcz", "SHIPPED", "DELIVERED", "Wysłane", "Dostarczone"),
    ]
)
def test_valid_order_transition(
    driver, clean_db, order_id, action,
    old_status, new_status, old_label, new_label
):
    """REQ-ZAM-04/06: Valid transitions change order status."""
    login_as_jan(driver)

    row = get_order(driver, order_id)
    assert row.get_attribute("data-status") == old_status

    row.find_element(
        By.CSS_SELECTOR,
        f"button.akcja-{action}"
    ).click()

    message = wait_for(driver, By.ID, "flash")

    assert message.text == (
        f"Zamówienie #{order_id}: "
        f"{old_label} → {new_label}."
    )

    updated_row = get_order(driver, order_id)

    assert updated_row.get_attribute(
        "data-status"
    ) == new_status


# REQ-ZAM-07
@pytest.mark.parametrize(
    "order_id,status_label,expected_status",
    [
        (4, "Dostarczone", "DELIVERED"),

        # DEF-09: Cancelling a shipped order must be rejected.
        pytest.param(
            3,
            "Wysłane",
            "SHIPPED",
            marks=pytest.mark.xfail(
                reason="DEF-09: Shipped order can be cancelled",
                strict=True
            )
        ),
    ]
)
def test_forbidden_transition(
    driver, clean_db, order_id,
    status_label, expected_status
):
    """REQ-ZAM-07: Reject forbidden status transitions."""
    login_as_jan(driver)

    driver.get(
        f"{SKLEPTO_URL}/akcja.php"
        f"?id={order_id}&akcja=anuluj"
    )

    message = wait_for(driver, By.ID, "flash")

    assert message.text == (
        f"Niedozwolone przejście: "
        f"{status_label} → anuluj."
    )

    row = get_order(driver, order_id)

    assert row.get_attribute(
        "data-status"
    ) == expected_status


# REQ-ZAM-08
@pytest.mark.parametrize(
    "order_id",
    [6, 999]
)
def test_inaccessible_order(driver, clean_db, order_id):
    """REQ-ZAM-08: Reject foreign or missing orders."""
    login_as_jan(driver)

    driver.get(
        f"{SKLEPTO_URL}/akcja.php"
        f"?id={order_id}&akcja=oplac"
    )

    message = wait_for(driver, By.ID, "flash")

    assert message.text == "Nie znaleziono zamówienia."
