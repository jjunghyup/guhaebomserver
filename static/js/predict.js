$(function() {
    $('button#predict').bind('click', function() {
        var data = {
          'query': $('input[name=query]').val()
        };
        $.ajax({
            url: '/predict/intent',
            data: data,
            dataType: "text",
            type: 'POST',
            success: function(result){
                var json = $.parseJSON(result);
                console.log(json.predictions);
                $('#result').val(json.predictions);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});