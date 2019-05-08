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
    });
});