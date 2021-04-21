# Inventory Service
DevOps Inventory Team

[![Build Status](https://travis-ci.com/NYU-DevOps-Inventory-Team/inventories.svg?branch=main)](https://travis-ci.com/NYU-DevOps-Inventory-Team/inventories)
[![codecov](https://codecov.io/gh/NYU-DevOps-Inventory-Team/inventories/branch/main/graph/badge.svg?token=5NLUQE5NIR)](https://codecov.io/gh/NYU-DevOps-Inventory-Team/inventories)

This app is live on [IBM Cloud](https://nyu-inventory-service-s21.us-south.cf.appdomain.cloud/).

This repository contains the inventory service for an e-commerce business. The service is a REST API to maintain an accurate count of products and their attributes.

**Note:** This repo has a `Vagrantfile` so the easiest way to play with it is to:

```bash
vagrant up
vagrant ssh
cd /vagrant
nosetests
flask run -h 0.0.0.0
```

If you have an IBM Cloud API key in `~/.bluemix/apiKey-inventory.json` on your vagrant machine, you can login with the following commands:

```bash
ibmcloud login -a https://cloud.ibm.com --apikey @~/.bluemix/apiKey-inventory.json -r us-south
ibmcloud target --cf -o mv2232@stern.nyu.edu -s dev
```

These are the RESTful routes for the Inventory Service 
```
Endpoint                        Methods      Rule
--------------------------      -------      -------------------------
index                           GET          / 
create_new_inventory_item       POST         /inventory 
list_inventory_items            GET          /inventory 
get_inventory_item              GET          /inventory/<inventory_id> 
update_inventory_item           PUT          /inventory/<inventory_id> 
delete_inventory_item           DELETE       /inventory/<inventory_id> 
disable_supplier                PUT          /inventory/supplier/<supplier_id> 
```

The test cases can be run with `nosetests`.
