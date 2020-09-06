// 全局常量
HOST = 'http://0.0.0.0:2828'

// Post发送方法封装
function psend(url, data, callback, is_async = true) {
    console.log("++++")
    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        async: is_async,
        success: function (data) {
            callback(data)
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            alert("Post ajax时出错了");
        }
    });
}