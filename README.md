# Inventory Service
DevOps Inventory Team

This repository contains the inventory service for an e-commerce business. The service is a REST API to maintain an accurate count of products and their attributes.

[![Build Status](https://travis-ci.com/NYU-DevOps-Inventory-Team/inventories.svg?branch=main)](https://travis-ci.com/NYU-DevOps-Inventory-Team/inventories)
[![codecov](https://codecov.io/gh/NYU-DevOps-Inventory-Team/inventories/branch/main/graph/badge.svg?token=5NLUQE5NIR)](https://codecov.io/gh/NYU-DevOps-Inventory-Team/inventories)

**Note:** This repo has a `Vagrantfile` so the easiest way to play with it is to:

```bash
vagrant up
vagrant ssh
cd /vagrant
nosetests
flask run -h 0.0.0.0
```

These are the RESTful routes for `inventories` 
```
Endpoint                        Methods      Rule
--------------------------      -------      -------------------------
index                           GET          / 
create_new_inventory_item       POST         /inventory 
list_inventory_items            GET          /inventory 
get_inventory_item              GET          /inventory/<inventory_id> 
update_inventory_item           PUT          /inventory/<inventory_id> 
delete_inventory_item           DELETE       /inventory/<inventory_id> 


The test cases have 96% test coverage and can be run with `nosetests`
