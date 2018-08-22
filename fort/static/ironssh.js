function IronSSSHClient() {
    
}

//生成 websocket的 url
IronSSSHClient.prototype._generateURL = function (options) {
    if (window.location.protocol == 'https:'){
        //如果域名的请求协议是https websocket也用加密的
        var protocol = 'wss://';
    }else {
        var protocol = 'ws://';
    }
    //  ws://127.0.0.1:8000/host/就是item.id 获取的机器在表里的 id/
    var url = protocol + window.location.host + '/host/' + encodeURIComponent(options.des_id) + '/';
    return url;
};


//连接方法
IronSSSHClient.prototype.connect = function (options) {
    //调用上方的_generateURL url方法
    var des_url = this._generateURL(options);
    //判断浏览器是否支持websocket 生成一个websocket对象
    if (window.WebSocket) {
        this._connection = new WebSocket(des_url);
    }else if (window.MozWebSocket) {
        //火狐比较特殊
        this._connection = new MozWebSocket(des_url);
    }else {
        options.onError('小白您好，您当前浏览器不支持websocket');
        return;
    }
    //开启链接的时候
    this._connection.onopen = function () {
        options.onConnect();
    };
    //有消息过来的时候
    this._connection.message = function (evt) {
        var data = JSON.parse(evt.data.toString());
        // 如果传过来的数据里定义了error，说明有错误
        if (data.error !== undefined ) {
            options.onError(data.error);
        }else {
            options.onData(data.data)
        }
    };

    this._connection.onclose = function (evt) {
        options.onClose();
    };
};


//发送方法
IronSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify({'data':data}));

};