"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import InventoryModel, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
# DELETE A PET
######################################################################
@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def delete_product_in_inventory(product_in_inventory_id):
    """
    Delete a Product in Inventory
    This endpoint will delete a Product in Inventory based the id specified in the path
    """
    app.logger.info("Request to delete pet with id: %s", product_in_inventory_id)
    product_in_inventory = Pet.find(product_in_inventory_id)
    if product_in_inventory:
        product_in_inventory.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    InventoryModel.init_db(app)

