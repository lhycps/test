$(function () {
    EDIT_UID = undefined;
    DELETE_UID = undefined;
    bindBtnEditEvent();
    bindConformEdit();
    bindBtnDeleteEvent();
    bindConformDelete();
})

function conform() {
    var AddDayCount = $("#len").val()
    if (AddDayCount === '') {
        $("#task").val(GetDateStr(0));
        $("#question").val(GetDateStr(1));
        $("#scheme").val(GetDateStr(2));
        $("#schemereview").val(GetDateStr(3));

        $("#firstmeeting").val(GetDateStr(4));
        $("#onsiteevalaation").val(GetDateStr(5));
        $("#record").val(GetDateStr(6));
        $("#test").val(GetDateStr(7));
        $("#lasttmeeting").val(GetDateStr(8));

        $("#reporter").val(GetDateStr(9));
        $("#reporterview").val(GetDateStr(9));
        $("#acceptreporter").val(GetDateStr(13));
        $("#agreen").val(GetDateStr(14));

    } else {
        GetDateStr(AddDayCount);
        console.log('else', AddDayCount)
        // 默认时间为todays
        $("#task").val(GetDateStr(0));
        $("#question").val(GetDateStr(1 * AddDayCount));
        $("#scheme").val(GetDateStr(2 * AddDayCount));
        $("#schemereview").val(GetDateStr(3 * AddDayCount));

        $("#firstmeeting").val(GetDateStr(4 * AddDayCount));
        $("#onsiteevalaation").val(GetDateStr(5 * AddDayCount));
        $("#record").val(GetDateStr(6 * AddDayCount));
        $("#test").val(GetDateStr(7 * AddDayCount));
        $("#lasttmeeting").val(GetDateStr(8 * AddDayCount));

        $("#reporter").val(GetDateStr(9 * AddDayCount));
        $("#reporterview").val(GetDateStr(9 * AddDayCount));
        $("#acceptreporter").val(GetDateStr(10 * AddDayCount + 3));
        $("#agreen").val(GetDateStr(11 * AddDayCount + 3));


    }


    return AddDayCount
}

function GetDateStr(AddDayCount) {
    var _date = new Date();
    var currentWeek = _date.getDay();
    _date.setDate(_date.getDate() + AddDayCount); //获取AddDayCount天后的日期
    var years = _date.getFullYear();
    var months = (_date.getMonth() + 1) < 10 ? "0" + (_date.getMonth() + 1) : (_date.getMonth() + 1); //获取当前月份的日期，不足10补0
    var days = _date.getDate() < 10 ? "0" + _date.getDate() : _date.getDate(); //获取当前几号，不足10补0
    var dates = new Date(years, months - 1, days);
    var _week;
    if (dates.getDay() == 0) _week = "周日";
    if (dates.getDay() == 1) _week = "周一";
    if (dates.getDay() == 2) _week = "周二";
    if (dates.getDay() == 3) _week = "周三";
    if (dates.getDay() == 4) _week = "周四";
    if (dates.getDay() == 5) _week = "周五";
    if (dates.getDay() == 6) _week = "周六";
    return years + '-' + months + "-" + days;
}

function conform0() {
    var contractdate = $("#contract").val();
    var acceptinput = $("#len0").val();
    if (contractdate === '') {
        alert('合同日期未选择')
    } else if (acceptinput === '') {
        $("#apply").val(getNextDate(contractdate, -3));
        $("#accept").val(getNextDate(contractdate, -2));
        $("#formalization").val(getNextDate(contractdate, -1));
        $("#secret").val(getNextDate(contractdate, 1));
        $("#authorization").val(getNextDate(contractdate, 2));

    } else if (acceptinput) {
        $("#apply").val(getNextDate(contractdate, -3 * acceptinput));
        $("#accept").val(getNextDate(contractdate, -2 * acceptinput));
        $("#formalization").val(getNextDate(contractdate, -1 * acceptinput));
        $("#secret").val(getNextDate(contractdate, 1 * acceptinput));
        $("#authorization").val(getNextDate(contractdate, 2 * acceptinput));

    }

}

//获得合同时间的处理函数
function getNextDate(date, day) {
    var dd = new Date(date);
    dd.setDate(dd.getDate() + day);
    var y = dd.getFullYear();
    var m = dd.getMonth() + 1 < 10 ? "0" + (dd.getMonth() + 1) : dd.getMonth() + 1;
    var d = dd.getDate() < 10 ? "0" + dd.getDate() : dd.getDate();
    return y + "-" + m + "-" + d;
}

function bindBtnEditEvent() {
    //点击编辑按钮编辑时间信息
    $('.date_edit').click(function () {
        //点击编辑显示模态对话框
        var date_edit = $(this).attr("date_edit");
        EDIT_UID = date_edit;
        $.ajax({
            url: '/djcp/editdate/',
            type: 'GET',
            dataType: 'JSON',
            data: {"date_edit": date_edit},
            success: function (data) {
                console.log(data)
                if (!data.error) {

                    $('#ModalThree').modal('show');

                    $("#bind_unitcontact").val(data.date[0].unit_id);

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
        var form = $("#dateform_id").serialize();
        console.log(form)

        form = form + "&uuid=" + EDIT_UID;
        $.ajax({
            url: '/djcp/conformeditdate/' + '?uuid=' + EDIT_UID,
            type: 'POST',
            dataType: 'JSON',
            data: form,
            success: function (data) {
                console.log(data)
                if (data.error) {
                    $("#prodatespan").html(data.error).css('color', 'red')
                } else {
                    alert('更新成功')
                    location.reload()
                }
                setTimeout(function () {
                    $("#prodatespan").html('')

                }, 1000)

            }
        })


    })


}


function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".date_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("date_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/djcp/conformdeldate/' + "?id=" + DELETE_UID,
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
        setHiddenCol(document.getElementById('Table1'), 20)
    }

}

