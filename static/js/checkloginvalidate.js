$(document).ready(function() {

    $("#username").focus(function() {
        $(this).blur(function() {
            var username = $("#username").val();
            $('#userresult').html('');
            var re = /^\w{6,20}$/
            if (re.test(username)) {
                $('#userresult').css("color", "green");
                $('#userresult').append("valid username!");
                $('#userresult').removeAttr("class");
            } else {
                $('#userresult').attr("class", "error");
                $('#userresult').append("invalid username");
                $('#userresult').removeAttr("style");
            }
        });
    });

    $("#password").focus(function() {
        $(this).blur(function() {
            var password = $("#password").val();
            $('#passresult').html('');
            var re = /^.{6,20}$/
            if (re.test(password)) {
                $('#passresult').css("color", "green");
                $('#passresult').append("valid password!");
                $('#passresult').removeAttr("class");
            } else {
                $('#passresult').attr("class", "error");
                $('#passresult').append("invalid password");
                $('#passresult').removeAttr("style");
            }
        });
    });

    // $("#check_code").focus(function(){ 
    //     $(this).blur(function(){
    //         var check_code=$("#check_code").val();
    //         $.getJSON("/assess/checkcheck_code", {'check_code':check_code}, function(ret)
    //             {   $('#check_coderesult').html('');
    //                 if(ret.valid){
    //                 $('#check_coderesult').css("color","green"); 
    //                 $('#check_coderesult').append(ret.valid);
    //                 $('#check_coderesult').removeAttr("class");
    //                }; 
    //                 if(ret.error){
    //                     $('#check_coderesult').attr("class","error"); 
    //                     $('#check_coderesult').append(ret.error);
    //                     $('#check_coderesult').removeAttr("style");

    //                 };

    //                        });

    //                 });
    //     });
    function mySubmit(flag) {
        return flag;
    }
    $("form").submit(function(e) {
        if ($('#userresult').attr('class') == 'error' || $('#passresult').attr('class') == 'error') {
            return mySubmit(false);
        } else {
            return mySubmit(true);
        }
    });
})