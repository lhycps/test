//判断用户是否在5分钟内未操作页面，如果没有操作，则跳转到登录页
var lastTime = new Date().getTime();
var currentTime = new Date().getTime();
var timeOut = 30 * 60 * 1000; //设置超时时间： 3秒

$(function () {
    /* 鼠标移动事件 */
    $(document).mouseover(function () {
        lastTime = new Date().getTime(); //更新操作时间
    });
});
/* 定时器 间隔1秒检测是否长时间未操作页面 */
var timer = window.setInterval(testTime, 1000);

function testTime() {
    currentTime = new Date().getTime(); //更新当前时间
    if (location.href.substring(location.href.length - 10) == "/user/signin/") { //登录页
        clearInterval(timer); //关闭定时器
        console.log("当前所在页为登录页，不需要跳转");
    } else {
        if (currentTime - lastTime > timeOut) { //判断是否超时---超时
            clearInterval(timer);
            var src = window.top.location.href.substring(0, location.href.length - 10); //【注1】
//跳转到outline,提示用户跳转，可在后台进行销毁session;
            location.href = "/user/signin/"; //没有这个页面的可以直接跳转到登录页【注2】
        }
    }
}