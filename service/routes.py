"""
Inventory Service
Maintain an accurate count of inventory items and their attributes

Paths:
------
GET /inventory - Returns a list all of the inventory items
GET /inventory/{inventory_id} - Returns an inventory item with a given product id number
POST /inventory - creates a new inventory item record in the database
PUT /inventory/{inventory_id} - updates an inventory item record in the database
DELETE /inventory/{inventory_id} - deletes a product in inventory record in the database
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

from service.models import InventoryItem, DataValidationError

# Import Flask application
from . import app


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
            paths=url_for("list_inventory_items", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# ADD A NEW INVENTORY ITEM
######################################################################
@app.route("/inventory", methods=["POST"])
def create_new_inventory_item():
    """
    Creates a new inventory item
    This endpoint will create an inventory item based the data in the body that is posted
    """
    app.logger.info("Request to create new inventory item")
    check_content_type("application/json")
    inventory_item = InventoryItem()
    inventory_item.deserialize(request.get_json())
    inventory_item.create()
    message = inventory_item.serialize()
    location_url = url_for(
        "get_inventory_item",
        inventory_id=inventory_item.inventory_id,
        _external=True
    )
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# LIST ALL INVENTORIES
######################################################################
@app.route("/inventory", methods=["GET"])
def list_inventory_items():
    """ Returns all of the Inventory """
    app.logger.info("Request for inventory list of all products")

    all_inventory_items = []

    supplier_name = request.args.get("supplier_name")
    product_name = request.args.get("product_name")
    supplier_id = request.args.get("supplier_id")
    if supplier_name:
        all_inventory_items = InventoryItem.find_by_supplier_name(supplier_name)
    elif product_name:
        all_inventory_items = InventoryItem.find_by_product_name(product_name)
    elif supplier_id:
        all_inventory_items = InventoryItem.find_by_supplier_id(supplier_id)    
    else:
        all_inventory_items = InventoryItem.all()

    results = [inventory.serialize() for inventory in all_inventory_items]

    app.logger.info("Returning %d inventory items", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN INVENTORY ITEM
######################################################################
@app.route("/inventory/<int:inventory_id>", methods=["GET"])
def get_inventory_item(inventory_id):
    """
    Retrieve a single inventory item
    This endpoint will return an inventory item based on it's id
    """
    app.logger.info("Request for inventory item with id: %s", inventory_id)
    inventory_item = InventoryItem.find(inventory_id)
    if not inventory_item:
        raise NotFound("Inventory item with inventory id '{}' was not found.".format(inventory_id))
    return make_response(jsonify(inventory_item.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE AN EXISTING INVENTORY ITEM
######################################################################
@app.route("/inventory/<int:inventory_id>", methods=["PUT"])
def update_inventory_item(inventory_id):
    """
    Update an inventory item
    This endpoint will update an inventory item based the body that is posted
    """
    app.logger.info("Request to update Inventory item with id: %s", inventory_id)
    check_content_type("application/json")
    inventory_item = InventoryItem.find(inventory_id)
    if not inventory_item:
        raise NotFound("Inventory item with id '{}' was not found.".format(inventory_id))
    inventory_item.deserialize(request.get_json())
    inventory_item.inventory_id = inventory_id
    inventory_item.save()
    return make_response(jsonify(inventory_item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN INVENTORY ITEM
######################################################################
@app.route("/inventory/<int:inventory_id>", methods=["DELETE"])
def delete_inventory_item(inventory_id):
    """
    Delete an inventory item
    This endpoint will delete an inventory item based the inventory id specified in the path
    """
    app.logger.info("Request to delete inventory item with id: %s", inventory_id)
    inventory_item = InventoryItem.find(inventory_id)
    if inventory_item:
        inventory_item.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# DISABLE ITEM BY SUPPLIER ID
######################################################################
@app.route("/inventory/supplier/<int:supplier_id>", methods=["PUT"])
def disable_supplier(supplier_id):
    """
    Toggle inventory item status to enabled or disabled given Supplier ID
    This endpoint will enable or disable an inventory item based the supplier id specified in the path
    """
    app.logger.info("Request to disable inventory item with supplier id: %s", supplier_id)

    # retrieve inventory items from DB based on supplier id
    inventory_items = InventoryItem.find_by_supplier_id(supplier_id)
    if not inventory_items or inventory_items.count() == 0:
        raise NotFound("Inventory items with supplier id '{}' were not found.".format(supplier_id))

    results = []
    for item in inventory_items:
        # toggle supplier status attribute on item
        item.supplier_status = "disabled" if item.supplier_status == "enabled" else "enabled"

        # save item in DB and return new item
        item.save()
        results.append(item.serialize())

    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    InventoryItem.init_db(app)


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))


######################################################################
# ERROR HANDLERS
######################################################################

@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad requests with 400_BAD_REQUEST """
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
    """ Handles unsupported HTTP methods with 405_METHOD_NOT_SUPPORTED """
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
    """ Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE """
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
