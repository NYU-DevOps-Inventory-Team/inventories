$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_id").val(res.inventory_id);
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
    // Create an Inventory Item
    // ****************************************

    $("#create-btn").click(function () {
        const product_id = $("#product_id").val();
        const product_name = $("#product_name").val();
        const supplier_id = $("#supplier_id").val();
        const supplier_name = $("#supplier_name").val();
        const supplier_status = $("#supplier_status").val() === "enabled";
        const quantity = $("#quantity").val();
        const unit_price = $("#unit_price").val();
        const restock_threshold = $("#restock_threshold").val();

        const data = {
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
            flash_message("Item Created Successfully")
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
            type: "PUT",
            url: "/inventory/" + inventory_id,
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
    // Retrieve an Inventory Item
    // ****************************************

    $("#retrieve-btn").click(function () {

        const inventory_id = $("#inventory_id").val();

        const ajax = $.ajax({
            type: "GET",
            url: "/inventory/" + inventory_id,
            contentType: "application/json",
            data: ''
        });

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

        const inventory_id = $("#inventory_id").val();

        const ajax = $.ajax({
            type: "DELETE",
            url: "/inventory/" + inventory_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Inventory ID has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#inventory_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {
        // FIXME: We dont support searching by most of these fields so those will not work. see ../../models.py to either make more search methods or determine which to remove below
        const inventory_id = $("#inventory_id").val();
        const product_id = $("#product_id").val();
        const product_name = $("#product_name").val(); //supported
        const supplier_id = $("#supplier_id").val(); //supported
        const supplier_name = $("#supplier_name").val(); //supported
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
            //table looks like:
            //    <!-- Search Results -->
            //     <div class="table-responsive col-md-12" id="search_results">
            //         <table class="table-striped">
            //             <thead>
            //             <tr>
            //                 <th class="col-md-1">Inventory ID</th>
            //                 <th class="col-md-1">Product ID</th>
            //                 <th class="col-md-2">Product Name</th>
            //                 <th class="col-md-1">Supplier ID</th>
            //                 <th class="col-md-2">Supplier Name</th>
            //                 <th class="col-md-2">Supplier Status</th>
            //                 <th class="col-md-1">Quantity</th>
            //                 <th class="col-md-1">Restock Threshold</th>
            //                 <th class="col-md-2">Unit Price</th>
            //             </tr>
            //             </thead>
            //         </table>
            //     </div>

            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            let header = '<tr>';
            header += '<th style="width:10%">Inventory ID</th>'
            header += '<th style="width:40%">Product ID</th>'
            header += '<th style="width:40%">Product Name</th>'
            header += '<th style="width:40%">Supplier ID</th>'
            header += '<th style="width:10%">Supplier Name</th>'
            header += '<th style="width:10%">Supplier Status</th>'
            header += '<th style="width:10%">Quantity</th>'
            header += '<th style="width:10%">Restock Threshold</th>'
            header += '<th style="width:10%">Unit Price</th></tr>'
            $("#search_results").append(header);
            let firstProduct = "";
            for (let i = 0; i < res.length; i++) {
                const product = res[i];
                const row = "<tr><td>"
                    + product.inventory_id + "</td><td>"
                    + product.product_id + "</td><td>"
                    + product.product_name + "</td><td>"
                    + product.supplier_id + "</td><td>"
                    + product.supplier_name + "</td></tr>"
                    + product.supplier_status + "</td></tr>"
                    + product.quantity + "</td></tr>"
                    + product.restock_threshold + "</td></tr>"
                    + product.unit_price + "</td></tr>"
                    + "</td></tr>";
                $("#search_results").append(row);
                if (i === 0) {
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
