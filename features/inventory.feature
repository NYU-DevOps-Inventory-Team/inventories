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
    And I set the "product_name" to "product4"
    And I set the "product_id" to "4"
    And I set the "supplier_name" to "supplier4"
    And I set the "supplier_id" to "4"
    And I set the "quantity" to "10"
    And I set the "restock_threshold" to "4"
    And I set the "unit_price" to "20.00"
    And I select "Enabled" in the "supplier_status" dropdown
    And I press the "Create" button
    Then I should see the message "Item Created Successfully"

    When I copy the "inventory_id" field
    And I press the "Clear" button
    Then the "inventory_id" field should be empty
    And the "product_name" field should be empty
    And the "product_id" field should be empty
    And the "supplier_name" field should be empty
    And the "supplier_id" field should be empty
    And the "quantity" field should be empty
    And the "restock_threshold" field should be empty
    And the "unit_price" field should be empty

    When I paste the "inventory_id" field
    And I press the "Retrieve" button
    Then I should see "product4" in the "product_name" field
    And I should see "4" in the "product_id" field
    And I should see "supplier4" in the "supplier_name" field
    And I should see "4" in the "supplier_id" field
    And I should see "10" in the "quantity" field
    And I should see "4" in the "restock_threshold" field
    And I should see "20" in the "unit_price" field
    And I should see "enabled" in the "supplier_status" field

 Scenario: List all inventory items
     When I visit the "Home Page"
     And I press the "Search" button
     Then I should see "product1" in the results
     And I should see "product2" in the results
     And I should see "product3" in the results
     And I should not see "product4" in the results

 Scenario: List all suppliers
     When I visit the "Home Page"
     And I set the "supplier_name" to "supplier1"
     And I press the "Search" button
     Then I should see "supplier1" in the results
     And I should not see "supplier2" in the results
     And I should not see "supplier3" in the results

 Scenario: Update an inventory item
     When I visit the "Home Page"
     And I set the "product_name" to "product1"
     And I press the "Search" button
     Then I should see "product1" in the "product_name" field
     And I should see "supplier1" in the "supplier_name" field
     And I should see "1" in the "supplier_id" field
     And I should see "4" in the "quantity" field
     And I should see "2" in the "restock_threshold" field
     And I should see "5" in the "unit_price" field
     And I should see "enabled" in the "supplier_status" field

     When I change "product_name" to "product5"
     And I press the "Update" button
     Then I should see the message "Success"

     When I copy the "inventory_id" field
     And I press the "Clear" button
     And I paste the "inventory_id" field
     And I press the "Retrieve" button
     Then I should see "product5" in the "product_name" field

     When I press the "Clear" button
     And I press the "Search" button
     Then I should see "product5" in the results
     Then I should not see "product1" in the results
