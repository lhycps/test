$(function () {
    EDIT_UID = undefined;
    DELETE_UID = undefined;
    bindBtnEditEvent();
    bindCloseBtn();
    bindConformEdit();
    bindBtnDeleteEvent();
    bindConformDelete();
})

function bindBtnEditEvent() {
    //点击编辑按钮编辑角色信息
    $('.gmanager_edit').click(function () {
        //点击编辑显示模态对话框
        var gmanager_edit = $(this).attr("gmanager_edit");
        EDIT_UID = gmanager_edit;
        $.ajax({
            url: '/djcp/editgmanager/',
            type: 'GET',
            dataType: 'JSON',
            data: {"gmanager_edit": gmanager_edit},
            success: function (data) {
                console.log(data)
                if (!data.error) {
                    $('#gmanagerModel').modal('show');
                    $("#myModalLabel").text('编辑负责人信息');
                    $("#id_gname").val(data.gmanager[0].gmanager);
                    $("#id_gemail").val(data.gmanager[0].gemail);
                    $("#id_gpost").val(data.gmanager[0].gpost);
                    $("#id_gphone").val(data.gmanager[0].gphone);
                    $("#id_gtelephone").val(data.gmanager[0].gtelephone);
                    $("#bind_unitgmanager").val(data.gmanager[0].gnameinfo);
                } else {
                    alert(data.error)
                }

            }
        })

    })

}

function bindConformEdit() {
    //点击确认编辑
    $("#addgmanager_btn").click(function () {
        var form = $("#gmanagerform_id").serialize();
        var blins_unit = $("#bind_unitgmanager").val()
        if (blins_unit === '0') {
            $('#select_unit').html('未绑定单位').css('color', 'red');
            setTimeout(function () {
                $('#select_unit').html('')
            }, 1000)
        } else {
            form = form + "&uuid=" + EDIT_UID + "&bind_unitgmanager=" + blins_unit;
            $.ajax({
                url: '/djcp/conformeditgmanager/' + '?uuid=' + EDIT_UID,
                type: 'POST',
                dataType: 'JSON',
                data: form,
                success: function (data) {
                    if (data.error) {
                        $('span.error').html('')
                        $.each(data.error, function (i, errorlist) {
                            console.log(i, errorlist[0])
                            $('#id_' + i).next().html(errorlist[0])

                        })

                    } else {
                        location.reload()
                    }
                    setTimeout(function () {
                        $('span.error').html('')
                    }, 1000)
                }
            })
        }

    })


}

function bindCloseBtn() {
    //关闭模态框
    $("#closegmanager_btn").click(function () {
        $('#gmanagerModel').modal('hide');
    })
}

function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".gmanager_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("gmanager_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/djcp/conformdelgmanager/' + "?id=" + DELETE_UID,
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


function setHiddenCol(oTable, iCol) {
    //影藏表格中的列
    for (i = 0; i < oTable.rows.length; i++) {
        oTable.rows[i].cells[iCol].style.display = oTable.rows[i].cells[iCol].style.display == "none" ? "" : "none";
    }

}

window.onload = function hiddle_col() {
    var is_super = $("#Table1").attr('is_super');
    console.log(is_super, typeof (is_super))
    if (is_super == 'False') {
        setHiddenCol(document.getElementById('Table1'), 6)
    }

}
