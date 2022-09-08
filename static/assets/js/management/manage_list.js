$(function () {
    DELETE_UID = undefined;
    EDIT_UID = undefined;
    bindBtnAddEvent();
    bindBtnDeleteEvent();
    bindBtnEditEvent();
    bindaddoredit();
    bindConformDelete();
    loadProvince();



})


function loadProvince() {
    loadArea('province', 0, loadCity);
}

function loadCity() {
    loadArea('city', $('#province').val(), loadTown);
}

function loadTown() {
    loadArea('town', $('#city').val());
}

function loadArea(selectId, pid, nextLoad) {
    $('#' + selectId).empty();
    $.get('/sale/loadArea/', {'pid': pid}, function (result) {


        //将json格式字符串转换成json对象数组
        var areaList = JSON.parse(result.jareaList);

        //遍历数组
        for (var i = 0; i < areaList.length; i++) {
            //获取每一个area的json对象
            var area = areaList[i];

            $('#' + selectId).append("<option value='" + area.pk + "'>" + area.fields.areaname + "</option>");
        }

        //判断是否需要加载下一级菜单
        if (nextLoad != null) {
            nextLoad();
        }

    });


}


function fillContent(textareaObj) {
    //获取三级联动菜单选中内容
    var pro = $('#province option:selected').text();
    var city = $('#city option:selected').text();
    var town = $('#town option:selected').text();

    //将菜单地址存放至文本域中
    var addr = pro + ' ' + city + ' ' + town;
    $(textareaObj).val(addr);
}


function ischeck() {
    //判断邮编格式是都正确
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


function lxfs() {
    //电话号码的前端验证
    var phone = document.getElementById("phone").value;
    if (phone != '') {
        var patrn = /^1[3456789]\d{9}$/;
        flag = patrn.test(phone);
        if (!flag) {
            return false;
        } else {
            return true;
        }

    } else {
        return false;

    }
}


function luhnCheck(bankno) {
    //前端银行卡号的校验
    if (bankno != '') {
        var lastNum = bankno.substr(bankno.length - 1, 1); //取出最后一位（与luhn进行比较）
        var first15Num = bankno.substr(0, bankno.length - 1); //前15或18位
        var newArr = new Array();
        for (var i = first15Num.length - 1; i > -1; i--) { //前15或18位倒序存进数组
            newArr.push(first15Num.substr(i, 1));
        }
        var arrJiShu = new Array(); //奇数位*2的积 <9
        var arrJiShu2 = new Array(); //奇数位*2的积 >9
        var arrOuShu = new Array(); //偶数位数组
        for (var j = 0; j < newArr.length; j++) {
            if ((j + 1) % 2 == 1) { //奇数位
                if (parseInt(newArr[j]) * 2 < 9) arrJiShu.push(parseInt(newArr[j]) * 2);
                else arrJiShu2.push(parseInt(newArr[j]) * 2);
            } else //偶数位
                arrOuShu.push(newArr[j]);
        }
        var jishu_child1 = new Array(); //奇数位*2 >9 的分割之后的数组个位数
        var jishu_child2 = new Array(); //奇数位*2 >9 的分割之后的数组十位数
        for (var h = 0; h < arrJiShu2.length; h++) {
            jishu_child1.push(parseInt(arrJiShu2[h]) % 10);
            jishu_child2.push(parseInt(arrJiShu2[h]) / 10);
        }
        var sumJiShu = 0; //奇数位*2 < 9 的数组之和
        var sumOuShu = 0; //偶数位数组之和
        var sumJiShuChild1 = 0; //奇数位*2 >9 的分割之后的数组个位数之和
        var sumJiShuChild2 = 0; //奇数位*2 >9 的分割之后的数组十位数之和
        var sumTotal = 0;
        for (var m = 0; m < arrJiShu.length; m++) {
            sumJiShu = sumJiShu + parseInt(arrJiShu[m]);
        }
        for (var n = 0; n < arrOuShu.length; n++) {
            sumOuShu = sumOuShu + parseInt(arrOuShu[n]);
        }
        for (var p = 0; p < jishu_child1.length; p++) {
            sumJiShuChild1 = sumJiShuChild1 + parseInt(jishu_child1[p]);
            sumJiShuChild2 = sumJiShuChild2 + parseInt(jishu_child2[p]);
        }
        //计算总和
        sumTotal = parseInt(sumJiShu) + parseInt(sumOuShu) + parseInt(sumJiShuChild1) + parseInt(sumJiShuChild2);
        //计算luhn值
        var k = parseInt(sumTotal) % 10 == 0 ? 10 : parseInt(sumTotal) % 10;
        var luhn = 10 - k;
        if (lastNum == luhn) {
            // $("#banknoInfo").html("luhn验证通过");
            return true;
        } else {
            // $("#banknoInfo").html("银行卡号必须符合luhn校验");
            return false;
        }

    } else {
        return false;
    }

}


function bindBtnAddEvent() {
    //点击新增合同按钮弹出模态对话框
    $("#add_contact").click(function () {
        $("#frm")[0].reset();
        $(".text-bold").text('新增合同信息')
        $('#ModalThree').modal('show');
        EDIT_UID = undefined;
    });

}


function bindaddoredit() {
    //判断是走编辑还是走添加逻辑的函数
    $("#addcontract_btn").click(function () {
        if (EDIT_UID === undefined) {
            console.log('进入增加界面')
            bindConformAdd()
        } else {
            console.log('进入编辑界面')
            bindConformEdit()

        }
    })
}

function timeoutclearspan() {
    //超时自动清空span的函数
    setTimeout(function () {
        $("#addcontract_span").html('')
    }, 1000)

}

function bindConformAdd() {
    //点击增加按钮增加合同信息

    var unit_name = $("#unit_name").val();
    var sys_name = $("#sys_name").val();
    var money = $("#money").val();
    var bank = $("#bank").val();
    var bankcardnum = $("#bankcardnum").val();
    var address = $("#address").val();
    var province1 = $("#province1").val();
    var city1 = $("#city1").val();

    if (unit_name.length === 0) {
        $("#addcontract_span").html('单位名称不能为空').css('color', 'red');
        timeoutclearspan();
    } else if (sys_name.length === 0) {
        $("#addcontract_span").html('系统名称不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (bank.length === 0) {
        $("#addcontract_span").html('开户行不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (address.length === 0) {
        $("#addcontract_span").html('地址不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (money.length === 0) {
        $("#addcontract_span").html('合同金额不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (province1.length === 0) {
        $("#addcontract_span").html('签订地点/省/不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (city1.length === 0) {
        $("#addcontract_span").html('签订地点/市/县不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (ischeck() === false) {
        $("#addcontract_span").html('邮编格式不正确').css('color', 'red')
        timeoutclearspan();
    } else if (lxfs() === false) {
        $("#addcontract_span").html('电话号码格式不正确').css('color', 'red')
        timeoutclearspan();
    } else if (luhnCheck(bankcardnum) === false) {
        $("#addcontract_span").html('银行卡格式错误').css('color', 'red')
        timeoutclearspan();
    } else {
        $.ajax({
            url: '/sale/contract_add/',
            type: 'POST',
            data: $('#frm').serialize(),
            dataType: 'JSON',
            success: function (data) {
                if (data.error) {
                    $("#addcontract_span").html(data.error).css('color', 'red')
                } else {
                    alert(data.msg)
                    location.reload()
                }
                timeoutclearspan();

            }
        })

    }
}


function bindBtnEditEvent() {
    //点击编辑按钮编辑合同信息
    $('.contract_editid').click(function () {
        //点击编辑显示模态对话框
        console.log(111)
        var contract_editid = $(this).attr("contract_editid")
        EDIT_UID = contract_editid;
        $.ajax({
            url: '/sale/contract_edit/',
            type: 'GET',
            dataType: 'JSON',
            data: {"contract_editid": contract_editid},
            success: function (data) {
                console.log("data", data)
                if (!data.error) {
                    $('#unit_name').val(data[0].unit_name)
                    $('#sys_name').val(data[0].sys_name)
                    $('#level').val(data[0].level)
                    $('#code').val(data[0].code)
                    $('#name').val(data[0].name)
                    $('#phone').val(data[0].phone)
                    $('#bank').val(data[0].bank)
                    $('#bankcardnum').val(data[0].bankcardnum)
                    $('#province1').val(data[0].province1)
                    $('#city1').val(data[0].city1)
                    $('#money').val(data[0].money)
                    $('#address').val(data[0].address)
                    $(".text-bold").text('编辑合同');
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
    var unit_name = $("#unit_name").val();
    var sys_name = $("#sys_name").val();
    var money = $("#money").val();
    var bank = $("#bank").val();
    var bankcardnum = $("#bankcardnum").val();
    var address = $("#address").val();
    var province1 = $("#province1").val();
    var city1 = $("#city1").val();

    if (unit_name.length === 0) {
        $("#addcontract_span").html('单位名称不能为空').css('color', 'red');
        timeoutclearspan();
    } else if (sys_name.length === 0) {
        $("#addcontract_span").html('系统名称不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (bank.length === 0) {
        $("#addcontract_span").html('开户行不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (address.length === 0) {
        $("#addcontract_span").html('地址不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (money.length === 0) {
        $("#addcontract_span").html('合同金额不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (province1.length === 0) {
        $("#addcontract_span").html('签订地点/省/不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (city1.length === 0) {
        $("#addcontract_span").html('签订地点/市/县不能为空').css('color', 'red')
        timeoutclearspan();
    } else if (ischeck() === false) {
        $("#addcontract_span").html('邮编格式不正确').css('color', 'red')
        timeoutclearspan();
    } else if (lxfs() === false) {
        $("#addcontract_span").html('电话号码格式不正确').css('color', 'red')
        timeoutclearspan();
    } else if (luhnCheck(bankcardnum) === false) {
        $("#addcontract_span").html('银行卡格式错误').css('color', 'red')
        timeoutclearspan();
    } else {
        $.ajax({
            url: '/sale/contract_conformedit/',
            type: 'POST',
            dataType: 'JSON',
            data: $('#frm').serialize() + '&uuid=' + EDIT_UID,
            success: function (data) {
                if (data.msg) {
                    alert(data.msg)
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
    $(".contract_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("contract_delete");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        console.log('/sale/contract_conformedel/' + "?id=" + DELETE_UID)
        $.ajax({
            url: '/sale/contract_conformedel/' + "?id=" + DELETE_UID,
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




