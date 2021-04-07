"""
TestInventoryItem API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from flask_api import status  # HTTP Status Codes
from service.models import db, InventoryItem
from service.routes import app, init_db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)


def _create_test_inventory_item(product_id, product_name, quantity, restock_threshold, supplier_name, supplier_id,
                                unit_price):
    """create inventory items in bulk """
    return InventoryItem(
        product_id=product_id,
        product_name=product_name,
        quantity=quantity,
        restock_threshold=restock_threshold,
        supplier_name=supplier_name,
        supplier_id=supplier_id,
        unit_price=unit_price
    )


######################################################################
#  T E S T   C A S E S
######################################################################
class TestInventoryServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_test_inventory_items(self, count):
        """ Factory method to create inventories in bulk """
        inventory_items = []
        for _ in range(count):
            test_item = _create_test_inventory_item(
                product_id=123, product_name="test product", quantity=100, restock_threshold=50,
                supplier_name="test supplier", supplier_id=123, unit_price=12.50)

            # TODO: this is bad practice--hopefully the factory stuff will resolve. you should not depend on a different
            #  route working when testing some other route. in the case of the Create endpoint breaking, every other
            #  endpoint that uses this helper will also break and result in many false negatives in your tests. bad.
            resp = self.app.post(
                "/inventory", json=test_item.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test inventory item"
            )
            new_inventory_item = resp.get_json()
            test_item.inventory_id = new_inventory_item["inventory_id"]
            inventory_items.append(test_item)
        return inventory_items

    ######################################################################
    #  ROUTE TESTS
    ######################################################################

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Inventory REST API Service")

    def test_create_new_inventory_item(self):
        """ Create a new Inventory item """
        test_item = _create_test_inventory_item(
            product_id=123, product_name="test product", quantity=100, restock_threshold=50,
            supplier_name="test supplier", supplier_id=123, unit_price=12.50
        )
        logging.debug(test_item)
        resp = self.app.post(
            "/inventory", json=test_item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_inventory_item = resp.get_json()
        self.assertEqual(
            new_inventory_item["product_name"], test_item.product_name, "Names do not match")
        self.assertEqual(
            new_inventory_item["quantity"], test_item.quantity, "Quantities do not match")
        self.assertEqual(
            new_inventory_item["restock_threshold"], test_item.restock_threshold,
            "Restock threshold does not match")
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_inventory_item = resp.get_json()
        self.assertEqual(
            new_inventory_item["product_name"], test_item.product_name, "Names do not match")
        self.assertEqual(
            new_inventory_item["quantity"], test_item.quantity, "Quantities do not match")
        self.assertEqual(
            new_inventory_item["restock_threshold"], test_item.restock_threshold,
            "Restock Threshold does not match")

    def test_list_inventory_items(self):
        """ Get a list of inventory items without any filter"""
        self._create_test_inventory_items(5)
        resp = self.app.get("/inventory")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_query_inventory_items_list_by_supplier_name(self):
        """ Query Inventory Items by Supplier Name """
        test_items = self._create_test_inventory_items(10)
        desired_supplier_name = test_items[0].supplier_name
        items_with_desired_supplier_name = [item for item in test_items if item.supplier_name == desired_supplier_name]

        # hit the route
        resp = self.app.get(
            "/inventory", query_string="supplier_name={}".format(desired_supplier_name)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(items_with_desired_supplier_name))

        # check the data
        for item in data:
            self.assertEqual(item["supplier_name"], desired_supplier_name)

    def test_query_inventory_items_list_by_product_name(self):
        """ Query Inventory Items by Product Name """
        test_items = self._create_test_inventory_items(10)
        desired_product_name = test_items[0].product_name
        items_with_desired_product_name = [item for item in test_items if item.product_name == desired_product_name]

        # hit the route
        resp = self.app.get(
            "/inventory", query_string="product_name={}".format(desired_product_name)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(items_with_desired_product_name))

        # check the data
        for item in data:
            self.assertEqual(item["product_name"], desired_product_name)

    def test_get_inventory_item(self):
        """ Get a single Inventory item """
        # get the id of the inventory item
        test_item = _create_test_inventory_item(
            product_id=123, product_name="test product", quantity=100, restock_threshold=50,
            supplier_name="test supplier", supplier_id=123, unit_price=12.50
        )
        test_item.create()
        resp = self.app.get(
            "/inventory/{}".format(test_item.inventory_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["product_name"], test_item.product_name)

    def test_get_inventory_item_not_found(self):
        """ Get an inventory item that's not found """
        resp = self.app.get("/inventory/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_inventory_item(self):
        """ Update an existing product inventory """
        # create a product to update
        test_item = _create_test_inventory_item(
            product_id=123, product_name="test product", quantity=100, restock_threshold=50,
            supplier_name="test supplier", supplier_id=123, unit_price=12.50
        )
        resp = self.app.post(
            "/inventory", json=test_item.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the inventory item
        updated_item = resp.get_json()
        logging.debug(updated_item)
        updated_item["supplier_name"] = "unknown"
        resp = self.app.put(
            "/inventory/{}".format(updated_item["inventory_id"]),
            json=updated_item,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_item = resp.get_json()
        self.assertEqual(updated_item["supplier_name"], "unknown")

    def test_delete_inventory_item(self):
        """ Delete an inventory item """
        test_item = self._create_test_inventory_items(1)[0]
        resp = self.app.delete(
            "/inventory/{}".format(test_item.inventory_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/inventory/{}".format(test_item.inventory_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #  BAD ROUTE TESTS
    ######################################################################
    def test_bad_request(self):
        """ Send wrong media type """
        resp = self.app.post(
            "/inventory",
            json={"product_name": "not enough data"},
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """ Send wrong media type """
        test_item = self._create_test_inventory_items(1)[0]
        resp = self.app.post(
            "/inventory",
            json=test_item.serialize(),
            content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """ Make an illegal method call """
        resp = self.app.put(
            "/inventory",
            json={"not": "today"},
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
