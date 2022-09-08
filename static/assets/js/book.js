$(function () {
    var DELETE_UID = 0;
    var EDIT_UID = undefined;
    bindBtnAddEvent();
    closebtn();
    bindBookBtnSave();
    bindBtnDeleteEvent();
    bindBtnEditEvent();
    bindConformDelete();
    QueryData();


})

function QueryData() {
    $("#query_id").click(function () {

        $.ajax({
            url: '/lab/search/',
            type: 'get',
            data: $("#search_bookobj").serialize(),
            success: function (data) {
                console.log(data)

            }
        })

    })

}


function bindBtnAddEvent() {
    $("#add_book").click(function () {
        //清空对话框中的数据
        $("#addbook_form")[0].reset();
        EDIT_UID = undefined;
        $("#myModalLabel").text('增加图书')
        $('#myModal').modal('show');

    });

}


function bindBookBtnSave() {
    $("#addbook_btn").click(function () {
            if (EDIT_UID === undefined) {
                console.log('新建')
                conformadd()

            } else {
                conformedit()

            }
        }
    )


}

function conformadd() {
    var bookname = $("#addbookname_id").val();
    var author = $("#addauthor_id").val();
    var count = $("#addcount_id").val();
    var publish = $("#addpublish_id").val();
    var position = $("#addposition_id").val();
    if (bookname.length === 0) {
        $("#addbook_span").html('书名不能为空').css('color', 'red')
    } else if (author.length === 0) {
        $("#addbook_span").html('作者名不能为空').css('color', 'red')
    } else if (publish.length === 0) {
        $("#addbook_span").html('出版社不能为空').css('color', 'red')
    } else if (position === '0') {
        $("#addbook_span").html('未勾选所属位置').css('color', 'red')
    } else if (!(/(^[1-9]\d*$)/.test(count))) {
        $("#addbook_span").html('数量不是正整数').css('color', 'red')
    } else {
        $.ajax({
            url: '/lab/addbook/',
            type: 'post',
            data: $("#addbook_form").serialize(),
            dataType: "JSON",
            success: function (data) {
                if (data.error) {
                    console.log(data.error)
                } else {
                    alert(data.msg);
                    $("#addbook_form")[0].reset();
                }
                setTimeout(function () {
                    $("#addbook_span").html('')

                }, 1000)


            }

        })
    }


}

function closebtn() {
    $("#close_btn").click(function () {
        $('#myModal').modal('hide');
        location.reload()

    })


}
function conformedit() {
    var bookname = $("#addbookname_id").val();
    var author = $("#addauthor_id").val();
    var count = $("#addcount_id").val();
    var publish = $("#addpublish_id").val();
    var position = $("#addposition_id").val();
    if (bookname.length === 0) {
        $("#addbook_span").html('书名不能为空').css('color', 'red')
    } else if (author.length === 0) {
        $("#addbook_span").html('作者名不能为空').css('color', 'red')
    } else if (publish.length === 0) {
        $("#addbook_span").html('出版社不能为空').css('color', 'red')
    } else if (position === '0') {
        $("#addbook_span").html('未勾选所属位置').css('color', 'red')
    } else if (!(/(^[1-9]\d*$)/.test(count))) {
        $("#addbook_span").html('数量不是正整数').css('color', 'red')
    } else {
        $.ajax({
            url: "/lab/editconformbook/" + "?edit_uid=" + EDIT_UID,
            type: 'post',
            data: $("#addbook_form").serialize(),
            dataType: "JSON",
            success: function (data) {
                if (data.error) {

                    console.log(data.error)
                } else {
                    console.log(this.url)
                    location.reload()

                }
                setTimeout(function () {
                    $("#addbook_span").html('')

                }, 1000)


            }

        })
    }


}

function bindBtnDeleteEvent() {
    $(".btn_delete").click(function () {
        $('#delete_model').modal('show');
        var delete_uid = $(this).attr("delete_uid");
        DELETE_UID = delete_uid;
        console.log(DELETE_UID);
    });
}

function bindConformDelete() {
    $("#delete_uidbtn").click(function () {
        $.ajax({
            url: '/lab/deletebook/',
            type: 'GET',
            data: {'delete_uid': DELETE_UID},
            dataType: 'JSON',
            success: function (data) {
                if (data.status) {
                    location.reload()
                } else {
                    alert(data.error)
                }

            }
        })

    })


}

function bindBtnEditEvent() {
    $('.btn_edit').click(function () {
        //点击编辑显示模态对话框
        var edit_uid = $(this).attr('edit_uid');
        EDIT_UID = edit_uid;
        $.ajax({
            url: '/lab/editbook/',
            type: 'GET',
            dataType: 'JSON',
            data: {"edit_uid": edit_uid},
            success: function (data) {
                if (data.status) {
                    var edit_input = data.bookdict;
                    $("#addbookname_id").val(edit_input.bookname);
                    $("#addauthor_id").val(edit_input.author);
                    $("#addcount_id").val(edit_input.count);
                    $("#addpublish_id").val(edit_input.publish);
                    $("#addposition_id").val(edit_input.position);
                    $("#myModalLabel").text('编辑图书');
                    $('#myModal').modal('show');

                }


            }
        })

    })

}

