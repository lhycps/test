$(function () {
    DELETE_UID = undefined;
    PER_DELETE = undefined;
    PER2_DELETE = undefined;
    EDIT_UID = undefined;
    EDIT2_UID = undefined;
    EDIT3_UID = undefined;
    TITLE_UID = undefined;
    PERMISSION_UID = undefined;
    bindBtnAddEvent();
    bindBtnDeleteEvent();
    bindBtnEditEvent();
    bindCloseBtn();
    bindaddoredit();
    bindConformDelete();
    ShowMenu2View();
    bindAddMenu2Event();

    bindmenu2addoredit();
    bindConformDeleteMenu2();

    bindAddPermissionEvent();
    bindpermissionaddoredit();
    bindConformDeletePermission();


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
        $("#addmenu_form")[0].reset();
        $("#myModalLabel").text('新增菜单信息')
        $('#ModalThree').modal('show');
        EDIT_UID = undefined;

    });

}


function bindaddoredit() {
    $("#addmenu_btn").click(function () {
        if (EDIT_UID === undefined) {

            bindConformAdd()
        } else {

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


function ShowMenu2View() {
    //点击菜单现实二级的界面
    $('.menutitle').click(function () {
        $('.menutitle').css('background', 'none')
        var menu_id = $(this).attr("menu_id");
        $('#' + menu_id).css('background', '#0dcaf0')
        TITLE_UID = menu_id;
        $.ajax({
            url: '/user/menu2/',
            type: 'GET',
            dataType: 'JSON',
            data: {"menu_id": menu_id},
            success: function (data) {

                $('#menu2').empty();
                $.each(data, function (i, datalist) {

                    var s = `
                    
                   <tr>
    <td>
        <li class="trigger Free">
            <button menu2_id="${datalist.id}" id="menu2_${datalist.id}" href="#0"
                    class=" main-btn success-btn-outline rounded-md btn-hover menutitletwo">${datalist.title}
                
            </button>
        </li>
    </td>
    <td>
        <p>${datalist.url}</p>
        <p>${datalist.name}</p>
    </td>
    <td>
        <ul class="action">
            <li class="action per2_edit" per2_edit="${datalist.id}">
                <button class="text-active">
                    <i class="lni lni-pencil-alt"></i>
                </button>
            </li>
            <li class="min-width per2_delete" per2_delete="${datalist.id}">
                <div class="action">
                    <button class="text-danger">
                        <i class="lni lni-trash-can"></i>
                    </button>
                </div>
            </li>
        </ul>
    </td>
</tr>
                    
                    
                    `
                    $("#menu2").append(s)

                })


            }
        })

    })

}

function bindAddMenu2Event() {
    //点击新增二级菜单按钮弹出模态对话框
    $("#add_menu2").click(function () {
        $("#addmenu2_form")[0].reset();//初始化数据
        $(".text-boldmenu2").text('新增二级菜单信息')
        $('#ModalThreeMenu2').modal('show');
    });

}

function bindmenu2addoredit() {
    $("#addper_btn").click(function () {
        if (EDIT2_UID === undefined) {
            bindConformMenu2Add()
        } else {

            bindConformMenu2Edit()

        }
    })
}

function bindConformMenu2Add() {
    //点击增加按钮增加二级菜单信息

    var title = $("#titlemenu2_id").val();
    var url = $("#urlmenu2_id").val();
    var name = $("#namemenu2_id").val();
    var form = $('#addmenu2_form').serialize()

    if (title.length === 0) {
        $("#addmenu2_span").html('标题不能为空').css('color', 'red')
    } else if (url.length === 0) {
        $("#addmenu2_span").html('url不能为空').css('color', 'red')
    } else if (name.length === 0) {
        $("#addmenu2_span").html('别名不能为空').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/addmenu2/',
            type: 'POST',
            data: form,
            dataType: 'JSON',
            success: function (data) {

                if (data.error) {
                    $("#addmenu2_span").html(data.error).css('color', 'red')
                } else {
                    alert(data.msg)
                    location.reload()

                }
                setTimeout(function () {
                    $("#addmenu2_span").html('')
                }, 1000)

            }
        })

    }
}


//二级菜单相关内容---显示
$("#menu2").on('click', '.menutitletwo', function () {
    //点击二级菜单弹出权限界面
    $('.menutitletwo').css('background', 'none')
    var menu2_id = $(this).attr("menu2_id");
    $('#menu2_' + menu2_id).css('background', '#20c997')
    $.ajax({
        url: '/user/permission/',
        type: 'GET',
        dataType: 'JSON',
        data: {"menu2_id": menu2_id},
        success: function (data) {
            $('#permission').empty();
            $.each(data, function (i, datalist) {

                var s = `<tr>
                    <td>
                        <li class="trigger Free">
                        <li>
                     <p>${datalist.title}</p>
                    </li>
                                                
                                      
                    </li>

                </td>
                    <td>
                        <p>${datalist.url}</p>
                        <p>${datalist.name}</p>
                    </td>   
                    <td>
                        <ul class="action">
                            <li class="action per3_edit" per3_edit="${datalist.id}">
                                <button class="text-active">
                                    <i class="lni lni-pencil-alt"></i>
                                </button>
                            </li>
                            <li class="min-width per3_delete" per3_delete="${datalist.id}">
                                <div class="action">
                                    <button class="text-danger">
                                        <i class="lni lni-trash-can"></i>
                                    </button>
                                </div>
                            </li>
                        </ul>
                    </td>
                    </tr>
                           `
                $("#permission").append(s)

            })


        }
    })

});
//二级菜单弹出删除
$('#menu2').on('click', '.per2_delete', function () {
    $('#delete_modelmenu2').modal('show');
    var per2_delete = $(this).attr("per2_delete");
    PER_DELETE = per2_delete
})

function bindConformDeleteMenu2() {
    //绑定确定删除事件的函数
    $("#delete_uidbtnmenu2").click(function () {
        $.ajax({
            url: '/user/conformedelmenu2/' + "?id=" + PER_DELETE,
            type: 'GET',
            data: {'delete_uid': PER_DELETE},
            dataType: 'JSON',
            success: function (data) {
                if (data.msg) {
                    alert(data.msg)
                    location.reload()
                } else {

                    alert(data.error)
                }
            }
        })

    })


}


//弹出编辑界面

$('#menu2').on('click', '.per2_edit', function () {
    console.log(44)
    var per2_edit = $(this).attr("per2_edit")
    EDIT2_UID = per2_edit;
    console.log("per2_edit", per2_edit)
    $.ajax({
        url: '/user/editmenu2/',
        type: 'GET',
        dataType: 'JSON',
        data: {"per2_edit": per2_edit},
        success: function (data) {
            console.log("data111", data)
            if (!data.error) {
                $("#titlemenu2_id").val(data[0].title);
                $("#urlmenu2_id").val(data[0].url);
                $("#namemenu2_id").val(data[0].name);
                $("#bind_menu_id").val(data[0].menu_id);
                $(".text-boldmenu2").text('编辑二级菜单')
                $('#ModalThreeMenu2').modal('show');
            } else {
                alert(data.error)
            }


        }
    })


})

//确认编辑
function bindConformMenu2Edit() {
    //点击增加按钮编辑二级菜单信息
    var title = $("#titlemenu2_id").val();
    var url = $("#urlmenu2_id").val();
    var name = $("#namemenu2_id").val();
    var form = $('#addmenu2_form').serialize() + '&uuid=' + EDIT2_UID
    if (title.length === 0) {
        $("#addmenu2_span").html('标题不能为空').css('color', 'red')
    } else if (url.length === 0) {
        $("#addmenu2_span").html('url不能为空').css('color', 'red')
    } else if (name.length === 0) {
        $("#addmenu2_span").html('别名不能为空').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/conformeditmenu2/',
            type: 'POST',
            data: form,
            dataType: 'JSON',
            success: function (data) {
                if (data.error) {
                    $("#addmenu2_span").html(data.error).css('color', 'red')
                } else {
                    alert(data.msg)
                    location.reload()

                }
                setTimeout(function () {
                    $("#addmenu2_span").html('')
                }, 1000)

            }
        })

    }
}


//弹出权限的界面
function bindAddPermissionEvent() {
    //点击新增权限按钮弹出模态对话框
    $("#add_menu3").click(function () {
        $('#permission_form')[0].reset();
        $(".text-boldmenu3").text('新增权限信息')
        $('#ModalThreepermission').modal('show');


    });

}

function bindpermissionaddoredit() {
    $("#permission_btn").click(function () {
        if (EDIT3_UID === undefined) {
            bindConformPermissoonAdd()
        } else {
            bindConformPermissoonEdit()

        }
    })
}

function bindConformPermissoonAdd() {
    //确认增加权限
    //点击增加按钮增加二级菜单信息
    var title = $("#permissiontitle_id").val();
    var url = $("#permissionurl_id").val();
    var name = $("#permissionname_id").val();
    var form = $('#permission_form').serialize()
    if (title.length === 0) {
        $("#addpermission_span").html('标题不能为空').css('color', 'red')
    } else if (url.length === 0) {
        $("#addpermission_span").html('url不能为空').css('color', 'red')
    } else if (name.length === 0) {
        $("#addpermission_span").html('别名不能为空').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/addpermission/',
            type: 'POST',
            data: form,
            dataType: 'JSON',
            success: function (data) {
                if (data.error) {
                    $("#addpermission_span").html(data.error).css('color', 'red')
                } else {
                    alert(data.msg)
                    location.reload()
                }
                setTimeout(function () {
                    $("#addpermission_span").html('')
                }, 1000)

            }
        })

    }

}


//弹出权限的边界界面
$('#permission').on('click', '.per3_edit', function () {
    var per3_edit = $(this).attr("per3_edit")
    EDIT3_UID = per3_edit;
    $.ajax({
        url: '/user/editpermission/',
        type: 'GET',
        dataType: 'JSON',
        data: {"per3_edit": per3_edit},
        success: function (data) {
            console.log("data", data)
            if (!data.error) {
                $("#permissiontitle_id").val(data[0].title);
                $("#permissionurl_id").val(data[0].url);
                $("#permissionname_id").val(data[0].name);
                $("#bind_permission").val(data[0].pid_id);
                $(".text-boldmenu3").text('编辑权限信息')
                $('#ModalThreepermission').modal('show');
            } else {
                alert(data.error)
            }


        }
    })


})

function bindConformPermissoonEdit() {
    //确认编辑权限
    var title = $("#permissiontitle_id").val();
    var url = $("#permissionurl_id").val();
    var name = $("#permissionname_id").val();
    var form = $('#permission_form').serialize() + '&uuid=' + EDIT3_UID
    if (title.length === 0) {
        $("#addpermission_span").html('标题不能为空').css('color', 'red')
    } else if (url.length === 0) {
        $("#addpermission_span").html('url不能为空').css('color', 'red')
    } else if (name.length === 0) {
        $("#addpermission_span").html('别名不能为空').css('color', 'red')
    } else {
        $.ajax({
            url: '/user/conformeditpermission/',
            type: 'POST',
            data: form,
            dataType: 'JSON',
            success: function (data) {
                if (data.error) {
                    $("#addpermission_span").html(data.error).css('color', 'red')
                } else {
                    alert(data.msg)
                    location.reload()
                }
                setTimeout(function () {
                    $("#addpermission_span").html('')
                }, 1000)

            }
        })

    }

}


//权限弹出删除
$('#permission').on('click', '.per3_delete', function () {
    $('#delete_modelpermission').modal('show');
    var per3_delete = $(this).attr("per3_delete");
    PER2_DELETE = per3_delete
})

function bindConformDeletePermission() {
    //绑定确定删除事件的函数
    $("#delete_uidbtnpermission").click(function () {
        $.ajax({
            url: '/user/conformedelpermission/' + "?id=" + PER2_DELETE,
            type: 'GET',
            data: {'delete_uid': PER2_DELETE},
            dataType: 'JSON',
            success: function (data) {
                if (data.msg) {
                    alert(data.msg)
                    location.reload()
                } else {

                    alert(data.error)
                }
            }
        })

    })


}



