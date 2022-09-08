$(function () {
    DELETE_UID = undefined;
    EDIT_UID = undefined;
    TITLE_UID = undefined;
    bindBtnAddEvent();
    bindBtnDeleteEvent();
    bindBtnEditEvent();
    bindCloseBtn();
    bindaddoredit();
    bindConformDelete();
    ShowPermissionView();


})

function bindCloseBtn() {
    //点击增加菜单信息的关闭按钮，关闭模态框
    $("#closemenu_btn").click(function () {
        $('#addmenuModel').modal('hide');

    })

}

function bindBtnAddEvent() {
    //点击新增菜单按钮弹出模态对话框
    $("#add_menu").click(function () {
        console.log(111)
        $("#myModalLabel").text('新增菜单信息')
        $('#ModalThree').modal('show');
        EDIT_UID = undefined;

    });

}


function bindaddoredit() {
    $("#addmenu_btn").click(function () {
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
    //点击增加按钮增加菜单信息
    var title = $("#addmenu").val();
    var icon = $("#icon_id").val();
    if (title.length === 0) {
        $("#addmenu_span").html('标题不能为空').css('color', 'red')
    } else if (icon.length === 0) {
        $("#addmenu_span").html('图标不能为空').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/addmenu/',
            type: 'POST',
            data: $('#addmenu_form').serialize(),
            dataType: 'JSON',
            success: function (data) {
                console.log(data)
                if (data.error) {
                    $("#addmenu_span").html(data.error).css('color', 'red')
                } else {
                    location.reload()
                }
                setTimeout(function () {
                    $("#addmenu_span").html('')
                }, 1000)

            }
        })

    }
}


function bindBtnEditEvent() {
    //点击编辑按钮编辑菜单信息
    $('.menu_edit').click(function () {
        //点击编辑显示模态对话框
        var menu_edit = $(this).attr("menu_editid")
        EDIT_UID = menu_edit;
        $.ajax({
            url: '/user/editmenu/' + "?id=" + EDIT_UID,
            type: 'GET',
            dataType: 'JSON',
            data: {"menu_edit": menu_edit},
            success: function (data) {
                console.log(data)
                if (!data.error) {
                    $('#ModalThree').modal('show');
                    $(".text-bold").text('编辑菜单');
                    $("#addmenu").val(data[0].title);
                    $("#icon_id").val(data[0].icon);
                } else {
                    alert(data.error)
                }

            }
        })

    })

}


function bindConformEdit() {
    //点击确认编辑
    var menu = $("#addmenu").val();
    var icon = $("#icon_id").val();
    if (menu.length === 0) {
        $("#addmenu_span").html('标题不能为空').css('color', 'red')
    } else if (icon.length === 0) {
        $("#addmenu_span").html('图标不能为空').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/conformeditmenu/' + "?id=" + EDIT_UID,
            type: 'POST',
            dataType: 'JSON',
            data: {
                'menu_edit': EDIT_UID,
                'title': $("#addmenu").val(),
                'icon': $("#icon_id").val(),
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
    $(".menu_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("menu_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        console.log('/user/conforedelmenu/' + "?id=" + DELETE_UID)
        $.ajax({
            url: '/user/conforedelmenu/' + "?id=" + DELETE_UID,
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


//权限相关的界面用到的js
function ShowPermissionView1() {
    //点击菜单现实权限的界面
    $('.menutitle').click(function () {
        $('.menutitle').css('background', 'none')
        var menu_id = $(this).attr("menu_id");
        $('#' + menu_id).css('background', '#0dcaf0')
        $(this).addClass = 'active2';
        TITLE_UID = menu_id;
        console.log("menu_id", menu_id)
        $.ajax({
            url: '/user/permission/',
            type: 'GET',
            dataType: 'JSON',
            data: {"menu_id": menu_id},
            success: function (data) {
                $('#permissionlist').empty();
                $.each(data, function (i, datalist) {
                    var s = `<tr>

                        <td>
                            <p>${datalist.title}</p>
                        </td>
                        <td>
                            <p>${datalist.url}</p>
                        </td>
                        <td>
                            <p>${datalist.name}</p>
                        </td>
                        <td>
                            <li class="action">
                                    <button class=" text-orange">
                                        <i class="lni lni-link"></i>
                                    </button>
                             </li>
                        </td>
  
                        <td>
                            <ul class="action">
                                <li class="action per_edit" per_edit="${datalist.id}">
                                    <button class="text-active">
                                        <i class="lni lni-pencil-alt"></i>
                                    </button>
                                </li>
                                <li class="min-width per_delete"
                                    per_delete="${datalist.id}">
                                    <div class="action">
                                        <button class="text-danger">
                                            <i class="lni lni-trash-can"></i>
                                        </button>
                                    </div>
                                </li>
                            </ul>
                        </td>
                    </tr>`
                    $("#permissionlist").append(s)

                })

                console.log(data)

            }
        })

    })

}

function ShowPermissionView() {
    //点击菜单现实权限的界面
    $('.menutitle').click(function () {
        $('.menutitle').css('background', 'none')
        var menu_id = $(this).attr("menu_id");
        $('#' + menu_id).css('background', '#0dcaf0')
        $(this).addClass = 'active2';
        TITLE_UID = menu_id;

        $.ajax({
            url: '/user/permission/',
            type: 'GET',
            dataType: 'JSON',
            data: {"menu_id": menu_id},
            success: function (data) {
                $('#permissionlist').empty();
                $.each(data, function (i, datalist) {
                    var s = `<tr id="uu" style="background-color:rgb(192,192,192,0.3)">
                                            <td>
                                                <li class="trigger Free">
                                                    <i class="lni lni-angle-double-down"></i>
                                                    <i class=" lni lni-angle-double-up" style="display: none"></i>
                                                    <p style="display: inline-block">&nbsp;&nbsp;${datalist.title}</p>
                                                </li>

                                            </td>
                                            <td>
                                                <p>${datalist.url}</p>
                                            </td>
                                            <td>
                                                <p>${datalist.name}</p>
                                            </td>
                                            <td>
                                                <p>是</p>
                                            </td>
                                            <td>
                                                <p>${datalist.menu__title}</p>
                                            </td>
                                            <td>
                                                <ul class="action">
                                                    <li class="action per_edit" per_edit="3">
                                                        <button class="text-active">
                                                            <i class="lni lni-pencil-alt"></i>
                                                        </button>
                                                    </li>
                                                    <li class="min-width per_delete" per_delete="3">
                                                        <div class="action">
                                                            <button class="text-danger">
                                                                <i class="lni lni-trash-can"></i>
                                                            </button>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </td>
                                        </tr>
                            <tr class="aa">
                                            <td>
                                                <p style="display: inline-block">单位111/系统</p>
                                            </td>
                                            <td>
                                                <p>/djcp/unitinfo/</p>
                                            </td>
                                            <td>
                                                <p>unitinfo</p>
                                            </td>
                                            <td>
                                                <p>/djcp/unitinfo/</p>
                                            </td>
                                            <td>
                                                <p>/djcp/unitinfo/</p>
                                            </td>
                                            <td>
                                                <ul class="action">
                                                    <li class="action per_edit" per_edit="3">
                                                        <button class="text-active">
                                                            <i class="lni lni-pencil-alt"></i>
                                                        </button>
                                                    </li>
                                                    <li class="min-width per_delete" per_delete="3">
                                                        <div class="action">
                                                            <button class="text-danger">
                                                                <i class="lni lni-trash-can"></i>
                                                            </button>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </td>


                                        </tr>`
                    $("#permissionlist").append(s)

                })


            }
        })

    })

}


$("#uu").click(function () {
    if ($('.aa').is(":hidden")) {
        $('.aa').show()
        $('.lni-angle-double-down').css('display', 'inline-block')
        $('.lni-angle-double-up').css('display', 'none')


    } else {
        $('.aa').hide()
        $('.lni-angle-double-down').css('display', 'none')
        $('.lni-angle-double-up').css('display', 'inline-block')

    }

})



