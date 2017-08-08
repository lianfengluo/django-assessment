$(document).ready(function() {

    $('#loginform').submit(function() {
        var userName = $("#username").val(); //获得form中用户输入的name 注意这里的id_name 与你html中的id一致  
        var passWord = $("#password").val(); //同上  
        var check_code = $("#check_code").val();
        $.ajax({
            type: "POST",
            data: {
                username: userName,
                password: passWord,
                check_code: check_code,
                csrfmiddlewaretoken: csrf
            },
            url: "/login/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致  
            cache: false,
            dataType: "html",
            success: function(result, statues, json) {
                $("#loginerror").empty();
                $("#loginerror").css("display", "block");

                if (result == 'success') {
                    window.location.href = "/index/";
                } else {
                    var responseData = JSON.parse(result);
                    $('#captcha').attr("src", $("#captcha").attr("src") + "?");
                    for (var key in responseData['errors']) {
                        $("#loginerror").append(responseData['errors'][key] + '<br/>');
                    }
                    // $("#loginerror").append(responseData['check_code']);
                }
            },
            error: function() {
                $("#loginerror").empty();
                $("#loginerror").css("display", "block");
                $("#loginerror").append('<b>error occur</b>');
            }
        });
        return false;
    });

});