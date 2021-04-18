$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_id").val(res._id);
        $("#product_id").val(res.product_id);
        $("#product_name").val(res.product_name);
        $("#supplier_id").val(res.supplier_id);
        $("#supplier_name").val(res.supplier_name);
        if (res.supplier_status === "enabled") {
            $("#supplier_status").val("enabled");
        } else {
            $("#supplier_status").val("disabled");
        }
        $("#quantity").val(res.quantity);
        $("#unit_price").val(res.unit_price);
        $("#restock_threshold").val(res.restock_threshold);

    }

    /// Clears all form fields
    function clear_form_data() {
        $("#inventory_id").val("");
        $("#product_id").val("");
        $("#product_name").val("");
        $("#supplier_id").val("");
        $("#supplier_name").val("");
        $("#supplier_status").val("");
        $("#quantity").val("");
        $("#unit_price").val("");
        $("#restock_threshold").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Pet
    // ****************************************

    $("#create-btn").click(function () {
        const inventory_id = $("#inventory_id").val();
        const product_id = $("#product_id").val();
        const product_name = $("#product_name").val();
        const supplier_id = $("#supplier_id").val();
        const supplier_name = $("#supplier_name").val();
        const supplier_status = $("#supplier_status").val() === "enabled";
        const quantity = $("#quantity").val();
        const unit_price = $("#unit_price").val();
        const restock_threshold = $("#restock_threshold").val();

        const data = {
            "inventory_id": inventory_id,
            "product_id": product_id,
            "product_name": product_name,
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "supplier_status": supplier_status,
            "quantity": quantity,
            "unit_price": unit_price,
            "restock_threshold": restock_threshold,
        };

        const ajax = $.ajax({
            type: "POST",
            url: "/inventory",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {
        const inventory_id = $("#inventory_id").val();
        const product_id = $("#product_id").val();
        const product_name = $("#product_name").val();
        const supplier_name = $("#supplier_name").val();
        const supplier_id = $("#supplier_id").val();
        const supplier_status = $("#supplier_status").val() == "enabled";
        const quantity = $("#quantity").val();
        const unit_price = $("#unit_price").val();
        const restock_threshold = $("#restock_threshold").val();

        const data = {
            "inventory_id": inventory_id,
            "product_id": product_id,
            "product_name": product_name,
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "supplier_status": supplier_status,
            "quantity": quantity,
            "unit_price": unit_price,
            "restock_threshold": restock_threshold,
        };

        const ajax = $.ajax({
            type: "PUT",
            url: "/inventories/" + product_id,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Pet
    // ****************************************

    $("#retrieve-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/inventories/" + product_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        const product_id = $("#product_id").val();

        const ajax = $.ajax({
            type: "DELETE",
            url: "/inventory/" + product_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {
        // FIXME: We dont support searching by most of these fields so those will not work. see ../../models.py to either make more search methods or determine which to remove below
        const inventory_id = $("#inventory_id").val();
        const product_id = $("#product_id").val();
        const product_name = $("#product_name").val();
        const supplier_id = $("#supplier_id").val();
        const supplier_name = $("#supplier_name").val();
        const supplier_status = $("#supplier_status").val() === "enabled";

        let queryString = "";

        if (product_name) {
            queryString += 'product_name=' + product_name
        }
        if (product_id) {
            if (queryString.length > 0) {
                queryString += '&product_id=' + product_id
            } else {
                queryString += 'product_id=' + product_id
            }
        }
        if (supplier_id) {
            if (queryString.length > 0) {
                queryString += '&supplier_id=' + supplier_id
            } else {
                queryString += 'supplier_id=' + supplier_id
            }
        }
        if (supplier_status) {
            if (queryString.length > 0) {
                queryString += '&supplier_status=' + supplier_status
            } else {
                queryString += 'supplier_status=' + supplier_status
            }
        }
        if (inventory_id) {
            if (queryString.length > 0) {
                queryString += '&inventory_id=' + inventory_id
            } else {
                queryString += 'inventory_id=' + inventory_id
            }
        }
        if (supplier_name) {
            if (queryString.length > 0) {
                queryString += '&supplier_name=' + supplier_name
            } else {
                queryString += 'supplier_name=' + supplier_name
            }
        }

        const ajax = $.ajax({
            type: "GET",
            url: "/inventory?" + queryString,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            let firstProduct = "";
            for (let i = 0; i < res.length; i++) {
                const product = res[i];
                const row = "<tr><td>" + product.product_id + "</td><td>" + product.name + "</td><td>" + product.supplier_id + "</td><td>" + product.supplier_status + "</td></tr>" + product.supplier_name + "</td><td>" + product.id + "</td><td>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstProduct = product;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstProduct !== "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

})
