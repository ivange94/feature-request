$(document).ready(function() {
    var baseUrl = 'http://127.0.0.1:5000/';
    var tableData = []

    var table = $('#myTable').DataTable({
        'processing': true,
        'ajax': {
            'url': baseUrl + 'api/tickets',
        },
        'columns': [
            {"data": "title"},
            {"data": "description"},
            {"data": "client"},
            {"data": "product_area"},
            {"data": "priority"},
            {"data": "target_date"},
            {
                mRender: function(data, type, row) {
                    return '<a href="#"><span class="glyphicon glyphicon-pencil" data-id="' + row.id + '" data-bind="click: setValues()" id="btnEdit"></span></a> / <a href="#"><span class="glyphicon glyphicon-remove" data-id="' + row.id + '" id="btnDelete"></span></a>'
                }
            },
        ]
    });

    $('#myTable').on('click', 'span#btnDelete', function(){
        $('#actionStatus').hide();
        var shouldDelete = confirm('Are you sure you want to delete this record?')
        if (shouldDelete) {
            var id = $(this).attr('data-id');
            $.ajax({
                url: baseUrl + 'api/tickets/' + id,
                type: 'DELETE',
                success: function(result) {
                    table.ajax.reload(null, false);
                }
            })
        }
    });

    $('#btnAddFeatureRequestModal').click(function () {
        $('#actionStatus').hide();
        $('#formCreateTicket').trigger('reset');
    })

    function getFormData($form) {
        var unindexed_array = $form.serializeArray();
        var indexed_array = {};

        $.map(unindexed_array, function(n, i) {
            indexed_array[n['name']] = n['value']
        });

        return indexed_array;
    }

    function validate(formData) {
        if (formData.title.trim() === '')
            return false;
        if (formData.description.trim() === '')
            return false;
        if (formData.client.trim() === '')
            return false;
        if (formData.product_area.trim() === '')
            return false;
        if (!formData.target_date)
            return false;
        if (!formData.priority)
            return false;
        return true;
    }

    $('#btnAddNewFeatureRequest').click( function() {
        var jsonBody = getFormData($("#formCreateTicket"));
        var isValid = validate(jsonBody);

        if (isValid) {
            $.ajax({
                type: 'POST',
                url: baseUrl + 'api/tickets',
                data: JSON.stringify(jsonBody),
                success: function(result) {
                    $('#addFeatureRequestModal').modal('hide');
                    table.ajax.reload(null, false);
                    $('#actionStatus').show();
                    $('#formCreateTicket').trigger('reset');
                }
            })
        } else {
            alert('All fields are required');
        }
    });

    $('#btnUpdateFeatureRequest').click( function() {
        $('#actionStatus').hide();
        var body = getFormData($("#formUpdateTicket"));

        var isValid = validate(body);

        body.id = $('#ticketId').val();
        
        if (isValid) {
            $.ajax({
                type: 'PUT',
                url: baseUrl + 'api/tickets',
                data: JSON.stringify(body),
                success: function(result) {
                    $('#editFeatureRequestModal').modal('hide');
                    table.ajax.reload(null, false);
                    $('#actionStatus').show();
                }
            })
        } else {
            alert('All fields are required');
        }
    });

    $('#myTable').on('click', 'span#btnEdit', function(){
        $('#actionStatus').hide();
        var ticketId = $(this).attr('data-id');

        $.get(baseUrl + 'api/tickets/' + ticketId, function(result) {
            var ticket = result['data'];
            $('#edit_title').val(ticket['title']);
            $('#edit_description').val(ticket['description']);
            $('#edit_client').val(ticket['client']);
            $('#edit_product_area').val(ticket['product_area']);
            $('#edit_priority').val(ticket['priority']);
            $('#edit_target_date').val(ticket['target_date']);
            $('#ticketId').val(ticket['id']);

            $('#editFeatureRequestModal').modal('show');
        })
    });
});
