function messagess(content, type) {
    layer({
        content: content,
        type: type,
        buttons: {
            close: function (e) {
                e.fadeout()
                location.reload()
            }
        }

    })

}