// $(document).ready(function() {


// });
$.verify = {
    verifyLogin: function() {
        $("#loginform").submit(function(e) {
            try {
                var check = $.verify1.checkUser() + $.verify1.checkPass() + $.verify1.checkCap();
                // alert(check);
                e.preventDefault();
                if (check == 3) {
                    var userName = $("#username").val(); //获得form中用户输入的name 注意这里的id_name 与你html中的id一致  
                    var passWord = $("#password").val(); //同上  
                    var check_code = $("#check_code").val();
                    $.ajax({
                        type: "POST",
                        data: {
                            username: userName,
                            password: passWord,
                            check_code: check_code,
                        },
                        url: "/login/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致  
                        cache: false,
                        dataType: "html",
                        success: function(result, statues, json) {
                            $("#loginerror").empty();
                            // $("#loginerror").css("display", "block");

                            if (result == 'success') {
                                window.location.href = "/index/";
                            } else {
                                $('#check_code').val('');
                                var responseData = JSON.parse(result);
                                $('#captcha').attr("src", $("#captcha").attr("src") + "?");
                                for (var key in responseData['errors']) {
                                    $("#loginerror").append(responseData['errors'][key] + '<br/>');
                                }
                                // $("#loginerror").append(responseData['check_code']);
                            }
                        },
                        error: function() {
                            $('#captcha').attr("src", $("#captcha").attr("src") + "?");
                            $("#loginerror").empty();
                            $("#loginerror").css("display", "block");
                            $("#loginerror").append('<b>error occur</b>');
                        }
                    });
                    // return true;
                    // return mySubmit(false);
                } else {
                    // alert(1);
                    $("#myErrorModal").modal('show')
                        // return false
                        // return mySubmit(false);
                }
            } catch (e) {}
        });
    },

    verifySignup: function() {
        $("form").submit(function(e) {
            try {
                var check = $.verify1.checkUser() + $.verify1.checkPass() + $.verify1.checkPass2() + $.verify1.checkEmail() + $.verify1.checkNick() + $.verify1.checkCon() + $.verify1.checkCap();
                // alert(check);
                if (check == 7) {
                    $('#captcha').attr("src", $("#captcha").attr("src") + "?");
                    return true;
                } else {
                    // alert(1);
                    $("#myErrorModal").modal('show')
                    e.preventDefault();
                    return false
                        // return mySubmit(false);
                }
            } catch (e) {

            }
        });
        $('#myErrorModal').on('show.bs.modal', function(e) {
            $(this).find('.modal-dialog').css({
                'margin-top': function() {
                    var modalHeight = $('#myErrorModal').find('.modal-dialog').height();
                    return ($(window).height() / 5);
                }
            });
        });
    },
    verifyProfile: function() {
        $("form").submit(function(e) {
            var check = $.verify1.checkEmail() + $.verify1.checkNick() + $.verify1.checkCon();
            // alert(check);
            if (check == 3) {
                $('#check_cod').val('');
                return true;
            } else {
                // alert(1);
                $("#myErrorModal").modal('show')
                e.preventDefault();
                return false
                    // return mySubmit(false);
            }
        });
        $('#myErrorModal').on('show.bs.modal', function(e) {
            $(this).find('.modal-dialog').css({
                'margin-top': function() {
                    var modalHeight = $('#myErrorModal').find('.modal-dialog').height();
                    return ($(window).height() / 5);
                }
            });
        });
    },

};

/* focusverifylogin: function() {
     $("#username").focus(function() {
         $(this).blur(function() {
             var username = $(this).val();
             var re = /^\w{6,20}$/
             if (username) {
                 if (re.test(username)) {
                     // $(this).parent('div').attr("class", "has-success input-group");
                     $("#error1").empty();
                 } else {
                     $("#error1").empty();
                     // $(this).parent('div').attr("class", "has-error input-group");
                     $("#error1").append('<b id="erroruser">Invalid username</b>');
                 }
             } else {
                 // $(this).parent('div').attr("class", "input-group");
                 $("#error1").empty();
             }
         });
     });
     $("#password").focus(function() {
         $(this).blur(function() {
             var password = $(this).val();
             var re = /^.{6,20}$/
             if (password) {
                 if (re.test(password)) {
                     // $(this).parent('div').attr("class", "has-success input-group");
                     $("#error2").empty();
                 } else {
                     $("#error2").empty();
                     // $(this).parent('div').attr("class", "has-error input-group");
                     $("#error2").append('<b id="errorpass">Invalid password</b>');
                 }
             } else {
                 // $(this).parent('div').attr("class", "input-group");
                 $("#error2").empty();
             }
         });
     });
     $("#check_code").focus(function() {
         $(this).blur(function() {
             var check_code = $(this).val();
             var re = /^\w{4}$/
             if (check_code) {
                 if (re.test(check_code)) {
                     // $(this).parent('div').attr("class", "has-success input-group");
                     $("#error3").empty();
                 } else {
                     $("#error3").empty();
                     // $(this).parent('div').attr("class", "has-error input-group");
                     $("#error3").append('<b id="errorcap">Invalid captcha</b>');
                 }
             } else {
                 $(this).parent('div').attr("class", "input-group");
                 $("#error3").empty();
             }
         });
     });*/

// $("form").submit(function(e) {
//     if ($('#check_code').parent('div').attr('class') == 'has-success input-group' && $('#password').parent('div').attr('class') == 'has-success input-group' && $('#username').parent('div').attr('class') == 'has-success input-group') {
//         return mySubmit(true);
//     } else {
//         return mySubmit(false);
//     }
// });



$.verify1 = {
    checkUser: function() {
        var username = $("#username").val();
        var re = /^\w{6,20}$/
        if (username) {
            if (re.test(username)) {
                // $(this).parent('div').attr("class", "has-success input-group");
                $("#errorUser").empty();
                return 1;
            } else {
                $("#errorUser").empty();
                // $(this).parent('div').attr("class", "has-error input-group");
                $("#errorUser").append('<b>Invalid username</b><br/><b>(at least 6 character)</b><br/>');
            }
        } else {
            // $(this).parent('div').attr("class", "input-group");
            $("#errorUser").empty();
            $("#errorUser").append('<b>Input your username</b>');
        }
        return 0;
    },

    checkPass: function() {
        var password = $('#password').val();
        var re = /^.{6,20}$/
        if (password) {
            if (re.test(password)) {
                // $(this).parent('div').attr("class", "has-success input-group");
                $("#errorPass").empty();
                return 1;
            } else {
                $("#errorPass").empty();
                // $(this).parent('div').attr("class", "has-error input-group");
                $("#errorPass").append('<b>Invalid password</b><br/><b>(at least 6 character)</b><br/>');
            }
        } else {
            // $(this).parent('div').attr("class", "input-group");
            $("#errorPass").empty();
            $("#errorPass").append('<b>Input your password</b>');
        }
        return 0;
    },
    checkPass2: function() {
        var password = $('#password').val();
        var password2 = $('#password2').val();
        if (password2) {
            if (password == password2) {
                // $(this).parent('div').attr("class", "has-success input-group");
                $("#errorPass2").empty();
                return 1;
            } else {
                $("#errorPass2").empty();
                // $(this).parent('div').attr("class", "has-error input-group");
                $("#errorPass2").append('<b>Two password are different</b>');
            }
        } else {
            // $(this).parent('div').attr("class", "input-group");
            $("#errorPass2").empty();
            $("#errorPass2").append('<b>Input password again</b>');
        }
        return 0;
    },
    checkEmail: function() {
        var email = $('#email').val();
        var re = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,6}){1,2})$/
        if (email) {
            if (re.test(email)) {
                // $(this).parent('div').attr("class", "has-success input-group");
                $("#errorEmail").empty();
                return 1;
            } else {
                $("#errorEmail").empty();
                // $(this).parent('div').attr("class", "has-error input-group");
                $("#errorEmail").append('<b>Invalid email</b>');
            }
        } else {
            // $(this).parent('div').attr("class", "input-group");
            $("#errorEmail").empty();
            $("#errorEmail").append('<b>Input email</b>');
        }
        return 0;
    },
    checkNick: function() {
        var nickname = $('#nickname').val();
        var re = /^\w{4,20}$/
        if (nickname) {
            if (re.test(nickname)) {
                // $(this).parent('div').attr("class", "has-success input-group");
                $("#errorNick").empty();
                return 1;
            } else {
                $("#errorNick").empty();
                // $(this).parent('div').attr("class", "has-error input-group");
                $("#errorNick").append('<b>Invalid nickname</b><br/><b>(at least 4 character)</b><br/>');
            }
        } else {
            // $(this).parent('div').attr("class", "input-group");
            $("#errorNick").empty();
            $("#errorNick").append('<b>Input nickname</b>');
        }
        return 0;
    },
    checkCon: function() {
        var contact_number = $('#contact_number').val();
        var re = /^[\d|\-|\+|(|)]{6,25}$/
        if (contact_number) {
            if (re.test(contact_number)) {
                // $(this).parent('div').attr("class", "has-success input-group");
                $("#errorCon").empty();
                return 1;
            } else {
                $("#errorCon").empty();
                // $(this).parent('div').attr("class", "has-error input-group");
                $("#errorCon").append('<b>Invalid contact number</b>');
            }
        } else {
            // $(this).parent('div').attr("class", "input-group");
            $("#errorCon").empty();
            $("#errorCon").append('<b>Input contact number</b>');
        }
        return 0;
    },
    checkCap: function() {
        var check_code = $("#check_code").val();
        var re = /^\w{4}$/
        if (check_code) {
            if (re.test(check_code)) {
                // $(this).parent('div').attr("class", "has-success input-group");
                $("#errorCap").empty();
                return 1;
            } else {
                $("#errorCap").empty();
                // $(this).parent('div').attr("class", "has-error input-group");
                $("#errorCap").append('<b> Invalid captcha</b>');
            }
        } else {
            $("#errorCap").empty();
            $("#errorCap").append('<b>Input your captcha</b>');
        }
        return 0;
    },

}