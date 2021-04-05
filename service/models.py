"""
Models for InventoryItem

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class InventoryItem(db.Model):
    """
    Class that represents an inventory item
    """
    app = None

    # Table Schema
    inventory_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(63), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    restock_threshold = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer, nullable=False)
    supplier_name = db.Column(db.String(63))
    unit_price = db.Column(db.Float, nullable=False)
    # todo: this should probably be a enumerable
    supplier_status = db.Column(db.String(63), nullable=False)

    def __repr__(self):
        return "<InventoryItem %r id=[%s]>" % (self.product_name, self.inventory_id)

    def create(self):
        """
        Creates an inventoryItem to the database
        """
        logger.info("Creating %s", self.product_name)
        self.inventory_id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates an inventoryItem to the database
        """
        logger.info("Saving %s", self.product_name)
        db.session.commit()

    def delete(self):
        """ Removes an inventoryItem from the data store """
        logger.info("Deleting %s", self.product_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes an inventoryItem into a dictionary """
        return {
            "inventory_id": self.inventory_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "restock_threshold": self.restock_threshold,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier_name,
            "unit_price": self.unit_price,
            "supplier_status": self.supplier_status
        }

    def deserialize(self, data):
        """
        Deserializes an inventoryItem from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.product_id = data["product_id"]
            self.product_name = data["product_name"]
            self.quantity = data["quantity"]
            self.restock_threshold = data["restock_threshold"]
            self.supplier_id = data["supplier_id"]
            self.supplier_name = data["supplier_name"]
            self.unit_price = data["unit_price"]
            self.supplier_status = data["supplier_status"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid InventoryItem: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid InventoryItem: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the InventoryItems in the database """
        logger.info("Processing all InventoryItems")
        return cls.query.all()

    @classmethod
    def find(cls, inventory_id):
        """ Finds an inventoryItem by its ID """
        logger.info("Processing lookup for id %s ...", inventory_id)
        return cls.query.get(inventory_id)

    @classmethod
    def find_or_404(cls, inventory_id):
        """ Find an inventoryItem by its id """
        logger.info("Processing lookup or 404 for id %s ...", inventory_id)
        return cls.query.get_or_404(inventory_id)

    @classmethod
    def find_by_name(cls, product_name):
        """Returns all InventoryItems with the given name

        Args:
            product_name (string): the name of the InventoryItems you want to match
        """
        logger.info("Processing name query for %s ...", product_name)
        return cls.query.filter(cls.product_name == product_name)
