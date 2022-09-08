$(function () {
    console.log(3333)
    DELETE_UID = undefined;
    EDIT_UID = undefined;
    bindBtnAddEvent();
    bindBtnDeleteEvent();
    bindBtnEditEvent();
    bindaddoredit();
    bindConformDelete();
    del_input();
    is_bandpro();
    insertVal();
    click_reset()


})


function bindBtnAddEvent() {
    //点击新增奖金按钮弹出模态对话框
    $("#add_bonus").click(function () {
        $("#frm")[0].reset();
        $(".text-bold").text('新增奖金信息')
        var currentdate = getNowFormatDate();
        $("#completion_time").val(currentdate);
        $("#pdfspan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')

        $('#ModalThree').modal('show');
        EDIT_UID = undefined;
    });

}


function bindaddoredit() {
    //判断是走编辑还是走添加逻辑的函数
    $("#addbonus_btn").click(function () {
        if (EDIT_UID === undefined) {
            bindConformAdd()
        } else {
            bindConformEdit()
        }
    })
}

function timeoutclearspan() {
    //超时自动清空span的函数
    setTimeout(function () {
        $("#addbonus_span").html('')
    }, 1000)

}

function bindConformAdd() {
    //点击增加按钮增加奖金信息
    var formdata = new FormData()
    formdata.append('bonus_pdf', $("#bonus_pdf")[0].files[0])
    $('#frm').find('input, textarea, button,select').removeAttr("disabled");
    var frmVal = $('#frm').serialize();
    frmVal = decodeURIComponent(frmVal, true);
    formdata.append('inputdata', frmVal)
    var unit = $("#unit").val();
    var system = $("#system").val();
    if (unit.length === 0) {
        $("#addbonus_span").html('单位名称不能为空').css('color', 'red');
        timeoutclearspan();
    } else if (system.length === 0) {
        $("#addbonus_span").html('系统名称不能为空').css('color', 'red')
        timeoutclearspan();
    } else {
        $.ajax({
            url: '/djcp/bonus_add/',
            type: 'POST',
            data: formdata,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.msg)
                    location.replace('/djcp/bonus/')
                }
                timeoutclearspan();

            }
        })

    }


}


function bindBtnEditEvent() {
    //点击编辑按钮编辑奖金信息
    $('.bonus_editid').click(function () {
        //点击编辑显示模态对话框
        var bonus_editid = $(this).attr("bonus_editid")
        EDIT_UID = bonus_editid;
        $.ajax({
            url: '/djcp/bonus_edit/',
            type: 'GET',
            dataType: 'JSON',
            data: {"bonus_editid": bonus_editid},
            success: function (data) {
                if (!data.error) {
                    console.log(data)
                    $('#bandprodiv').attr("hidden", true);//编辑按钮自动隐藏绑定入口
                    initinput()//初始化界面
                    $('#unit').val(data.msg[0].unit)
                    $('#bonus').val(data.msg[0].bonus)
                    $('#contract_pdf').val(data.msg[0].contract_pdf)
                    $('#nature').val(data.msg[0].nature)
                    $("#nature").attr('disabled', 'true');//编辑时候性质为只读状态
                    $('#pm').val(data.msg[0].pm)
                    $('#remarks').val(data.msg[0].remarks)
                    $('#sale').val(data.msg[0].sale)
                    $('#system').val(data.msg[0].bonussystem__system)
                    $('#level').val(data.msg[0].bonussystem__level)
                    $('#completion_time').val(data.msg[0].bonussystem__completion_time)

                    var contract_pdf = data.msg[0].contract_pdf
                    var index = contract_pdf.lastIndexOf("\/");    //获取-后边的字符串
                    obj = contract_pdf.substring(index + 1, contract_pdf.length);
                    if (obj) {
                        $("#pdfspan").html(obj + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                    } else {
                        $("#pdfspan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                    }
                    for (var i = 0; i < data.msg.length; i++) {
                        if (i > 0) {
                            addItem(i)
                        }
                        $('#system' + i).val(data.msg[i].bonussystem__system)
                        $('#level' + i).val(data.msg[i].bonussystem__level)
                        $('#completion_time' + i).val(data.msg[i].bonussystem__completion_time)
                        $("#add_input").attr("hidden", true);
                        $("#delsystem" + i).attr("hidden", true);
                    }
                    $(".text-bold").text('编辑奖金');
                    $('#ModalThree').modal('show');
                } else {
                    alert(data.error)
                }

            }
        })

    })

}


function bindConformEdit() {
    //点击确认编辑
    var formdata = new FormData()
    var filecontract = $("#bonus_pdf")[0].files[0]
    if (filecontract) {
        formdata.append('bonus_pdf', $("#bonus_pdf")[0].files[0])
    } else {
        var filename = $('#pdfspan')[0].innerText
        // newfilename = filename.replace(/[\r\n]/g, "")
        console.log("newfilename", filename)

        console.log(filename)
        formdata.append('bonus_name', filename)
    }

    $('#frm').find('input, textarea, button,select').removeAttr("disabled");
    var frmVal = $('#frm').serialize();
    frmVal = decodeURIComponent(frmVal, true);
    formdata.append('inputdata', frmVal)
    formdata.append('edit_uid', EDIT_UID)
    var unit = $("#unit").val();
    var system = $("#system").val();
    if (unit.length === 0) {
        $("#addbonus_span").html('单位名称不能为空').css('color', 'red');
        timeoutclearspan();
    } else if (system.length === 0) {
        $("#addbonus_span").html('系统名称不能为空').css('color', 'red')
        timeoutclearspan();
    } else {
        $.ajax({
            url: '/djcp/bonus_conformedit/' + "?edit_uid=" + EDIT_UID,
            type: 'POST',
            data: formdata,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.msg)
                    location.reload()
                }
                timeoutclearspan();

            }
        })

    }

}

function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".bonus_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("bonus_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/djcp/bonus_conformdel/',
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

function addItem(input_count) {
    s = `
     <div class="col-12" id='addtexts${input_count}'>
        <div class="row">
            <div class="col-5">
                <div class="input-style-1">
                    <label class="rflag">系统名称</label>
                    <input type="text" name="system${input_count}" id="system${input_count}">
                </div>
            </div>
            <div class="col-3">
                <div class="select-style-1">
                    <label>系统级别</label>
                    <div class="select-position">
                        <select class="light-bg" id="level${input_count}" name="level${input_count}">
                            <option value="1">S2A2G2</option>
                            <option value="2">S2A1G2</option>
                            <option value="3">S1A2G2</option>
                            <option value="4">S3A3G3</option>
                            <option value="5">S3A2G3</option>
                            <option value="6">S2A3G3</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="col-3">
                <div class="input-style-1">
                    <label>完成时间</label>
                    <input type="date" name="completion_time${input_count}" id="completion_time${input_count}">
                </div>
            </div>
            <div class="col-1">
                <div class="input-style-1">
                    <label>&nbsp;&nbsp;</label>
                    <p class="text-dark delete-btn ml-10 delclass deldiv" id="delsystem${input_count}"> 
                        <i class="lni lni-trash-can"></i>
                    </p>
                </div>
            </div>
        </div>
    </div>`
    $('#add_txt').append(s);     //指定生成的位置,如在'add_txt'处生成
}


window.onload = function add_input() {
    //点击按钮添加输入框
    var input_count = 0
    $('#add_input').click(function () {
        input_count++;
        addItem(input_count);
        var currentdate = getNowFormatDate();
        $("#completion_time" + input_count).val(currentdate);


    })

}

function del_input() {
    //点击删除按钮删除生成的input输入框
    $('#add_txt').on('click', '.deldiv', function () {
        $(this).parent().parent().parent().remove();
    })

}

function is_bandpro() {
    //选择等保测评弹出绑定项目输入框，点击安全测评隐藏绑定项目输入框
    $('#nature').on('change', function () {
            initinput();
            var natureVal = $(this).val();
            is_security(natureVal)

        }
    )
}

function is_security(natureVal) {
    //判断是否是安全测评的函数，如果是安全测评自动隐藏，不是则显示
    if (natureVal == '安全测评') {
        $('#bandprodiv').attr("hidden", true);
        $("#unit").val('')
        $("#pm").val('1')
        $("#add_txt").empty()
        $('#system').val('')
        $('#level').val('1')

    } else {
        $('#bandprodiv').attr("hidden", false);
    }
}

function insertVal() {
    //点击绑定项目输入框插入对应的数据到input框中
    $("#bonus_pro").on('change', function () {
        $("#unit").val('')
        $("#pm").val('1')
        $("#add_txt").empty()
        $('#system').val('')
        $('#level').val('0')
        $('#completion_time').val('')
        var bonus_proVal = $(this).val()

        if (bonus_proVal) {
            $.ajax({
                url: '/djcp/insertVal/',
                type: 'GET',
                data: {'bid': bonus_proVal},
                dataType: 'JSON',
                success: function (data) {
                    for (let i = 0; i < data.length; i++) {
                        if (i == 0) {
                            isreadonly("unit")
                            isreadonly("pm")
                            isreadonly("system")
                            isreadonly("completion_time")
                            $("#unit").val(data[i].djcp__customer__unit_name)
                            $("#pm").val(data[i].pm)
                            $("#pm").attr('disabled', 'true');
                            $("#pm").css('background-color', 'rgb(210, 210, 210)');

                            $('#system').val(data[i].sys_name)
                            $('#level').val(data[i].level)
                            $("#level").attr('disabled', 'true');
                            $("#level").css('background-color', 'rgb(210, 210, 210)');
                            $('#completion_time').val(data[i].djcp__prodate__agreen)
                            $(".lni-plus").attr("hidden", true);
                            $(".lni-trash-can").attr("hidden", true);
                        } else {
                            addItem(i)
                            $('#system' + i).val(data[i].sys_name)
                            $('#level' + i).val(data[i].level)
                            $('#completion_time' + i).val(data[i].djcp__prodate__agreen)
                            isreadonly("system" + i)
                            $("#level" + i).attr('disabled', 'true');
                            $("#level" + i).css('background-color', 'rgb(210, 210, 210)');
                            isreadonly("completion_time" + i)
                            $(".lni-plus").attr("hidden", true);
                            $(".lni-trash-can").attr("hidden", true);

                        }


                    }


                }
            })
        } else {
            $(".lni-plus").attr("hidden", false);
            $(".lni-trash-can").attr("hidden", false);
            initinput()

        }


    })


}


function isreadonly(eleid) {
//设置为只读的函数
    var obj = document.getElementById(eleid);

    obj.setAttribute("readonly", true);

    obj.style.backgroundColor = "#d2d2d2";

}

function initinput() {
    //初始化输入框信息
    $("#level").val('1')
    var currentdate = getNowFormatDate();
    $("#completion_time").val(currentdate);
    $("#level").attr('disabled', false);
    $("#level").css('background-color', '');
    $("#pm").attr('disabled', false);
    $("#pm").css('background-color', '');
    $("#unit").removeAttr('readonly');
    $("#unit").css('background-color', '');
    $("#pm").removeAttr('readonly');
    $("#pm").css('background-color', '');
    $("#system").removeAttr('readonly');
    $("#system").css('background-color', '');
    $("#completion_time").removeAttr('readonly');
    $("#completion_time").css('background-color', '');
    $("#add_txt").empty();
    $("#bonus_pro").val('');
    $(".lni-plus").attr("hidden", false);
    $(".lni-trash-can").attr("hidden", false);


}


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

    $("#reporter_id").val(currentdate)
    return currentdate;
}


$(function () {
    $('input[name="datefilter"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            applyLabel: '确定',
            cancelLabel: '取消',
            daysOfWeek: ['⽇', '⼀', '⼆', '三', '四', '五', '六'],
            monthNames: ['⼀⽉', '⼆⽉', '三⽉', '四⽉', '五⽉', '六⽉',
                '七⽉', '⼋⽉', '九⽉', '⼗⽉', '⼗⼀⽉', '⼗⼆⽉'],
            firstDay: 1
        }

    });
    $('input[name="datefilter"]').on('apply.daterangepicker', function (ev, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
    });
    $('input[name="datefilter"]').on('cancel.daterangepicker', function (ev, picker) {
        $(this).val('');
    });
});

function click_reset() {
    $("#chongzhi").click(function () {
        $("#nature1").val('')
        $("#pm1").val('')
        $("#sale1").val('')
        $("#bonus1").val('')
        $("#level1").val('')
        $("#datefilter").val('')
        $("#unit1").val('')
    })


}

