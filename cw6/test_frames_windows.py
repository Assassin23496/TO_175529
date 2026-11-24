"""Frames and browser windows."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import INTERNET_URL


def body_text(driver):
    return driver.find_element(By.TAG_NAME, "body").text


def h3_text(driver):
    return driver.find_element(By.TAG_NAME, "h3").text




def test_nested_frames(driver):
    driver.get(f"{INTERNET_URL}/nested_frames")
    wait = WebDriverWait(driver, 15)

    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.NAME, "frame-top")
        )
    )

    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.NAME, "frame-left")
        )
    )
    assert body_text(driver) == "LEFT"

    driver.switch_to.parent_frame()
    driver.switch_to.frame(1)
    assert body_text(driver) == "MIDDLE"

    driver.switch_to.default_content()
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.NAME, "frame-bottom")
        )
    )
    assert body_text(driver) == "BOTTOM"




def test_new_window(driver):
    driver.get(f"{INTERNET_URL}/windows")

    main = driver.current_window_handle

    driver.find_element(By.LINK_TEXT, "Click Here").click()

    WebDriverWait(driver, 5).until(
        EC.number_of_windows_to_be(2)
    )

    new = [h for h in driver.window_handles if h != main][0]

    driver.switch_to.window(new)
    assert h3_text(driver) == "New Window"

    driver.close()

    driver.switch_to.window(main)
    assert h3_text(driver) == "Opening a new window"

