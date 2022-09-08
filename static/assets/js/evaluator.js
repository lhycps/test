$(function () {
    DELETE_UID = undefined;
    EDIT_UID = undefined;
    bindBtnAddEvent();
    closebtn();
    bindMenBtnSave();
    bindBtnDeleteEvent();
    bindBtnEditEvent();
    bindConformDelete();


})


function bindBtnAddEvent() {
    //点击增加人员按钮弹出模态对话框
    $("#add_men").click(function () {
        //清空对话框中的数据
        $("#addmen_form")[0].reset();
        EDIT_UID = undefined;
        $("#myModalLabel").text('增加人员')
        $('#addmenModel').modal('show');


    });

}

function closebtn() {
    //点击关闭按钮关闭模态对话框
    $("#closemen_btn").click(function () {
        $('#addmenModel').modal('hide');
        location.reload()

    })


}

function bindMenBtnSave() {
    $("#addmen_btn").click(function () {
            if (EDIT_UID === undefined) {
                conformadd()

            } else {
                conformedit()

            }
        }
    )


}

function isPhoneNumber(tel) {
    var reg = /^0?1[3|4|5|6|7|8][0-9]\d{8}$/;
    return reg.test(tel);
}

function getroleval() {
    var all = "";
    $("select option").each(function () {
        all += $(this).attr("value") + " ";
    });
    return sel = $("select").val();
}


function conformadd() {
    var name = $("#name").val();
    var address = $("#address").val();
    var phone = $("#phone").val();
    var role = getroleval();

    if (name.length === 0) {
        $("#name_span").html('姓名不能为空').css('color', 'red')
    } else if (address.length === 0) {
        $("#address_span").html('地址不能为空').css('color', 'red')
    } else if (!isPhoneNumber(phone)) {
        $("#phone_span").html('电话号码格式不正确').css('color', 'red')
    } else if (role.length === 0) {
        $("#role_span").html('未勾选角色信息').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/addmen/',
            type: 'post',
            data: $("#addmen_form").serialize(),
            dataType: "JSON",
            success: function (data) {
                console.log("data", data)
                if (data.error) {
                    alert(data.error);
                } else {
                    alert(data.msg);
                    $("#addmen_form")[0].reset();

                }
                setTimeout(function () {
                    $("#addmen_span").html('')

                }, 1000)


            }

        })
    }
    setTimeout(function () {
        $("#name_span").html('')
        $("#address_span").html('')
        $("#role_span").html('')
        $("#phone_span").html('')


    }, 1000)


}


function conformedit() {
    var name = $("#name").val();
    var address = $("#address").val();
    var phone = $("#phone").val();
    var role = getroleval();
    if (name.length === 0) {
        $("#name_span").html('姓名不能为空').css('color', 'red')
    } else if (address.length === 0) {
        $("#address_span").html('地址不能为空').css('color', 'red')
    } else if (!isPhoneNumber(phone)) {
        $("#phone_span").html('电话号码格式不正确').css('color', 'red')
    } else if (role.length === 0) {
        $("#role_span").html('未勾选角色信息').css('color', 'red')
    } else {
        $.ajax({
            url: "/user/conforeditmen/" + "?id=" + EDIT_UID,
            type: 'post',
            data: {
                "uid": EDIT_UID,
                "name": name,
                "address": address,
                "phone": phone,
                "role": role,
            },
            dataType: "JSON",
            success: function (data) {
                if (data.error) {
                    console.log(data.error)
                } else {
                    alert(data.msg)
                    location.reload()
                }
                setTimeout(function () {
                    $("#addmen_span").html('')

                }, 1000)


            }

        })
    }


}

function bindBtnDeleteEvent() {
    $(".men_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("men_delete");
        DELETE_UID = delete_uid;
        console.log(DELETE_UID);
    });
}

function bindConformDelete() {
    $("#delete_uidbtn").click(function () {
        var role = getroleval();
        console.log(role)
        $.ajax({
            url: '/user/conforedelmen/' + '?id=' + DELETE_UID,
            type: 'GET',
            data: {
                'delete_uid': DELETE_UID,
                "role": role,
            },
            dataType: 'JSON',
            success: function (data) {
                if (data.msg) {
                    location.reload()
                } else {
                    alert(data.error)
                }

            }
        })

    })


}

function bindBtnEditEvent() {
    $('.men_edit').click(function () {
        //点击编辑显示模态对话框
        var edit_uid = $(this).attr('men_editid');
        EDIT_UID = edit_uid;
        console.log(EDIT_UID)
        $.ajax({
            url: '/user/editmen/' + '?id=' + EDIT_UID,
            type: 'GET',
            dataType: 'JSON',
            data: {"edit_uid": edit_uid},
            success: function (data) {
                var m = JSON.parse(data.roleobj)
                var arr = new Array()
                $.each(m, function (i, mlist) {
                    console.log(mlist.pk)
                    arr.push(mlist.pk)
                })
                if (!data.error) {
                    $("#name").val(data.eva[0].name);
                    $("#address").val(data.eva[0].address);
                    $("#phone").val(data.eva[0].phone);
                    $("#role").val(arr);
                    $("#myModalLabel").text('编辑人员');
                    $('#addmenModel').modal('show');
                }
            }
        })

    })

}

