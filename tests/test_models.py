"""
Test cases for InventoryItem Model

"""
import logging
import unittest
import os

from flask_api import status
from werkzeug.exceptions import NotFound

from service.models import InventoryItem, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)


def _create_test_inventory_item(product_id, product_name, quantity, restock_threshold, supplier_name, supplier_id,
                                unit_price, supplier_status):
    """create inventory items in bulk """
    return InventoryItem(
        product_id=product_id,
        product_name=product_name,
        quantity=quantity,
        restock_threshold=restock_threshold,
        supplier_name=supplier_name,
        supplier_id=supplier_id,
        supplier_status=supplier_status,
        unit_price=unit_price
    )


######################################################################
#  I N V E N T O R Y   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryItem(unittest.TestCase):
    """ Test Cases for InventoryItem Model """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        InventoryItem.init_db(app)

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_test_inventory_items(self, count):
        """ Factory method to create inventories in bulk """
        inventory_items = []
        for _ in range(count):
            test_item = _create_test_inventory_item(
                product_id=123, product_name="test product", quantity=100, restock_threshold=50,
                supplier_name="test supplier", supplier_id=123, unit_price=12.50, supplier_status="enabled")
            test_item.create()
            inventory_items.append(test_item)
        return inventory_items

    ######################################################################
    #  T E S T   C A S E S
    #####################################################################
    def test_create_inventory_item(self):
        """ Create an inventory item and add it to the database """
        test_item = InventoryItem.all()
        self.assertEqual(test_item, [])
        test_item = _create_test_inventory_item(
            product_id=123, product_name="test product", quantity=100, restock_threshold=50,
            supplier_name="test supplier", supplier_id=123, unit_price=12.50, supplier_status="enabled"
        )
        self.assertTrue(test_item is not None)
        self.assertEqual(test_item.inventory_id, None)
        test_item.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(test_item.inventory_id, 1)
        test_item = InventoryItem.all()
        self.assertEqual(len(test_item), 1)

    def test_find_inventory_item(self):
        """ Find an inventory item by ID """
        test_items = self._create_test_inventory_items(3)
        logging.debug(test_items)
        # make sure they got saved
        self.assertEqual(len(InventoryItem.all()), 3)
        # find the 2nd inventory item in the list
        found_item = InventoryItem.find(test_items[1].inventory_id)
        self.assertIsNot(found_item, None)
        self.assertEqual(found_item.inventory_id, test_items[1].inventory_id)
        self.assertEqual(found_item.product_name, test_items[1].product_name)
        self.assertEqual(found_item.quantity, test_items[1].quantity)

    def test_find_by_supplier_name(self):
        """ Find inventory item by supplier name """
        inventory_items = [
            _create_test_inventory_item(
                product_id=123, product_name="test product1", quantity=100, restock_threshold=50,
                supplier_name="test supplier1", supplier_id=123, unit_price=12.50),
            _create_test_inventory_item(
                product_id=123, product_name="test product2", quantity=100, restock_threshold=50,
                supplier_name="test supplier2", supplier_id=125, unit_price=12.50),
            _create_test_inventory_item(
                product_id=123, product_name="test product3", quantity=100, restock_threshold=50,
                supplier_name="test supplier3", supplier_id=127, unit_price=12.50)]
        for inventory_item in inventory_items:
            inventory_item.create()
        found_items = InventoryItem.find_by_supplier_name("test supplier1")
        #added this line below
        self.assertEqual(found_items[0].supplier_id, inventory_items[0].supplier_id)
        #copied from "find_by_name" test
        self.assertEqual(found_items[0].inventory_id, inventory_items[0].inventory_id)
        self.assertEqual(found_items[0].product_name, inventory_items[0].product_name)
        self.assertEqual(found_items[0].quantity, inventory_items[0].quantity)

    def test_find_by_product_name(self):
        """ Find an inventory item by Name """
        inventory_items = [
            _create_test_inventory_item(
                product_id=123, product_name="test product", quantity=100, restock_threshold=50,
                supplier_name="test supplier1", supplier_id=123, unit_price=12.50, supplier_status="enabled"),
            _create_test_inventory_item(
                product_id=123, product_name="test product2", quantity=100, restock_threshold=50,
                supplier_name="test supplier2", supplier_id=125, unit_price=12.50, supplier_status="enabled"),
            _create_test_inventory_item(
                product_id=123, product_name="test product3", quantity=100, restock_threshold=50,
                supplier_name="test supplier3", supplier_id=127, unit_price=12.50, supplier_status="enabled")]
        for inventory_item in inventory_items:
            inventory_item.create()
        found_items = InventoryItem.find_by_product_name("test product1")
        self.assertEqual(found_items[0].inventory_id, inventory_items[0].inventory_id)
        self.assertEqual(found_items[0].product_name, inventory_items[0].product_name)
        self.assertEqual(found_items[0].quantity, inventory_items[0].quantity)

    def test_find_by_supplier_id(self):
        """ Find an inventory item by supplier id """
        inventory_items = [
            _create_test_inventory_item(
                product_id=123, product_name="test product", quantity=100, restock_threshold=50,
                supplier_name="test supplier1", supplier_id=123, unit_price=12.50, supplier_status="enabled"),
            _create_test_inventory_item(
                product_id=124, product_name="test product2", quantity=100, restock_threshold=50,
                supplier_name="test supplier2", supplier_id=125, unit_price=12.50, supplier_status="enabled"),
            _create_test_inventory_item(
                product_id=125, product_name="test product2.5", quantity=100, restock_threshold=50,
                supplier_name="test supplier2", supplier_id=125, unit_price=12.50, supplier_status="enabled"),
            _create_test_inventory_item(
                product_id=127, product_name="test product3", quantity=100, restock_threshold=50,
                supplier_name="test supplier3", supplier_id=127, unit_price=12.50, supplier_status="enabled")]
        for inventory_item in inventory_items:
            inventory_item.create()

        matches = [item.serialize() for item in inventory_items if item.supplier_id == 125]

        found_items = InventoryItem.find_by_supplier_id("125")
        found_items = [item.serialize() for item in found_items]

        self.assertEqual(found_items, matches)

    def test_update_a_inventory_item(self):
        """ Update an inventory item """
        test_item = self._create_test_inventory_items(1)[0]
        logging.debug(test_item)
        logging.debug(test_item)
        self.assertEqual(test_item.inventory_id, 1)
        # Change it an save it
        test_item.supplier_name = "new supplier"
        original_id = test_item.inventory_id
        test_item.save()
        self.assertEqual(test_item.inventory_id, original_id)
        self.assertEqual(test_item.supplier_name, "new supplier")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        found_items = InventoryItem.all()
        self.assertEqual(len(found_items), 1)
        self.assertEqual(found_items[0].inventory_id, 1)
        self.assertEqual(found_items[0].supplier_name, "new supplier")

    def test_delete_a_inventory_item(self):
        """ Delete an inventory item """
        test_item = self._create_test_inventory_items(1)[0]
        self.assertEqual(len(InventoryItem.all()), 1)
        # delete the inventory item and make sure it isn't in the database
        test_item.delete()
        self.assertEqual(len(InventoryItem.all()), 0)

    def test_serialize_a_inventory_item(self):
        """ Test serialization of an inventory item """
        test_item = self._create_test_inventory_items(1)[0]
        data = test_item.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("inventory_id", data)
        self.assertEqual(data["inventory_id"], test_item.inventory_id)
        self.assertIn("product_name", data)
        self.assertEqual(data["product_name"], test_item.product_name)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], test_item.quantity)
        self.assertIn("supplier_name", data)
        self.assertEqual(data["supplier_name"], test_item.supplier_name)
        self.assertIn("supplier_id", data)
        self.assertEqual(data["supplier_id"], test_item.supplier_id)

    def test_deserialize_a_inventory_item(self):
        """ Test deserialization of an inventory item """
        data = {
            "inventory_id": 1,
            "product_id": 123,
            "product_name": "test product1",
            "quantity": 100,
            "restock_threshold": 200,
            "supplier_id": 123,
            "supplier_name": "supplier test",
            "supplier_status": "enabled",
            "unit_price": 12.50,
        }
        inventory_item = InventoryItem()
        inventory_item.deserialize(data)
        self.assertNotEqual(inventory_item, None)
        self.assertEqual(inventory_item.inventory_id, None)
        self.assertEqual(inventory_item.product_name, "test product1")
        self.assertEqual(inventory_item.quantity, 100)
        self.assertEqual(inventory_item.supplier_id, 123)
        self.assertEqual(inventory_item.unit_price, 12.50)

    def test_deserialize_missing_data(self):
        """ Test deserialization of an inventory item """
        data = {"id": 1, "product_name": "test product2", "quantity": 100}
        inventory_item = InventoryItem()
        self.assertRaises(DataValidationError, inventory_item.deserialize, data)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        inventory_item = InventoryItem()
        self.assertRaises(DataValidationError, inventory_item.deserialize, data)

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        test_items = self._create_test_inventory_items(5)
        found_item = InventoryItem.find_or_404(test_items[1].inventory_id)
        self.assertIsNot(found_item, None)
        self.assertEqual(found_item.inventory_id, test_items[1].inventory_id)
        self.assertEqual(found_item.product_name, test_items[1].product_name)
        self.assertEqual(found_item.quantity, test_items[1].quantity)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, InventoryItem.find_or_404, 0)
