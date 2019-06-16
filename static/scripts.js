//  global variables
let stage = 0

window.onload = setInterval(function(){
    $.ajax({
        url: "/_states/",
        type: "POST",
        success: function(resp) {
            change_temp(resp.temperatura);
            stage = resp.stage
            watchProcess();
        }
    });
}, 5000);


$(document).ready(function() {
    //$.getJSON( "config.json", function(data) {
    //    console.log(data);
    var items = [];
    $.ajax({
        url: "/_config",
        type: "POST",
        success: function(data) {
            data.peripherals.forEach(item => {
                if (item.type != 'therm') {
                    items.push("<div class='btn-wrapper'><button id='" + item.name + "'>" + item.display_name + "</button><div class='icon'></div></div>" );
                }
            });
           
            $("#buttons").append(items.join(""));
            watchProcess();
        }
    });

    
});

function watchProcess() {
    let fill;

    switch (stage) {
        case 1:
            fill = 8;
        break;
        case 2:
            fill = 25;
        break;
        case 3:
            fill = 42;
        break;
        case 4:
            fill = 58;
        break;
        case 5:
            fill = 75;
        break;
        case 6:
            fill = 100;
        break;
    };

    $('#timeline').css({ background: "linear-gradient(to right, #0dab14 0%, #0dab14 " + fill + "%, white " + fill + "%, white 100%)" })
    
    for (i = 0; i < stage; i++) {
        $($('#stages').children()[i]).addClass('active')
    }
}

document.addEventListener('click', function(event) {
    const element = event.target;

    
    if (element.localName == 'button') {
        $.ajax({
            url: "/_get_data/",
            type: "POST",
            success: function(resp) {
                $(element).parent().toggleClass('active');
                updateState(element);
                console.log(resp);
            }
        });
    }
    
    function updateState(element) {
        if (element.id == 'start') {
            // jesli kliknelismy w start
            if ($(element).parent().hasClass('active')) {
                // jesli włączamy proces
                $('#buttons').children().find('button').prop('disabled', true );
            } else {
                // jeśli wyłączamy
                $('#buttons').children().find('button').prop('disabled', false );
            }
        }
    }
});

function change_temp(new_temp) {
    document.getElementById("temperature").innerHTML = `<h2>${new_temp}°C</h2>`;
}