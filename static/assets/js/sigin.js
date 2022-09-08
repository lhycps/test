//登录时间
$("#signin_id").click(function () {
    var username = $("#user_id").val();
    var pwd = $("#pwd_id").val();
    var remember = $("#checkbox-remember").is(':checked')
    if (username.length === 0) {
        $("#span_sigin").html('用户名不能为空').css('color', 'red')

    } else if (pwd.length === 0) {
        $("#span_sigin").html('密码不能为空').css('color', 'red')
    } else {
        $.ajax({
            url: "",
            type: "post",
            data: {
                "username": username,
                "pwd": pwd,
                "remember": remember,
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                console.log(data.remember_cookie)
                if (data.user === null) {
                    $("#span_sigin").html(data.msg).css('color', 'red')

                } else if (data.user === "0") {
                    $("#span_sigin").html('<p>您的邮箱未激活，请前往 <a href="/user/active_account/">激活</a>，否则无法登录</p>').css('color', "red")
                } else {
                    if (data.remember_cookie) {
                        //存储cookie
                        $.cookie('remember_cookie', data.remember_cookie, {
                            'expires': 15,
                            'path': '/',
                            // 'domain': '127.0.0.1'
                        });
                        console.log(data.remember_cookie)
                    }
                    location.href = '/user/index/'
                }


            }
        })
    }

})

//获取rember_cookie的信息展示到前端input框中
$(function () {
    var value = $.cookie('remember_cookie');
    if (value) {
        value = $.base64.decode(value);
        $('#user_id').val(value.split('&')[0]);
        $('#pwd_id').val(value.split('&')[1]);
        $('#checkbox-remember')[0].checked = true
    }
})


// 解决session过期跳转登录页，并跳出iframe框架
$(function () {
    if (window != window.top) {
        window.top.location = '/user/signin/';
    }
});