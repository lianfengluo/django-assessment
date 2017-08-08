$(document).ready(function(){
    $("#username").focus(function(){ 
        $(this).blur(function(){
                var username=$("#username").val();
                $.getJSON("/assess/checkuser", {'username':username}, function(ret)
                    {   $('#userresult').html('');
                        if(ret.valid){
                        $('#userresult').css("color","green"); 
                        $('#userresult').append(ret.valid);
                        $('#userresult').removeAttr("class");
                       }; 
                        if(ret.error){
                            $('#userresult').attr("class","error"); 
                            $('#userresult').append(ret.error);
                            $('#userresult').removeAttr("style");

                        };
         
                               });
                            
                        });
        });
    $("#password").focus(function(){ 
        $(this).blur(function(){
            var password=$("#password").val();
            $('#passresult').html('');
            var re=/^.{6,20}$/
            if (re.test(password)) {$('#passresult').css("color","green");$('#passresult').append("valid password!"); $('#passresult').removeAttr("class");}
            else{$('#passresult').attr("class","error");$('#passresult').append("invalid password");$('#passresult').removeAttr("style");}
                            });
    });
    $("#password2").focus(function(){ 
        $(this).blur(function(){
            var password2=$("#password2").val();
            var password=$("#password").val();
            $('#pass2result').html('');
            var re=/^.{6,20}$/
            if (re.test(password2)) {
                if (password==password2)
                    {$('#pass2result').css("color","green");$('#pass2result').append("valid password!"); $('#pass2result').removeAttr("class");}
                else
                    {$('#pass2result').attr("class","error");$('#pass2result').append("two password not match");$('#pass2result').removeAttr("style");}
            }
            else{$('#pass2result').attr("class","error");$('#pas2sresult').append("two password not match");$('#pass2result').removeAttr("style");}
                            });
    });
    $("#nickname").focus(function(){ 
        $(this).blur(function(){
            var nickname=$("#nickname").val();
            $('#nicknameresult').html('');
            var re=/^.{3,20}$/
            if (nickname.indexOf("'")>-1 || nickname.indexOf('"')>-1) {$('#nicknameresult').attr("class","error");$('#nicknameresult').append("invalid nicknameresult");$('#nicknameresult').removeAttr("style");}
            else{
                if (re.test(nickname)) {$('#nicknameresult').css("color","green");$('#nicknameresult').append("valid nicknameresult!"); $('#nicknameresult').removeAttr("class");}
                else{$('#nicknameresult').attr("class","error");$('#nicknameresult').append("invalid nicknameresult");$('#nicknameresult').removeAttr("style");}
            }
                            });
    });
    $("#contact_number").focus(function(){ 
        $(this).blur(function(){
            var contact_number=$("#contact_number").val();
            $('#contact_numberresult').html('');
            var re=/^\w{8,20}$/
            if (re.test(contact_number)) {$('#contact_numberresult').css("color","green");$('#contact_numberresult').append("valid contact_number!"); $('#contact_numberresult').removeAttr("class");}
            else{$('#contact_numberresult').attr("class","error");$('#contact_numberresult').append("invalid contact_numberresult");$('#contact_numberresult').removeAttr("style");}
           
                            });
    });

    $("#email").focus(function(){ 
        $(this).blur(function(){
                var email=$("#email").val();
                $.getJSON("/assess/checkemail", {'email':email}, function(ret)
                    {   $('#emailresult').html('');
                        if(ret.valid){
                        $('#emailresult').css("color","green"); 
                        $('#emailresult').append(ret.valid);
                        $('#emailresult').removeAttr("class");
                       }; 
                        if(ret.error){
                            $('#emailresult').attr("class","error"); 
                            $('#emailresult').append(ret.error);
                            $('#emailresult').removeAttr("style");

                        };
         
                               });
                            
                        });
        });

/*    $("#check_code").focus(function(){ 
        $(this).blur(function(){
            var check_code=$("#check_code").val();
            $.getJSON("/assess/checkcheck_code", {'check_code':check_code}, function(ret)
                {   $('#check_coderesult').html('');
                    if(ret.valid){
                    $('#check_coderesult').css("color","green"); 
                    $('#check_coderesult').append(ret.valid);
                    $('#check_coderesult').removeAttr("class");
                   }; 
                    if(ret.error){
                        $('#check_coderesult').attr("class","error"); 
                        $('#check_coderesult').append(ret.error);
                        $('#check_coderesult').removeAttr("style");

                    };
     
                           });
                        
                    });
        });*/
    function mySubmit(flag){  
    return flag;  
    }  
    $("form").submit(function(e){
        if($('#userresult').attr('class')=='error' || $('#passresult').attr('class')=='error' || $('#emailresult').attr('class')=='error' || $('#contact_numberresult').attr('class')=='error'|| $('#pass2result').attr('class')=='error'|| $('#nicknameresult').attr('class')=='error')
        //$('#check_coderesult').attr('class')=='error'
            {return mySubmit(false);}
        return mySubmit(true);
        });
})

