function checkUsername() {
    var username = $('#username_id').val();
    if (username.length < 6) {
        $('#span_username').html('未通过校验，长度小于6位').css("color", "red")
        return false;
    } else {
        return $.getJSON('/user/checkuname/', {username: username}, function (data) {
            if (data.msg == null) {
                $('#span_username').html('恭喜您，用户名可用').css("color", "green")
                return true;
            } else {
                $('#span_username').html('该用户已注册').css("color", "red")
                return false;

            }

        })


    }

}


function checkEmail() {
    var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"); //正则表达式
    var email = $("#email_id").val();
    if (email === "") {
        $('#span_email').html('邮箱不能为空').css("color", "red")
        return false;
    } else if (!reg.test(email)) {
        $('#span_email').html('邮箱格式不正确').css("color", "red")
        return false;
    } else {
        $('#span_email').html('邮箱验证通过').css("color", "green")
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
        $("#span_password").html('密码校验通过').css("color", 'green')
        return true;
    }

}


function checkrePassword() {
    var repwd = $("#repassword_id").val();
    var pwd = $("#password_id").val();
    if (repwd === pwd) {
        $("#span_repassword").html('密码校验通过').css("color", 'green')
        return true;

    } else {
        $("#span_repassword").html('二次密码不一致').css("color", 'red')
        return false;
    }

}


$('#regrr').click(function () {
    var agree = $("#checkbox-not-robot").is(':checked')
    if (agree === false) {
        $("#span_agreen").html('请勾选已同意').css('color', 'red')
    } else {
        $("#span_agreen").html('')
    }
    var res = checkEmail() && checkPassword() && checkUsername() && checkrePassword() && agree;

    if (res === true) {

        $.ajax({
            url: '',
            type: 'post',
            data: {
                "username": $("#username_id").val(),
                "pwd": $("#password_id").val(),
                "email": $("#email_id").val(),
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
            },
            success: function (data) {
                if (data.mag == null) {
                    location.href = '/user/signin/'
                } else {
                    alert('注册失败')
                }

            }
        })

    }


})


