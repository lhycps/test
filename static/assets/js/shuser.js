$(function () {
    EDIT_UID = undefined;
    DELETE_UID = undefined;
    bindBtnEditEvent();
    bindBtnDeleteEvent();
    bindConformDelete();

})

function bindBtnEditEvent() {

    //弹出编辑模态对话框
    $('.user_edit').click(function () {
        console.log(11)
        //点击编辑显示模态对话框
        var edit_uid = $(this).attr('user_edit');
        EDIT_UID = edit_uid;
        console.log(EDIT_UID)
        $.ajax({
            url: '/user/edituser/',
            type: 'GET',
            dataType: 'JSON',
            data: {"edit_uid": edit_uid},
            success: function (data) {
                console.log(data)
                var m = JSON.parse(data.roleobj)
                var arr = new Array()
                $.each(m, function (i, mlist) {
                    console.log(mlist.pk)
                    arr.push(mlist.pk)
                })
                if (!data.error) {
                    $("#name_id").val(data.user[0].name);
                    $("#phone_id").val(data.user[0].phone);
                    $("#email_id").val(data.user[0].email);
                    $("#role").val(arr);
                    $('#ModalThree').modal('show');
                }
            }
        })

    })

}

function getroleval() {
    var all = "";
    $("select option").each(function () {
        all += $(this).attr("value") + " ";
    });
    return sel = $("select").val();
}


$('#adduser_btn').click(function () {
    //确定编辑的函数
    var name = $("#name_id").val();
    var email = $("#email_id").val();
    var phone = $("#phone_id").val();
    var role = getroleval();
    if (role.length === 0) {
        $("#role_span").html('未勾选角色信息').css('color', 'red');
        setTimeout(function () {
            $("#role_span").html('')

        }, 1000)
    } else {
        $.ajax({
            url: "/user/conformedituser/",
            type: 'post',
            data: {
                "uid": EDIT_UID,
                "name": name,
                "email": email,
                "phone": phone,
                "role": role,
            },
            dataType: "JSON",
            success: function (data) {
                if (data.error) {
                    console.log(data.error);

                } else {

                    location.reload()

                }
                setTimeout(function () {
                    $("#adduser_span").html('')

                }, 1000)


            }

        })
    }
})


function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".user_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("user_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/user/conformedeluser/' + "?id=" + DELETE_UID,
            type: 'GET',
            data: {'delete_uid': DELETE_UID},
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



