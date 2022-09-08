$(function () {
    EDIT_UID = undefined;
    DELETE_UID = undefined;
    bindBtnEditEvent();
    bindConformEdit();
    bindBtnDeleteEvent();
    bindConformDelete();

})


function bindBtnEditEvent() {
    //点击编辑按钮编辑角色信息

    $('.system_edit').click(function () {
        //点击编辑显示模态对话框
        var system_edit = $(this).attr("system_edit");
        EDIT_UID = system_edit;
        //清空原始的checkbox的所有数据
        var check = document.getElementsByName("supervisored");
        for (let j = 0; j < check.length; j++) {
            check[j].checked = false;
        }
        $.ajax({
            url: '/djcp/editsystem/',
            type: 'GET',
            dataType: 'JSON',
            data: {"system_edit": system_edit},
            success: function (data) {
                console.log(data)
                if (!data.error) {
                    $('#ModalThree').modal('show');
                    $("#proname").val(data.system[0].proname);
                    $("#agentname").val(data.system[0].agentname);
                    $("#sys_name").val(data.system[0].sys_name);
                    $("#level").val(data.system[0].level);
                    $("#sys_service").val(data.system[0].sys_service);
                    $("#sys_obj").val(data.system[0].sys_obj);
                    $("#pro_num").val(data.system[0].pro_num);
                    $("#Record_num").val(data.system[0].Record_num);
                    $("#pm").val(data.system[0].pm);

                    $("#supervisor").val(data.system[0].supervisor);

                    $("#reporter").val(data.system[0].reporter_pro);
                    $("#desc").val(data.system[0].desc);
                    $("#bind_systeminfo").val(data.system[0].proinfo_id);


                    var supervisored = data.system[0].supervisored;
                    var ss = supervisored.match(/\d+/g)
                    console.log("supervisored", ss)
                    for (let j = 0; j < check.length; j++) {
                        for (let i = 0; i < ss.length; i++) {
                            if (check[j].value == ss[i]) {
                                check[j].checked = true;
                            }


                        }
                    }


                } else {
                    alert(data.error)
                }

            }
        })

    })

}


function bindConformEdit() {
    //点击确认编辑
    $("#conformbtn").click(function () {
            var form = $("#system_form").serialize();
            form = form + "&uuid=" + EDIT_UID;
            $.ajax({
                url: '/djcp/conformeditsystem/' + '?uuid=' + EDIT_UID,
                type: 'POST',
                dataType: 'JSON',
                data: form,
                success: function (data) {
                    console.log(data)
                    if (data.error) {
                        $('#prosyatemespan').html(data.error).css('color', 'red')
                    } else {
                        location.reload()
                    }
                    setTimeout(function () {
                        $('span.error').html('')
                    }, 1000)
                }
            })


        }
    )


}


function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".system_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("system_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/djcp/conformdelsystem/' + "?id=" + DELETE_UID,
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
    console.log(is_super,typeof(is_super))
    if (is_super == 'False') {
        setHiddenCol(document.getElementById('Table1'), 14)
    }

}
