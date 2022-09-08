function getNowFormatDate() {
    //获得当前时间插入到时间输入框中
    var date = new Date();
    var seperator1 = "-";
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = year + seperator1 + month + seperator1 + strDate;
    console.log(currentdate)
    $("#reporter_id").val(currentdate)
    return currentdate;
}

function addDays(days) {
    var d = new Date();
    var m = d.setMilliseconds(d.getMilliseconds() + (days * 24 * 60 * 60 * 1000))
    console.log(m)
}


//点击受理阶段按钮返回受理阶段时间
function conform0() {
    var contractdate = $("#contract").val();
    var acceptinput = $("#len0").val();
    if (contractdate === '') {
        messagess('合同日期未选择', 'danger')
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

// 点击准备阶段确认按钮返回前端时间
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

//获得合同时间的处理函数
function getNextDate(date, day) {
    var dd = new Date(date);
    dd.setDate(dd.getDate() + day);
    var y = dd.getFullYear();
    var m = dd.getMonth() + 1 < 10 ? "0" + (dd.getMonth() + 1) : dd.getMonth() + 1;
    var d = dd.getDate() < 10 ? "0" + dd.getDate() : dd.getDate();
    return y + "-" + m + "-" + d;
}


//点击添加按钮得事件
$(".dateadd").click(function () {
    $.ajax({
        url: '',
        type: 'POST',
        dataType: 'JSON',
        data: $("#contactform_id").serialize(),
        success: function (data) {
            if (data.error) {
                $("#prodatespan").html(data.error).css('color', 'red')
                layer({
                    content: content,
                    type: type,
                    buttons: {
                        close: function (e) {
                            e.fadeout()
                        }
                    }
                })
            } else {
                messagess('成功', 'success')
            }
            setTimeout(function () {
                $("#prodatespan").html('')

            }, 1000)

        }
    })


})









