import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager

# App URL = Kubernetes NodePort (from service.yaml / kubectl get services)
BASE_URL = os.getenv("BASE_URL", "http://localhost:30120/")

# Fixture: open Chrome before each test, close it after
@pytest.fixture
def setup_teardown():
    options = Options()
    options.add_argument("--headless=new")   # needed when Jenkins runs it
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    yield driver
    driver.quit()

# Helper: read the alert text and close the alert
def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text

# Test 1: Empty username
def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Username cannot be empty."

# Test 2: Empty password
def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").send_keys("Pranathi")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Password cannot be empty."

# Test 3: Password shorter than 6 characters
def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").send_keys("Pranathi")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Password must be at least 6 characters long."

# Test 4: Valid input -> greeting page
def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "username").send_keys("Pranathi")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    assert "/submit" in driver.current_url
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Hello, Pranathi! Welcome to the website" in body_text
