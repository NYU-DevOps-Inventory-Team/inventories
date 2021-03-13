"""
Models for InventoryModel

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


class InventoryModel(db.Model):
    """
    Class that represents a <your resource model name>
    """

    app = None

    # Table Schema
    product_in_inventory_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    restock_threshold = db.Column(db.Integer)
    supplier_name = db.Column(db.String(63))
    supplier_id = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<InventoryModel %r id=[%s]>" % (self.name, self.product_in_inventory_id)

    def create(self):
        """
        Creates a InventoryModel to the database
        """
        logger.info("Creating %s", self.name)
        self.product_in_inventory_id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a InventoryModel to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a InventoryModel from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a InventoryModel into a dictionary """
        return {
            "product_in_inventory_id": self.product_in_inventory_id,
            "name": self.name,
            "quantity": self.quantity,
            "restock_threshold": self.restock_threshold,
            "supplier_name": self.supplier_name,
            "supplier_id": self.supplier_id,
            "unit_price": self.unit_price
            }

    def deserialize(self, data):
        """
        Deserializes a InventoryModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.quantity = data["quantity"]
            self.restock_threshold = data["restock_threshold"]
            self.supplier_name = data["supplier_name"]
            self.supplier_id = data["supplier_id"]
            self.unit_price = data["unit_price"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid InventoryModel: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid InventoryModel: body of request contained bad or no data"
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
        """ Returns all of the InventoryModels in the database """
        logger.info("Processing all InventoryModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a InventoryModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a InventoryModel by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all InventoryModels with the given name

        Args:
            name (string): the name of the InventoryModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
