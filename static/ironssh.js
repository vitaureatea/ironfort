
function  IronSSHClient() {

}

//生成 websocket的 url
IronSSHClient.prototype._generateURL = function (options) {
    if (window.location.protocol == 'https:'){
        var protocol = 'wss://';
    }else{
        var protocol = 'ws://';
    }
    // ws://192.168.1.108:8000/host/3/
    var url = protocol + window.location.host + '/host/' + encodeURIComponent(options.des_id) + '/';
    return url;
};

//连接方法
IronSSHClient.prototype.connect = function (options) {
    // ws://192.168.1.108:8000/host/3/
    var des_url = this._generateURL(options);

    if (window.WebSocket) {
        this._connection = new WebSocket(des_url);
    }
    else if (window.MozWebSocket) {
        this._connection = new MozWebSocket(des_url);
    }
    else {
        options.onError('当前浏览器不支持WebSocket！');
        return ;
    }

    this._connection.onopen = function () {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = JSON.parse(evt.data.toString());
        if (data.error !== undefined) {
            options.onError(data.error);
        }
        else {
            options.onData(data.data);
        }
    };

    this._connection.onclose = function (evt) {
        options.onClose();
    };
};


//发送方法
IronSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify({'data': data}));

};