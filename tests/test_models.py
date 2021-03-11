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

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ Test something """
        self.assertTrue(True)
