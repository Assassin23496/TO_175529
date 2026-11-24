from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from test_actions import loaded_paragraphs

INTERNET_URL = "https://the-internet.herokuapp.com"


def test_task1_loading_disappears(driver):
    driver.get(f"{INTERNET_URL}/dynamic_loading/1")

    wait = WebDriverWait(driver, 15)

    driver.find_element(By.CSS_SELECTOR, "#start button").click()

    loading = wait.until(
        EC.visibility_of_element_located((By.ID, "loading"))
    )

    assert loading.is_displayed()

    wait.until(EC.invisibility_of_element(loading))

    result = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
    )

    assert result.text == "Hello World!"


def test_task2_enable_input(driver):
    driver.get(f"{INTERNET_URL}/dynamic_controls")

    wait = WebDriverWait(driver, 15)

    input_field = driver.find_element(
        By.CSS_SELECTOR, "#input-example input"
    )

    assert not input_field.is_enabled()

    driver.find_element(
        By.CSS_SELECTOR, "#input-example button"
    ).click()

    input_field = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#input-example input")
        )
    )

    input_field.send_keys("Selenium")

    assert input_field.get_attribute("value") == "Selenium"


def test_task3_prompt_cancel(driver):
    driver.get(f"{INTERNET_URL}/javascript_alerts")

    driver.find_element(
        By.XPATH, "//button[text()='Click for JS Prompt']"
    ).click()

    alert = WebDriverWait(driver, 5).until(
        EC.alert_is_present()
    )

    alert.dismiss()

    result = driver.find_element(By.ID, "result").text

    assert result == "You entered: null"


def test_task4_iframe_editor(driver):
    driver.get(f"{INTERNET_URL}/iframe")

    wait = WebDriverWait(driver, 15)

    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.ID, "mce_0_ifr")
        )
    )

    editor = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "tinymce")
        )
    )

    text = editor.text
    print("Текст редактора:", text)

    assert text == "Your content goes here."

    driver.switch_to.default_content()


class ScrollUntilFiveParagraphs:
    def __call__(self, driver):
        count = loaded_paragraphs(driver)
        print("Загружено абзацев:", count)

        if count >= 5:
            return True

        ActionChains(driver).scroll_by_amount(0, 700).perform()
        return False


def test_task5_infinite_scroll(driver):
    driver.get(f"{INTERNET_URL}/infinite_scroll")

    wait = WebDriverWait(driver, 40)

    wait.until(ScrollUntilFiveParagraphs())

    assert loaded_paragraphs(driver) >= 5
