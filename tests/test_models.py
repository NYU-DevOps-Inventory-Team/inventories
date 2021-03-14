"""
Test cases for InventoryModel Model

"""
import logging
import unittest
import os
from service.models import InventoryModel, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  I N V E N T O R I E S   M O D E L   T E S T   C A S E S
######################################################################
def _test_create_product_in_inventory(name, quantity, restock_threshold, supplier_name, supplier_id, unit_price):
    """create products in inventory in bulk """
    return InventoryModel(
        name=name,
        quantity=quantity,
        restock_threshold=restock_threshold,
        supplier_name=supplier_name,
        supplier_id=supplier_id,
        unit_price=unit_price
    )


class TestInventoryModel(unittest.TestCase):
    """ Test Cases for InventoryModel Model """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        InventoryModel.init_db(app)

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_product_in_inventory(self):
        """ Create a product in inventory and assert that it exists """
        product_in_inventory = _test_create_product_in_inventory(
            name="test product", quantity=100, restock_threshold=50,
            supplier_name="test supplier", supplier_id=123, unit_price=12.50)
        self.assertTrue(product_in_inventory is not None)
        self.assertEqual(product_in_inventory.product_in_inventory_id, None)
        self.assertEqual(product_in_inventory.name, "test product")
        self.assertEqual(product_in_inventory.quantity, 100)
        self.assertEqual(product_in_inventory.supplier_name, "test supplier")
        self.assertEqual(product_in_inventory.supplier_id, 123)
        self.assertEqual(product_in_inventory.unit_price, 12.50)

        # test product in inventory without optional field supplier name

        product_in_inventory = _test_create_product_in_inventory(
            name="test product", quantity=100, restock_threshold=50,
            supplier_name=None, supplier_id=123, unit_price=12.50)
        self.assertTrue(product_in_inventory is not None)
        self.assertEqual(product_in_inventory.product_in_inventory_id, None)
        self.assertEqual(product_in_inventory.name, "test product")
        self.assertEqual(product_in_inventory.quantity, 100)
        self.assertEqual(product_in_inventory.supplier_name, None)
        self.assertEqual(product_in_inventory.supplier_id, 123)
        self.assertEqual(product_in_inventory.unit_price, 12.50)

    def test_add_product_in_inventory(self):
        """ Create a product in inventory and add it to the database """
        product_in_inventory = InventoryModel.all()
        self.assertEqual(product_in_inventory, [])
        product_in_inventory = _test_create_product_in_inventory(
            name="test product", quantity=100, restock_threshold=50,
            supplier_name="test supplier", supplier_id=123,
            unit_price=12.50)
        self.assertTrue(product_in_inventory is not None)
        self.assertEqual(product_in_inventory.product_in_inventory_id, None)
        product_in_inventory.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(product_in_inventory.product_in_inventory_id, 1)
        product_in_inventory = InventoryModel.all()
        self.assertEqual(len(product_in_inventory), 1)

        # test get product in inventory by id

    def test_find_product_in_inventory(self):
        """ Find a product in inventory by ID """
        products_in_inventory = [_test_create_product_in_inventory(name="test product1", quantity=100, restock_threshold=50,
                                                   supplier_name="test supplier1", supplier_id=123, unit_price=12.50),
                 _test_create_product_in_inventory(name="test product2", quantity=100, restock_threshold=50,
                                                   supplier_name="test supplier2", supplier_id=125, unit_price=12.50),
                 _test_create_product_in_inventory(name="test product3", quantity=100, restock_threshold=50,
                                                   supplier_name="test supplier3", supplier_id=127, unit_price=12.50)]
        for product_in_inventory in products_in_inventory:
            product_in_inventory.create()
        logging.debug(products_in_inventory)
        # make sure they got saved
        self.assertEqual(len(InventoryModel.all()), 3)
        # find the 2nd pet in the list
        found_product_in_inventory = InventoryModel.find(products_in_inventory[1].product_in_inventory_id)
        self.assertIsNot(found_product_in_inventory, None)
        self.assertEqual(found_product_in_inventory.product_in_inventory_id, products_in_inventory[1].product_in_inventory_id)
        self.assertEqual(found_product_in_inventory.name, products_in_inventory[1].name)
        self.assertEqual(found_product_in_inventory.quantity, products_in_inventory[1].quantity)
