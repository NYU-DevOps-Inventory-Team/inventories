# inventories
DevOps Inventory Team

This repository contains the code for Inventory for an e-commerce business. This shows how to create a REST API with subordinate resources like products in inventory to maintain an accurate count of products and their attributes that have addresses:

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
Endpoint          Methods  Rule
----------------  -------  -----------------------------------------------------
index             GET      /

list_inventory     GET      /inventory
create_inventory   POST     /inventory
get_inventory     GET      /inventory/<id>
update_inventory   PUT      /inventory/<id>
delete_inventory   DELETE   /inventory/<id>


The test cases have 96% test coverage and can be run with `nosetests`
