$(document).ready(function() {
    //Add listener to buttons

    var numUpdate = 0;
    var curFunHandle;
    
    // A function which makes the call and updates the database. Note that when it returns, it must reset numUpdate
    // clear the current function handle
    function update_item(jsonData) {
        alert('Hit');
        $itemNumber = $("[id='"+jsonData['item']+"']");
        $.get('/butiko/list/change_item_count/', jsonData, function(data, status){
           $itemNumber.html(data);
           $itemNumber.css('color','#000000');
        });
    }

    $(".button-link").click( function() {
        var classString = $(this).attr("data-id");
        itemID     = classString.substring(0,classString.indexOf('-'));
        itemAction = classString.substring(classString.indexOf('-')+1);

        // Optimistically update, but show grey to convey updating
        $itemNumber = $("[id='"+itemID+"']");
        curNum = parseInt($itemNumber.html());
        if (itemAction == "add" ) {
            $itemNumber.html((curNum+1).toString());
            $itemNumber.css('color', '#e6e6e6');
            numUpdate++;
        }
        else if (itemAction == "sub" && curNum >0) {
            $itemNumber.html((curNum-1).toString());
            $itemNumber.css('color', '#e6e6e6');
            numUpdate--;
        }
    
        // Check to see if there are pending requests. If not, create one
        if (curFunHandle) {
            clearTimeout(curFunHandle);
            curFunHandle = null;
        }
        curFunHandle = setTimeout( function() {update_item({item:itemID, action:itemAction, num:numUpdate});},  1000);

//        $.get('/butiko/list/change_item_count/', {item: itemID, action: itemAction}, function(data, status){
//            $itemNumber.html(data);
//            $itemNumber.css('color','#000000');
//        });
    });

    $('.show-hidden-div').click( function() {
        data_field = $(this).attr('data-id');
        $divEl = $(".sunken-div[data-id='"+data_field+"']");
        if ($divEl.prop('hidden') == true) {
            $divEl.prop('hidden', false)
            $(this).html('Hide Request');
        } else {
            $divEl.prop('hidden', true);
            $(this).html('Show Request');
//        $("div[data-id='"+data_field+"']").prop('hidden', false);
        }
    });

    $('.grant-deny').click( function() {
        var splitStr = $(this).attr('data').split('-');
        var act = splitStr[0]; lis = splitStr[1]; use = splitStr[2];
        var sunkdiv = ".sunken-div[data-id='".concat(lis,"-",use, "']");
        var reqdiv  = ".new-requests[data-id='".concat(lis,"-",use, "']");
        $divEl1 = $(sunkdiv);
        $divEl2 = $(reqdiv);
        $.get('/butiko/grant_deny/', {action: act, list: lis, user: use}, function(data) {
            $divEl1.html(data['response']);
            setTimeout( function() { del_div($divEl1); del_div($divEl2); }, 2000);

            function del_div(divEl) {
                divEl.remove()
            }
        }, "json");
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
