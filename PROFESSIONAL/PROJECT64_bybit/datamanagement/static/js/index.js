
function updateTable() {
    console.log(2000)
    $.ajax({
        url: '/rest_update/',  // Replace with the actual URL of your Django view
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            updateTableContents(data.present_positions);
            updateClosedContents(data.closed_positions);

        },
        error: function () {
            console.error('Error fetching data from the server.');
        }
    });
}


function updateTableContents(positions) {
    var tbody = $('#present_position_table');
    tbody.empty();

    positions.forEach(function (pos, index) {
        var row = '<tr>' +
            '<th scope="row">' + (index + 1) + '</th>' +
            '<td>' + pos.symbol + '</td>' +
            '<td>' + pos.time_start + '</td>' +
            '<td>' + pos.price_in + '</td>' +
            '<td style="color: ' + (pos.type =="SHORT" ? 'rgb(216, 25, 25)' : 'rgb(21, 214, 21)') + ';">' + pos.type + '</td>' +
            '<td>' + pos.current_price + '</td>' +
            '<td>' + pos.stoploss + '</td>' +
            '<td>' + pos.take_profit + '</td>' +
            '<td>' + pos.quantity + '</td>' +
            '<td style="color: ' + (pos.pnl < 0 ? 'rgb(216, 25, 25)' : 'rgb(21, 214, 21)') + ';">' + pos.pnl + '</td>'  +
            '</tr>';
        tbody.append(row);
    });
}
function updateClosedContents(positions) {
    var tbody = $('#closed_position_table');
    tbody.empty();

    positions.forEach(function (pos, index) {
        var row = '<tr>' +
            '<th scope="row">' + (index + 1) + '</th>' +
            '<td>' + pos.symbol + '</td>' +
            '<td>' + pos.time_start + '</td>' +
            '<td>' + pos.price_in + '</td>' +
            '<td style="color: ' + (pos.type =="SHORT" ? 'rgb(216, 25, 25)' : 'rgb(21, 214, 21)') + ';">' + pos.type + '</td>' +
            '<td>' + pos.current_price + '</td>' +
            '<td>' + pos.stoploss + '</td>' +
            '<td>' + pos.take_profit + '</td>' +
            '<td>' + pos.quantity + '</td>' +
            '<td style="color: ' + (pos.pnl < 0 ? 'rgb(216, 25, 25)' : 'rgb(21, 214, 21)') + ';">' + pos.pnl + '</td>'  +
            '</tr>';
        tbody.append(row);
    });
}

updateTable();
setInterval(updateTable, 1000);






