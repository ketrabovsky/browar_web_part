document.addEventListener("DOMContentLoaded", function(event) {
    $('button#heater').click(function(){
        $.ajax({
            url: "/_get_data/",
            type: "POST",
            success: function(resp){
                console.log(resp);
                $('button#heater').toggleClass('active');
            }
        });
        console.log(data)
    });
});

document.addEventListener("DOMContentLoaded", function(event) {
    $('button#pompka').click(function(){
        $.ajax({
            url: "/_get_data1/",
            type: "POST",
            success: function(resp){
                console.log(resp);
                $('button#pompka').toggleClass('active');
            }
        });
        console.log(data)
    });
});
