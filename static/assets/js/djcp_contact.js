$(".contact").click(function () {
    //添加联系人信息
    var blins_unit = $("#bind_unitcontact").val()
    if (blins_unit === '0') {
        $('#select_unit').html('未绑定单位').css('color', 'red')
    } else {
        $('#select_unit').html('')
        $.ajax({
            url: "/djcp/contact/",
            type: 'POST',
            data: $("#contactform_id").serialize(),
            dataType: 'JSON',
            success: function (data) {
                if (data.error) {
                    $('span.error').html('')
                    $.each(data.error, function (i, errorlist) {
                        console.log(i, errorlist[0])
                        $('#id_' + i).next().html(errorlist[0])
                    })
                    messagess(data.error, 'danger')
                } else {
                    messagess(data.msg, 'success')
                }
                setTimeout(function () {
                    $('span.error').html('')
                }, 1000)
            }
        })
    }

})


$(".manage").click(function () {
    //添加负责人信息
    var blins_gunit = $("#bind_gunitcontact").val()
    if (blins_gunit === '0') {
        $('#gselect_unit').html('未绑定单位').css('color', 'red')
    } else {
        $('#gselect_unit').html('')
        $.ajax({
                url: "/djcp/gmanagerInfo/",
                type: 'POST',
                data: $("#gcontactform_id").serialize(),
                dataType: 'JSON',
                success: function (data) {
                    if (data.error) {
                        $('span.gerror').html('')
                        $.each(data.error, function (i, errorlist) {
                            console.log(i, errorlist[0])
                            $('#id_' + i).next().html(errorlist[0])
                        })
                        messagess(data.error, 'danger')
                    } else {
                        messagess(data.msg, 'success')
                    }
                    setTimeout(function () {
                        $('span.gerror').html('')
                    }, 1000)

                }
            }
        )
    }
})

// layer({
//     title: '我是标题',
//     content: '我是内容',
//     type: 'success',
//     // buttons: {
//     //     confirm: function (e) {
//     //         alert("您点击确认按钮")
//     //     },
//     //     cancel: function (e) {
//     //         alert("您点击取消按钮")
//     //         e.fadeout()
//     //     },
//     //     close: function (e) {
//     //         alert("您点击关闭按钮")
//     //         e.fadeout()
//     //     }
//     // }
// })
