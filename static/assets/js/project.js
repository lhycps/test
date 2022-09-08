$(function () {
    console.log(333)
    DOWNLOAD_UID = undefined;
    var EDIT_UID = undefined;
    INFO_UID = undefined;
    CASE_UID = undefined;
    bindBtnAddEvent();
    bindBtnDeleteEvent();
    bindConformDelete();
    bindBtnDownloadEvent();
    conformdownload();
    //信息调查表
    bindBtnInfoEditEvent()
    bindBtnInfoAddEvent();
    outPutInfo();
    //测评方案
    bindBtnAddEvent_Case();
    bindBtnCaseAddEvent();
    CreateCase();


})

function selectsystem(obj) {
    //点击单位信息自动插入系统信息选择框
    var unit_id = obj.value
    $.ajax({
            url: '/djcp/get_unit_id/',
            type: 'GET',
            dataType: "JSON",
            data: {"unit_id": unit_id},
            success: function (data) {
                $("#bind_sys_id").empty()
                $.each(data, function (i, syslist) {
                    var s = ` <option value="${syslist.id}">${syslist.sys_name}</option>`
                    $("#bind_sys_id").append(s)

                })

            }
        },
    )


}

function selectcontact(obj) {
    //点击单位信息自动插入联系人信息选择框
    var unit_id = obj.value
    $.ajax({
            url: '/djcp/get_contact_id/',
            type: 'GET',
            dataType: "JSON",
            data: {"unit_id": unit_id},
            success: function (data) {
                $("#contact_id").empty()
                $.each(data, function (i, contactlist) {
                    var s = ` <option value="${contactlist.id}">${contactlist.name}</option>`
                    $("#contact_id").append(s)

                })

            }
        },
    )


}

function selectgmanage(obj) {
    //点击单位信息自动插入负责人信息选择框
    var unit_id = obj.value
    $.ajax({
            url: '/djcp/get_gmanage_id/',
            type: 'GET',
            dataType: "JSON",
            data: {"unit_id": unit_id},
            success: function (data) {
                console.log(data)
                $("#gmanage_id").empty()
                $.each(data, function (i, gmanagelist) {
                    var s = ` <option value="${gmanagelist.id}">${gmanagelist.gmanager}</option>`
                    $("#gmanage_id").append(s)

                })

            }
        },
    )


}

function selectdate(obj) {
    //点击单位信息自动插入合同日期信息选择框
    var unit_id = obj.value
    $.ajax({
            url: '/djcp/get_date_id/',
            type: 'GET',
            dataType: "JSON",
            data: {"unit_id": unit_id},
            success: function (data) {
                console.log("data", data)
                $("#date_id").empty()
                $.each(data, function (i, datelist) {
                    var s = ` <option value="${datelist.id}">${datelist.contract}</option>`
                    $("#date_id").append(s)

                })

            }
        },
    )


}


function bindBtnAddEvent() {
    $("#add_pro").click(function () {
        $("#is_add").text('增加项目')
        $('#ModalThree').modal('show');
        EDIT_UID = undefined;
    });

}


//点击增加按钮增加系统信息
$("#conform").click(function () {
    var form = $("#addproject_form").serialize()
    var unitcontact = $("#bind_unitcontact").val();
    var sys = $("#bind_sys_id").val();
    var date = $("#date_id").val();
    var contact = $("#contact_id").val();
    var gmanage = $("#gmanage_id").val();
    if (unitcontact === null || unitcontact === "0") {
        $("#unitcontact_span").html('单位不能为空').css('color', 'red')
        setTimeout(function () {
            $("#unitcontact_span").html('')
        }, 1000)
    } else if (sys === null || sys === "0") {
        $("#sys_span").html('系统名称不能为空').css('color', 'red')
        setTimeout(function () {
            $("#sys_span").html('')
        }, 1000)
    } else if (date === null || date === "0") {
        $("#date_span").html('合同日期不能为空').css('color', 'red')
        setTimeout(function () {
            $("#date_span").html('')
        }, 1000)
    } else if (contact === null || contact === "0") {
        $("#contact_span").html('联系人不能为空').css('color', 'red')
        setTimeout(function () {
            $("#contact_span").html('')
        }, 1000)
    } else if (gmanage === null || gmanage === "0") {
        $("#gmanage_span").html('负责人不能为空').css('color', 'red')
        setTimeout(function () {
            $("#gmanage_span").html('')
        }, 1000)
    } else {
        $.ajax({
            url: '/djcp/addproject/',
            type: 'POST',
            data: form,
            dataType: 'JSON',
            success: function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    location.reload()
                }
                setTimeout(function () {
                    $("#addrole_span").html('')
                }, 1000)

            }
        })

    }

})


function bindBtnDeleteEvent() {
    //弹出删除模态框的事件
    $(".btn_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("delete_uid");
        DELETE_UID = delete_uid;

    });
}

function bindConformDelete() {
    //绑定确定删除事件的函数
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/djcp/conformdelproject/' + "?id=" + DELETE_UID,
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


function bindBtnDownloadEvent() {
    //点击下载excel按钮弹出下载对话框
    //弹出删除模态框的事件
    $(".download_excel").click(function () {
        $('#ModalOne').modal('show');
        var dow_uid = $(this).attr("dow_uid");
        DOWNLOAD_UID = dow_uid;

    });
}

function conformdownload() {
    //绑定确定下载的事件excel
    $("#conforn_down").click(function () {
        $.ajax({
            url: '/djcp/conformdownload/',
            type: 'GET',
            data: {'dow_uid': DOWNLOAD_UID},
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

//---------信息调查表--------


function bindBtnInfoEditEvent() {
    //点击编辑按钮编辑信息调查表内容
    $('.btn_info').click(function () {
        //点击编辑显示模态对话框
        $('#ModalFour').modal('show');
        initINFO()
        var info_uid = $(this).attr("info_uid")
        INFO_UID = info_uid;
        $.ajax({
            url: '/djcp/Information_edit/',
            type: 'GET',
            dataType: 'JSON',
            data: {"info_uid": info_uid},
            success: function (data) {

                if (!data.error) {
                    if (data.zc_excel) {
                        $("#zichanspan").html(`<span style="white-space: nowrap;text-overflow: ellipsis;width: 650px;display: block;overflow: hidden;">${data.zc_excel.slice(10)}</span>` + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                    } else {
                        $("#zichanspan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                    }
                    if (data.tpt) {
                        $("#tptspan").html(`<span style="white-space: nowrap;text-overflow: ellipsis;width: 250px;display: block;overflow: hidden;" >${data.tpt.slice(4)}</span>` + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                        // $("#tptimage").className('custom-file-container__image-preview--active')
                        // let temp = document.getElementById('tptimage')
                        // temp.className('custom-file-container__image-preview--active')
                        // temp.classList.add('custom-file-container__image-preview--active')
                        // temp.classList.

                        $('#tptimage')[0].classList.add('custom-file-container__image-preview--active')
                        $("#tptimage").css('background-image', `url(/media/${data.tpt})`)
                    } else {
                        $("#tptspan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                    }
                    $('#tpt_desc').val(data.tpt_desc)

                    $("#infotitle").html(data.djcp__customer__unit_name + data.djcp__proInfo__sys_name)


                } else {
                    alert(data.error)
                }

            }
        })

    })

}

function initINFO() {
    //初始化信息
    $("#tptspan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
    $("#zichanspan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
    $('#tpt_desc').val('')
    $("#infotitle").html('')
}

function timeoutclearspan() {
    //超时自动清空span的函数
    setTimeout(function () {
        $("#tips").html('')
    }, 1000)

}

function bindBtnInfoAddEvent() {
    //添加信息调查表页面
    $('#infosheet').click(function () {
        var formdata = new FormData()
        formdata.append('info_uid', INFO_UID)
        var zichan = $("#zichan")[0].files[0]
        var tpt = $("#tpt")[0].files[0]
        formdata.append('zichan', zichan)
        formdata.append('tpt', tpt)
        var tpt_desc = $("#tpt_desc").val();
        formdata.append('tpt_desc', tpt_desc)
        var zc = $('#zichanspan')[0].outerText
        var tptspan = $('#tptspan')[0].outerText
        if (tpt_desc.length === 0) {
            $("#tips").html('拓扑图描述不能为空').css('color', 'red');
            timeoutclearspan();
        } else if (zc == 'Choose file...\n' + 'Browse') {
            $("#tips").html('未上传资产表').css('color', 'red');
            timeoutclearspan();
        } else if (tptspan == 'Choose file...\n' + 'Browse') {
            $("#tips").html('未上传网络拓扑图').css('color', 'red');
            timeoutclearspan();
        } else {
            $.ajax({
                url: '/djcp/Information_add/',
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


                }
            })

        }

    })


}

//生成信息调查表
function outPutInfo() {
    $('.outPutInfo').click(function () {
        var parentNode = $(this).parent();
        var dow_uid_info = $(this).attr("dow_uid_info")
        $(".dis_uid" + dow_uid_info).css('display', 'block')
        parentNode.css("display", "none")
        $.ajax({
            url: '/djcp/Information_download/',
            type: 'GET',
            data: {"dow_uid_info": dow_uid_info},
            success: function (data) {
                parentNode.css("display", "block")
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.msg)
                    $(".dis_uid" + dow_uid_info).css('display', 'none')
                    location.reload()
                }


            }
        })


    })


}

//测评方案相关
//点击上传测评方案按钮弹出方案的模态框
function bindBtnAddEvent_Case() {
    $(".case").click(function () {
        console.log('ehuehuhuhuh');
        $('#ModalFive').modal('show');
        var case_uid = $(this).attr("case_uid")
        CASE_UID = case_uid;
        $("#casespan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
        $.ajax({
            url: '/djcp/insert_case/',
            type: 'GET',
            dataType: 'JSON',
            data: {"case_uid": case_uid},
            success: function (data) {

                if (data.caseUpload) {
                    $("#casespan").html(`<span style="white-space: nowrap;text-overflow: ellipsis;width: 650px;display: block;overflow: hidden;">${data.caseUpload.slice(11)}</span>` + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                } else {
                    $("#casespan").html('Choose file...' + '<span class="custom-file-container__custom-file__custom-file-control__button"> Browse </span>')
                }
                $("#CaseTitle").html(data.case__customer__unit_name + data.case__proInfo__sys_name)
            }
        })

    })
}

function bindBtnCaseAddEvent() {
    //用户上传测评方案
    $('#addcase').click(function () {
        var formdata = new FormData()
        formdata.append('case_uid', CASE_UID)
        var caseUploadspan = $("#caseid")[0].files[0]
        formdata.append('caseUploadspan', caseUploadspan)
        var cases = $('#casespan')[0].outerText
        if (cases == 'Choose file...\n' + 'Browse') {
            $("#caseIdSpan").html('未上传测评方案').css('color', 'red');
            timeoutclearspan();
        } else {
            $.ajax({
                url: '/djcp/upload_case/',
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
                }
            })

        }

    })


}


//生成测评方案
function CreateCase() {
    $('.outPutCase').click(function () {
        var parentNode = $(this).parent();
        var create_uid_case = $(this).attr("create_uid_case")
        console.log(create_uid_case)
        $(".dis_uid_case" + create_uid_case).css('display', 'block')
        parentNode.css("display", "none")
        $.ajax({
            url: '/djcp/create_case/',
            type: 'GET',
            data: {"create_uid_case": create_uid_case},
            success: function (data) {
                parentNode.css("display", "block")
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.msg)
                    $(".dis_uid_case" + create_uid_case).css('display', 'none')
                    location.reload()
                }


            }
        })


    })


}