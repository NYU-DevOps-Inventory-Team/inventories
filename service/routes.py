"""
Inventory Service
Maintain an accurate count of products in inventory and their attributes

Paths:
------
GET /inventory - Returns a list all of the products in inventory
GET /inventory/{id} - Returns a product in inventory with a given product id number
POST /inventory - creates a new product in inventory record in the database
PUT /inventory/{id} - updates a product in inventory record in the database
DELETE /inventory/{id} - deletes a product in invetory record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound

from service.models import InventoryModel, DataValidationError

# Import Flask application
from . import app


######################################################################
# Error Handlers
######################################################################

@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=message,
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=message,
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        jsonify(
            name="Inventory REST API Service",
            version="1.0",
            # paths=url_for("list_inventory", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# ADD A NEW PRODUCT IN INVENTORY
######################################################################
@app.route("/inventory", methods=["POST"])
def create_product_in_inventory():
    """
    Creates a new product in inventory
    This endpoint will create a product in inventory based the data in the body that is posted
    """
    app.logger.info("Request to create a product in inventory")
    check_content_type("application/json")
    product_in_inventory = InventoryModel()
    product_in_inventory.deserialize(request.get_json())
    product_in_inventory.create()
    message = product_in_inventory.serialize()
    # location_url = url_for("get_product_in_inventory",
    #                        product_in_inventory=product_in_inventory.product_in_inventory_id,
    #                        _external=True)
    location_url = "not implemented"
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url})

######################################################################
# RETRIEVE A PRODUCT IN INVENTORY
######################################################################
@app.route("/inventory/<int:product_in_inventory_id>", methods=["GET"])
def get_product_in_inventory(product_in_inventory_id):
    """
    Retrieve a single product in inventory
    This endpoint will return a product in inventory based on it's id
    """
    app.logger.info("Request for product in inventory with id: %s", product_in_inventory_id)
    product_in_inventory = InventoryModel.find(product_in_inventory_id)
    if not product_in_inventory:
        raise NotFound("Product in inventory with id '{}' was not found.".format(product_in_inventory_id))
    return make_response(jsonify(product_in_inventory.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE AN EXISTING PRODUCT IN INVENTORY
######################################################################
@app.route("/inventory/<int:inventory_id>", methods=["PUT"])
def update_product_in_inventory(inventory_id):
    """
    Update a Product In Inventory

    This endpoint will update a Product In Inventory based the body that is posted
    """
    app.logger.info("Request to update Product In Inventory with id: %s", inventory_id)
    check_content_type("application/json")
    product_in_inventory = InventoryModel.find(inventory_id)
    if not product_in_inventory:
        raise NotFound("Product In Inventory with id '{}' was not found.".format(inventory_id))
    product_in_inventory.deserialize(request.get_json())
    product_in_inventory.product_in_inventory_id = inventory_id
    product_in_inventory.save()
    return make_response(jsonify(product_in_inventory.serialize()), status.HTTP_200_OK)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    InventoryModel.init_db(app)


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))
