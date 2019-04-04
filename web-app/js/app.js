$(document).ready(function() {
    var tableData = []
    $.get('http://127.0.0.1:5000/api/tickets', function (data, status) {
        tableData = data['data'];
        console.log(JSON.stringify(tableData))
    });

    $('#myTable').DataTable({
        'processing': true,
        'ajax': {
            'url': 'http://127.0.0.1:5000/api/tickets',
        },
        'columns': [
            {"data": "id"},
            {"data": "title"},
            {"data": "description"},
            {"data": "client"},
            {"data": "product_area"},
            {"data": "priority"},
            {"data": "target_date"}
        ]
    });
});
