   $(function () {
       //创建一个当前日期对象
       var now = new Date();
       //格式化日，如果小于9，前面补0
       var day = ("0" + now.getDate()).slice(-2);
       //格式化月，如果小于9，前面补0
       var month = ("0" + (now.getMonth() + 1)).slice(-2);
       //拼装完整日期格式
       var today = now.getFullYear() + "-" + (month) + "-" + (day);
       //完成赋值
       $("#lucky").val(today);
       $("#luckly").val(today);
   }

