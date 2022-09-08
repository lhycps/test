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


$('#unitinfo_btn').click(function () {
        //单位信息判断
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
            $.ajax({
                url: '',
                type: 'POST',
                data: {
                    "unit_name": unit_name,
                    "address": address,
                    "nature": nature,
                    "code": code,
                    "department": department,
                    "superdepartment": superdepartment,
                    "desc": desc,
                    "csrfmiddlewaretoken": $('[name="csrfmiddlewaretoken"]').val()
                },
                dataType: 'JSON',
                success: function (data) {
                    if (data.msg) {
                        messagess(data.msg, 'success')
                        //清空对话框中的数据
                        $("#unitinfo_id")[0].reset();
                        $("#bind_unitinfo").empty()
                        $.ajax({
                            url: '/djcp/get_unitinfo/',
                            type: 'GET',
                            async: false,
                            data: {
                                "bind_unitinfo": $('#bind_unitinfo').val()
                            },
                            success: function (data) {
                                $.each(data, function (i, datalist) {
                                    var s = `<option id=${datalist.id} value=${datalist.id}>${datalist.unit_name}</option>`
                                    $("#bind_unitinfo").append(s)
                                })
                            }
                        })
                    } else {
                        messagess(data.error, 'danger')
                    }

                }
            })

        }
        setTimeout(function () {
            $("#unit_span").html('')

        }, 1000)


    }
)


$("#system_btn").click(function () {
    //系统信息判断
    $.ajax({
        url: '/djcp/sysinfo/',
        type: 'POST',
        dataType: 'JSON',
        data: $("#system_form").serialize(),
        success: function (data) {
            if (data.msg) {
                messagess(data.msg, 'success')
                $("#system_form")[0].reset();
            } else {
                $("#proadd_span").html(data.error).css('color', 'red')
                messagess(data.error, 'error')
            }
            setTimeout(function () {
                $("#proadd_span").html('')
            }, 1000)

        }
    })


})
