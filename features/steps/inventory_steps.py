"""
Inventory Steps

Steps file for inventory.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
from os import getenv
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions


@given('the following inventory items')
def step_impl(context):
    """ Delete all Inventory Items and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the items and delete them one by one
    context.resp = requests.get(context.base_url + '/inventory', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for item in context.resp.json():
        context.resp = requests.delete(context.base_url + '/inventory/' + str(item["inventory_id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)

    # load the database with new inventory items
    create_url = context.base_url + '/inventory'
    for row in context.table:
        data = {
            "product_name": row['product_name'],
            "product_id": row['product_id'],
            "supplier_name": row['supplier_name'],
            "supplier_id": row['supplier_id'],
            "restock_threshold": row['restock_threshold'],
            "quantity": row['quantity'],
            "unit_price": row['unit_price'],
            "supplier_status": row['supplier_status']
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@when('I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    # Uncomment next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)


@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    expect(element.first_selected_option.text).to_equal(text)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute('value')).to_be(u'')


# ##################################################################
# # These two function simulate copy and paste
# ##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


# ##################################################################
# # This code works because of the following naming convention:
# # The buttons have an id in the html hat is the button text
# # in lowercase followed by '-btn' so the Clean button has an id of
# # id='clear-btn'. That allows us to lowercase the name and add '-btn'
# # to get the element id of any button
# ##################################################################

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()


@then('I should see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    # expect(element.text).to_contain(name)
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)


@then('I should see the message "{message}"')
def step_impl(context, message):
    element = context.driver.find_element_by_id('flash_message')
    # expect(element.text).to_contain(message)
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)


# ##################################################################
# # This code works because of the following naming convention:
# # The id field for text input in the html is the element name
# # prefixed by ID_PREFIX so the Name field has an id='pet_name'
# # We can then lowercase the name and prefix with pet_ to get the id
# ##################################################################

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    # expect(element.get_attribute('value')).to_equal(text_string)
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)
