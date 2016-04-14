$(document).ready(function() {
    //Add listener to buttons
    $(".button-link").click( function() {
        var classString = $(this).attr("data-id");
        itemID     = classString.substring(0,classString.indexOf('-'));
        itemAction = classString.substring(classString.indexOf('-')+1);
        $.get('/butiko/list/change_item_count/', {item: itemID, action: itemAction}, function(data, status){
            $("#"+item).html(data);
        });
    });

    $('.show-hidden-div').click( function() {
        data_field = $(this).attr('data-id');
        $("div[data-id='"+data_field+"']").prop('hidden', false);
    });

    $('#suggestion').keyup( function() {
        var query;
        query = $(this).val();
        $.get('/butiko/suggest_list/', {suggestion: query}, function(data) {
            $('#list_of_lists').html(data);
        });
    });

    $('#id_pass_conf').keyup( function() {
        firstpass  = $('#id_password').val()
        secondpass = $(this).val()

        if (firstpass && firstpass === secondpass) {
            $('#register-user').prop('disabled', false);
            $(this).css({'background-color': 'white'});
        }
        else {
            $(this).css({'background-color': 'red'});
            $('#register-user').prop('disabled', true);
        }
    });
});
