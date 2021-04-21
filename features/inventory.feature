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


# Scenario: List all inventory items
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see "product1" in the results
#     And I should see "product2" in the results
#     And I should see "product3" in the results
#     And I should not see "product4" in the results

# Scenario: List all suppliers
#     When I visit the "Home Page"
#     And I set the "Supplier Name" to "supplier1"
#     And I press the "Search" button
#     Then I should see "supplier1" in the results
#     And I should not see "supplier2" in the results
#     And I should not see "supplier3" in the results

# Scenario: Update an inventory item
#     When I visit the "Home Page"
#     And I set the "Product Name" to "product1"
#     And I press the "Search" button
#     Then I should see "product1" in the "Product Name" field
#     And I should see "supplier1" in the "Supplier Name" field
#     And I should see "1" in the "Supplier ID" field
#     And I should see "enabled" in the "Supplier Status" field
#     And I should see "4" in the "Quantity" field
#     And I should see "2" in the "Restock Threshold" field
#     And I should see "5.00" in the "Unit Price" field
#     When I change "Product Name" to "product5"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Inventory ID" field
#     And I press the "Clear" button
#     And I paste the "Inventory ID" field
#     And I press the "Retrieve" button
#     Then I should see "product5" in the "Product Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see "product5" in the results
#     Then I should not see "product1" in the results
