//头像预览
$("#avatar").change(function () {
    var fileobj = $(this)[0].files[0];
    var reader = new FileReader();
    reader.readAsDataURL(fileobj);
    reader.onload = function () {
        $("#avatar_img").attr("src", reader.result)

    };

});



function bindConformEdit() {
    //点击确认编辑
    var title = $("#title_id").val();
    var url = $("#url_id").val();
    if (title.length === 0) {
        $("#addpermission_span").html('标题不能为空').css('color', 'red')
        setTimeout(function () {
            $("#addpermission_span").html('')
        }, 1000)
    } else if (url.length === 0) {
        $("#addpermission_span").html('权限url不能为空').css('color', 'red')
        setTimeout(function () {
            $("#addpermission_span").html('')
        }, 1000)
    } else {
        $.ajax({
            url: '/user/conformeditpermission/',
            type: 'POST',
            dataType: 'JSON',
            data: {
                'permission_edit': EDIT_UID,
                "title": title,
                "url": url,
            },
            success: function (data) {
                if (data.msg) {
                    location.reload()
                } else {
                    alert(data.error)
                }
            }
        })
    }

}
