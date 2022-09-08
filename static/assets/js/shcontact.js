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
    $('.contact_edit').click(function () {
        //点击编辑显示模态对话框
        var contact_edit = $(this).attr("contact_edit");
        EDIT_UID = contact_edit;
        $.ajax({
            url: '/djcp/editcontact/',
            type: 'GET',
            dataType: 'JSON',
            data: {"contact_edit": contact_edit},
            success: function (data) {
                if (!data.error) {
                    $('#contactModel').modal('show');
                    $("#myModalLabel").text('编辑联系人信息');
                    $("#id_name").val(data.contact[0].name);
                    $("#id_email").val(data.contact[0].email);
                    $("#id_post").val(data.contact[0].post);
                    $("#id_phone").val(data.contact[0].phone);
                    $("#id_telephone").val(data.contact[0].telephone);
                    $("#bind_unitcontact").val(data.contact[0].nameinfo);
                } else {
                    alert(data.error)
                }

            }
        })

    })

}

function bindConformEdit() {
    //点击确认编辑
    $("#addcontact_btn").click(function () {
        var form = $("#contactform_id").serialize();
        var blins_unit = $("#bind_unitcontact").val()
        if (blins_unit === '0') {
            $('#select_unit').html('未绑定单位').css('color', 'red');
            setTimeout(function () {
                $('#select_unit').html('')
            }, 1000)
        } else {
            form = form + "&uuid=" + EDIT_UID + "&bind_unitcontact=" + blins_unit;
            $.ajax({
                url: '/djcp/conformeditcontact/' + '?uuid=' + EDIT_UID,
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
    $("#closecontact_btn").click(function () {
        $('#contactModel').modal('hide');
    })
}

function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".contact_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("contact_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/djcp/conformdelcontact/' + "?id=" + DELETE_UID,
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
    if (is_super == 'False') {
        setHiddenCol(document.getElementById('Table1'), 6)
    }
}





