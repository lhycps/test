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
$(function () {
    var newtitle = '';
    $('a.cdes').mouseover(function (e) {
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