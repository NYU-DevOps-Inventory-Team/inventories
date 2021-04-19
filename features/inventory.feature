Feature: The inventory store service back-end
    As a Inventory Owner
    I need a RESTful catalog service
    So that I can keep track of all my inventory items

Background:
    Given the following inventory items
        | product_name | product_id | supplier_name | supplier_id | supplier_status | quantity | restock_threshold | unit_price |
        | product1 | 1 | supplier1 | 1 | enabled | 4 | 2 | 5.00 |
        | product2 | 2 | supplier2 | 2 | enabled | 5 | 1 | 10.00 |
        | product3 | 3 | supplier3 | 3 | disabled | 6 | 1 | 15.00 |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Inventory Item
    When I visit the "Home Page"
    And I set the "Product Name" to "product4"
    And I set the "Product ID" to "4"
    And I set the "Supplier Name" to "supplier4"
    And I set the "Supplier ID" to "4"
    And I set the "Quantity" to "10"
    And I set the "Restock Threshold" to "4"
    And I set the "Unit Price" to "20.00"
    And I select "Enabled" in the "Supplier Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"

    When I copy the "Inventory ID" field
    And I press the "Clear" button
    Then the "Inventory ID" field should be empty
    And the "Product Name" field should be empty
    And the "Product ID" field should be empty
    And the "Supplier Name" field should be empty
    And the "Supplier ID" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Threshold" field should be empty
    And the "Unit Price" field should be empty
    When I paste the "Inventory ID" field
    And I press the "Retrieve" button
    Then I should see "product4" in the "Product Name" field
    And I should see "4" in the "Product ID" field
    And I should see "supplier4" in the "Supplier Name" field
    And I should see "4" in the "Supplier ID" field
    And I should see "10" in the "Quantity" field
    And I should see "4" in the "Restock Threshold" field
    And I should see "20.00" in the "Unit Price" field
    And I should see "Enabled" in the "Supplier Status" field


# Scenario: List all pets
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: List all dogs
#     When I visit the "Home Page"
#     And I set the "Category" to "dog"
#     And I press the "Search" button
#     Then I should see "fido" in the results
#     And I should not see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: Update a Pet
#     When I visit the "Home Page"
#     And I set the "Name" to "fido"
#     And I press the "Search" button
#     Then I should see "fido" in the "Name" field
#     And I should see "dog" in the "Category" field
#     When I change "Name" to "Boxer"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see "Boxer" in the "Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see "Boxer" in the results
#     Then I should not see "fido" in the results
