
$(document).ready(function(){
    $.ajax({
        type:"get",
        dataType:"text",
        url:"/api/get/first/level",
        success:function(data){
            // 由JSON字符串转换为JSON对象
            var objJSON=eval("("+data+")");
            var len=objJSON.itemInfo.length;

            var objSelect=document.getElementById("book");
            for(var i=0;i<len;i++){
                var op=new Option(objJSON.itemInfo[i].itemname,objJSON.itemInfo[i].itemvalue);
                objSelect.add(op);
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           alert(errorThrown);
        }
    });
});

//显示二级分类
function firstlevel_Click(){
    var objfirst=document.getElementById("book");
    var index=objfirst.selectedIndex; //选中索引
    var itemvalue=objfirst.options[index].value; //选中值

    // 删除二级分类保留第一个
    var objsecond=document.getElementById("unit");
    for(var i=objsecond.options.length-1;i>0;i--){
        objsecond.options.remove(i);
    }

    // 删除三级分类保留第一个
    var objthird=document.getElementById("section");
    for(var i=objthird.options.length-1;i>0;i--){
        objthird.options.remove(i);
    }

    $.ajax({
        type:"get",
        dataType:"text",
        url:"/api/get/second/level/by/"+itemvalue,
        success:function(data){
            // 由JSON字符串转换为JSON对象
            var objJSON=eval("("+data+")");
            var len=objJSON.itemInfo.length;
            var objSelect=document.getElementById("unit");
            for(var i=0;i<len;i++){
                var op=new Option(objJSON.itemInfo[i].itemname,objJSON.itemInfo[i].itemvalue);
                objSelect.add(op);
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           alert(errorThrown);
        }
    });
}

//显示三级分类
function secondlevel_Click(){
    var objsecond=document.getElementById("unit");
    var index=objsecond.selectedIndex; //选中索引
    var itemvalue=objsecond.options[index].value; //选中值

    // 删除三级分类保留第一个
    var objthird=document.getElementById("section");
    for(var i=objthird.options.length-1;i>0;i--){
        objthird.options.remove(i);
    }

    $.ajax({
        type:"get",
        dataType:"text",
        url:"/api/get/third/level/by/"+itemvalue,
        success:function(data){
            // 由JSON字符串转换为JSON对象
            var objJSON=eval("("+data+")");
            var len=objJSON.itemInfo.length;
            var objSelect=document.getElementById("section");
            for(var i=0;i<len;i++){
              var op=new Option(objJSON.itemInfo[i].itemname,objJSON.itemInfo[i].itemvalue);
              objSelect.add(op);
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           alert(errorThrown);
        }
    });
}