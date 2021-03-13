"""
Test cases for InventoryModel Model

"""
import logging
import unittest
import os
from service.models import InventoryModel, DataValidationError, db


######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryModel(unittest.TestCase):
    """ Test Cases for InventoryModel Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        pass

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ Test something """
        self.assertTrue(True)

    def test_create_a_product_in_inventory(self):
        """ Create a pet and assert that it exists """
        product_in_inventory = InventoryModel(
            # id=123,
            name="test product",
            quantity=100,
            restock_threshold=50,
            supplier_name="test supplier",
            supplier_id=123,
            unit_price=12.50,
        )
        self.assertTrue(product_in_inventory is not None)
        self.assertEqual(product_in_inventory.id, None)
        self.assertEqual(product_in_inventory.name, "test product")
        self.assertEqual(product_in_inventory.quantity, 100)
        self.assertEqual(product_in_inventory.supplier_name, "test supplier")
        self.assertEqual(product_in_inventory.supplier_id, 123)
        self.assertEqual(product_in_inventory.unit_price, 12.50)
        product_in_inventory = InventoryModel(
            id=123,
            name="test product",
            quantity=100,
            restock_threshold=50,
            supplier_name="test supplier",
            supplier_id=123,
            unit_price=12.50,
        )
        self.assertEqual(product_in_inventory.available, False)
        self.assertEqual(product_in_inventory.gender, Gender.Female)
