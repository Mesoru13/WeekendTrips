async function build_results_page(task_id) {
    let task_status = 1001;
    let task_result;
    while( task_status != 1003 && task_status != 1004 ) {
        let result = $.getJSON('/get_task_result/',
            { 'task_id': task_id }).done(
                function (data, textStatus, jqXHR) {

                task_status = data['request_status'];
                task_result = data['task_result'];
            });
        while( result.state() == "pending" ) {
            await async_sleep(1000);
        };

        if( task_status != 1003 && task_status != 1004 ) {
            await async_sleep(30000);
        }
    }

    $('#waiting_section').fadeOut(500, function () {
        if(task_status == 1003 ){
            $('#ok_section').fadeIn(900, function () {
                build_ready_results(task_status, task_result);
                $('#try_another').fadeIn(1700);
            });
        } else {
            $('#failed_section').fadeIn(900);
        }
    });
}

async function build_ready_results(status, result)
{
    if( status == 1003 ) {
        let newTable;
        let json_result = JSON.parse(result);
        let i = 0;
        for( const [id, ticket] of Object.entries(json_result) ) {
            i++;
            let time_column = "";
            let ticket_info_column = ""
            let id = 'card_section' + i;
            let background_color;
            if( ticket['route_type'] == 'plane' ) {
                time_column = $("<td scope='col'>").append(
                    $("<p>").text('Departure time: ' + ticket['depart_datetime']),
                    $("<p>").text('Return time: ' + ticket['return_datetime'])
                )
                ticket_info_column = $("<td scope='col'>").append(
                    $("<p>").text('Travelling by: ✈'),
                    $("<p>").text('The lowest price: ' + parseFloat(ticket['price']).toFixed(2)  + ' Rub'),
                    $("<p>").text('Number: ' + ticket['airline'] + ticket['number'] )
                )
            } else {
                time_column = $("<td scope='col'>").append(
                    $("<p>").text('Departure time: ' + ticket['depart_datetime']),
                    $("<p>").text('Arrival time: ' + ticket['arrival_datetime']),
                    $("<p>").text('Travel time: ' + secondsToDhm(ticket['travel_time']))
                )
                ticket_info_column = $("<td scope='col'>").append(
                    $("<p>").text('Travelling by: 🚆'),
                    $("<p>").text('The lowest price: ' + parseFloat(ticket['price']).toFixed(2)  + ' Rub'),
                    $("<p>").text('Number: ' + ticket['number'] ),
                    $("<p>").text('Seating type: ' + ticket['seat_type'])
                )
            }

            newTable = $("<div class='row'>").append(
                $("<table id=" + id + " class='table' style='background-color: " + background_color + "'>").append(
                $("<thead class='thead-dark'>").append(
                    $("<tr>").append(
                        $("<th scope='col' width='22%'>").text('Cities info:'),
                        $("<th scope='col' width='26%'>").text('Time info:'),
                        $("<th scope='col' width='26%'>").text('Tickets info:'),
                        $("<th scope='col' width='26%'>").text('Links:')
                    )),
                $("<tbody>").append(
                    $("<tr>").append(
                        $("<td scope='col'>").append(
                            $("<p>").text('From: ' + ticket['origin_city']),
                            $("<p>").text('To: ' + ticket['destination_city'])
                        ),
                        time_column,
                        ticket_info_column,
                        $("<td scope='col'>").append(
                            $("<a href='" + ticket['url'] + "'>").text('Buy here!')
                        )
                    ))));
            $('#ok_section').append(newTable);
            $('#card_section' + i).fadeIn(300);
            await async_sleep(300);
        }
    } else {
        document.getElementById('waiting_section').hidden = true;
        document.getElementById('failed_section').hidden = false;
    }
}

function async_sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function secondsToDhm(seconds) {
    seconds = Number(seconds);
    let d = Math.floor(seconds / (3600*24));
    let h = Math.floor(seconds % (3600*24) / 3600);
    let m = Math.floor(seconds % 3600 / 60);

    let dDisplay = d > 0 ? d + " d " : "";
    let hDisplay = h > 0 ? h + " h " : "";
    let mDisplay = m > 0 ? m + " min " : "";
    return dDisplay + hDisplay + mDisplay;
}