"""
TestInventoryModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db, InventoryModel
from service.routes import app, init_db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)


def _create_test_product_in_inventory(name, quantity, restock, supplier_name, supplier_id,
                                      unit_price):
    """create products in inventory in bulk """
    return InventoryModel(
        name=name,
        quantity=quantity,
        restock_threshold=restock,
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

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Inventory REST API Service")

    def test_create_product_in_inventory(self):
        """ Create a new Product in Inventory """
        test_product_in_inventory = _create_test_product_in_inventory(
            name="test product", quantity=100, restock=50,
            supplier_name="test supplier", supplier_id=123, unit_price=12.50)
        logging.debug(test_product_in_inventory)
        resp = self.app.post(
            "/inventory", json=test_product_in_inventory.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_product_in_inventory = resp.get_json()
        self.assertEqual(new_product_in_inventory["name"], test_product_in_inventory.name, "Names do not match")
        self.assertEqual(
            new_product_in_inventory["quantity"], test_product_in_inventory.quantity, "Quantities do not match"
        )
        self.assertEqual(
            new_product_in_inventory["restock_threshold"], test_product_in_inventory.restock_threshold,
            "Restock Threshold does not match"
        )
        # # Check that the location header was correct
        # resp = self.app.get(location, content_type="application/json")
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_product_in_inventory = resp.get_json()
        # self.assertEqual(new_product_in_inventory["name"], test_product_in_inventory.name, "Names do not match")
        # self.assertEqual(
        #     new_product_in_inventory["quantity"], test_product_in_inventory.quantity, "Quantities do not match"
        # )
        # self.assertEqual(
        #     new_product_in_inventory["restock_threshold"], test_product_in_inventory.restock_threshold,
        #     "Restock Threshold does not match"
        # )

    def test_get_product_in_inventory(self):
        """ Get a single Product in Inventory """
        # get the id of the product in inventory
        test_product_in_inventory =_create_test_product_in_inventory(name="test product1", quantity=100, restock=50,
                                                   supplier_name="test supplier1", supplier_id=123, unit_price=12.50)
        test_product_in_inventory.create()
        resp = self.app.get(
            "/inventory/{}".format(test_product_in_inventory.product_in_inventory_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product_in_inventory.name)

    def test_get_product_in_inventory_not_found(self):
        """ Get a Product in inventory thats not found """
        resp = self.app.get("/inventory/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_in_inventory(self):
        """ Update an existing Pet """
        # create a pet to update
        test_update = _create_test_product_in_inventory(
            name="test product", quantity=100, restock=50,
            supplier_name="test supplier", supplier_id=123, unit_price=12.50)
        resp = self.app.post(
            "/inventory", json=test_update.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product in inventory
        new_product_in_inventory = resp.get_json()
        logging.debug(new_product_in_inventory)
        new_product_in_inventory["supplier_name"] = "unknown"
        resp = self.app.put(
            "/inventory/{}".format(new_product_in_inventory["product_in_inventory_id"]),
            json=new_product_in_inventory,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product_in_inventory = resp.get_json()
        self.assertEqual(updated_product_in_inventory["supplier_name"], "unknown")