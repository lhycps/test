function checkUsername() {
    var username = $('#username_id').val();
    if (username.length < 6) {
        $('#span_username').html('未通过校验，长度小于6位').css("color", "red")
        return false;
    } else {
        $('#span_username').html('')
        return true;

    }

}


function checkPassword() {
    var pwd = $("#password_id").val();
    var p = new RegExp("^(?!^\\d+$)(?!^[a-zA-Z]+$)[0-9a-zA-Z]{4,23}")
    if (!p.test(pwd)) {
        $("#span_password").html('密码必需由字母和数字组合').css("color", 'red')
        return false;
    } else {
        $("#span_password").html('')
        return true;
    }

}


function checknewPassword() {
    var pwd = $("#passwordnew_id").val();
    var p = new RegExp("^(?!^\\d+$)(?!^[a-zA-Z]+$)[0-9a-zA-Z]{4,23}")
    if (!p.test(pwd)) {
        $("#spannew_password").html('密码必需由字母和数字组合').css("color", 'red')
        return false;
    } else {
        $("#spannew_password").html('')
        return true;
    }

}


function checkrePassword() {
    var repwd = $("#repassword_id").val();
    var pwd = $("#passwordnew_id").val();
    if (repwd === pwd) {
        $("#span_repassword").html('')
        return true;

    } else {
        $("#span_repassword").html('二次密码不一致').css("color", 'red')
        return false;
    }

}


$('#resetpwd_id').click(function () {
    var res = checknewPassword() && checkPassword() && checkUsername() && checkrePassword();
    console.log("res", res)

    if (res === true) {

        $.ajax({
            url: '',
            type: 'post',
            data: {
                "username": $("#username_id").val(),
                "oldpwd": $("#password_id").val(),
                "newpwd": $("#passwordnew_id").val(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            success: function (data) {
                console.log(data)
                if (data.user != null) {
                    alert(data.msg)
                    location.href = '/user/signin/'

                } else {
                    alert(data.msg)
                }

            }
        })

    }


})


