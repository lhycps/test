$(function () {

    DELETE_UID = undefined;
    EDIT_UID = undefined;
    bindBtnAddEvent();
    bindBtnDeleteEvent();
    bindBtnEditEvent();
    bindCloseBtn();
    bindaddoredit();
    bindConformDelete();


})

function bindCloseBtn() {
    //点击增加角色信息的关闭按钮，关闭模态框
    $("#closerole_btn").click(function () {
        $('#addroleModel').modal('hide');

    })

}

function bindBtnAddEvent() {
    //点击新增角色按钮弹出模态对话框
    $("#add_role").click(function () {
        $("#myModalLabel").text('新增角色信息')
        $('#addroleModel').modal('show');
        EDIT_UID = undefined;

    });

}


function bindaddoredit() {
    $("#addrole_btn").click(function () {
        if (EDIT_UID === undefined) {
            console.log('进入增加界面')
            bindConformAdd()
        } else {
            console.log('进入编辑界面')
            bindConformEdit()

        }
    })
}


function bindConformAdd() {
    //点击增加按钮增加角色信息

    var name = $("#addrole").val();
    var permission = $("#permission").val();
    console.log(permission)
    if (name.length === 0) {
        $("#addrole_span").html('角色标题不能为空').css('color', 'red')
    } else if (permission.length === 0) {
        $("#addrole_span").html('未勾选权限').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/addrole/',
            type: 'POST',
            data: $('#addrole_form').serialize(),
            dataType: 'JSON',
            success: function (data) {
                if (data.error) {
                    $("#addrole_span").html(data.error).css('color', 'red')
                } else {
                    location.reload()
                }
                setTimeout(function () {
                    $("#addrole_span").html('')
                }, 1000)

            }
        })

    }
}


function bindBtnEditEvent() {
    //点击编辑按钮编辑角色信息
    $('.role_edit').click(function () {
        //点击编辑显示模态对话框
        var role_edit = $(this).attr("role_editid")
        EDIT_UID = role_edit;
        $.ajax({
            url: '/user/editrole/' + "?id=" + EDIT_UID,
            type: 'GET',
            dataType: 'JSON',
            data: {"role_edit": role_edit},
            success: function (data) {
                console.log(data)
                var m = JSON.parse(data.permission)
                var arr = new Array()
                $.each(m, function (i, mlist) {
                    arr.push(mlist.pk)
                })
                if (!data.error) {
                    $('#addroleModel').modal('show');
                    $("#myModalLabel").text('编辑角色');
                    var addrole = data.role[0].title;
                    $("#addrole").val(addrole);
                    $("#permission").val(arr);
                } else {
                    alert(data.error)
                }

            }
        })

    })

}


function bindConformEdit() {
    //点击确认编辑
    var name = $("#addrole").val();
    var permission = $("#permission").val();
    console.log(permission)
    if (name.length === 0) {
        $("#addrole_span").html('角色标题不能为空').css('color', 'red')
    } else if (permission.length === 0) {
        $("#addrole_span").html('未勾选权限').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/conformedit/' + "?id=" + EDIT_UID,
            type: 'POST',
            dataType: 'JSON',
            data: {
                'role_edit': EDIT_UID,
                'addrole': $("#addrole").val(),
                'permission': $("#permission").val(),
            },
            success: function (data) {
                if (data.msg) {
                    location.reload()
                } else {
                    alert(data.error)
                }
            }
        })

    }
}

function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".role_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("role_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        console.log('/user/conformedel/' + "?id=" + DELETE_UID)
        $.ajax({
            url: '/user/conformedel/' + "?id=" + DELETE_UID,
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



