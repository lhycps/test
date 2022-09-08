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
    $('.unit_edit').click(function () {
        //点击编辑显示模态对话框
        var unit_edit = $(this).attr("unit_edit");
        EDIT_UID = unit_edit;
        $.ajax({
            url: '/djcp/editunit/',
            type: 'GET',
            dataType: 'JSON',
            data: {"unit_edit": unit_edit},
            success: function (data) {
                console.log(data)
                if (!data.error) {
                    $('#unitModel').modal('show');
                    $("#myModalLabel").text('编辑联系人信息');
                    $("#unit_name").val(data.unit[0].unit_name);
                    $("#address").val(data.unit[0].address);
                    $("#desc").val(data.unit[0].company_profile);
                    $("#nature").val(data.unit[0].nature);
                    $("#code").val(data.unit[0].code);
                    $("#department").val(data.unit[0].department);
                    $("#superdepartment").val(data.unit[0].superdepar);
                } else {
                    alert(data.error)
                }

            }
        })

    })

}

function ischeck() {
    var code = document.getElementById("code").value;
    if (code != "") {   //邮政编码判断
        var pattern = /^[0-9]{6}$/;
        flag = pattern.test(code);
        if (!flag) {
            return false;
        } else {
            return true;
        }
    } else {
        return false;
    }
}

function bindConformEdit() {
    //点击确认编辑
    $("#addunit_btn").click(function () {
        var form = $("#unitform_id").serialize();
        var blins_unit = $("#bind_unitunit").val()
        var coderes = ischeck().toString();
        var unit_name = $("#unit_name").val();
        var address = $("#address").val();
        var nature = $("#nature").val();
        var code = $("#code").val();
        var desc = $("#desc").val();
        var department = $("#department").val();
        var superdepartment = $("#superdepartment").val();
        if (unit_name.length === 0) {
            $("#unit_span").html('单位名称不能为空').css('color', 'red')
        } else if (address.length === 0) {
            $("#unit_span").html('地址不能为空').css('color', 'red')
        } else if (nature === "0") {
            $("#unit_span").html('单位性质不能为空').css('color', 'red')
        } else if (desc.length === 0) {
            $("#unit_span").html('单位简介不能为空').css('color', 'red')
        } else if (department.length === 0) {
            $("#unit_span").html('部门不能为空').css('color', 'red')
        } else if (superdepartment.length === 0) {
            $("#unit_span").html('上级主管部门不能为空').css('color', 'red')
        } else if (coderes === 'false') {
            $("#unit_span").html('邮政编码非法').css('color', 'red')
        } else {
            form = form + "&uuid=" + EDIT_UID;
            $.ajax({
                url: '/djcp/conformeditunit/' + '?uuid=' + EDIT_UID,
                type: 'POST',
                dataType: 'JSON',
                data: form,
                success: function (data) {
                    if (data.error) {
                        $('span.error').html('')


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
    $("#closeunit_btn").click(function () {
        $('#unitModel').modal('hide');
    })
}

function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".unit_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("unit_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/djcp/conformdelunit/' + "?id=" + DELETE_UID,
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
        setHiddenCol(document.getElementById('Table1'), 7)
    }

}

$(function () {
    var newtitle = '';
    $('p.cdes').mouseover(function (e) {
        newtitle = this.title;
        this.title = '';
        if (newtitle != '') {
            $('body').append('<div id="mytitle" >' + newtitle + '</div>');
        }
        $('#mytitle').css({
            'left': (e.pageX + 'px'),
            'top': (e.pageY + 'px')
        }).show();
    }).mouseout(function () {
        this.title = newtitle;
        $('#mytitle').remove();
    }).mousemove(function (e) {
        $('#mytitle').css({
            'left': (e.pageX + 10 + 'px'),
            'top': (e.pageY + 10 + 'px')
        }).show();
    })
});