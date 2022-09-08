function getCaption(obj) {
    var index = obj.lastIndexOf("\-");    //获取-后边的字符串
    obj = obj.substring(index + 1, obj.length);
//  console.log(obj);
    return obj;
}

var str = " 执法办案流程-立案审批";

getCaption(str);