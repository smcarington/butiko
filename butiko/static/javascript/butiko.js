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

    $('#suggestion').keyup( function() {
        var query;
        query = $(this).val();
        $.get('/butiko/suggest_list/', {suggestion: query}, function(data) {
            $('#list_of_lists').html(data);
        });
    });
});
