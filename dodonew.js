Java.perform(function () {

    // 获取并拦截类 "com.dodonew.online.http.RequestUtil"
    let RequestUtil = Java.use("com.dodonew.online.http.RequestUtil");

    // Hook RequestUtil 类中的 "paraMap" 方法，该方法有三个参数：'java.util.Map'，'java.lang.String' 和 'java.lang.String'
    RequestUtil["paraMap"].overload('java.util.Map', 'java.lang.String', 'java.lang.String').implementation = function (addMap, append, sign) {

        // 打印 paraMap 方法调用时的输入参数
        console.log(`RequestUtil.paraMap is called: addMap=${addMap}, append=${append}, sign=${sign}`);

        // 调用原始的 paraMap 方法并保存返回结果
        let result = this["paraMap"](addMap, append, sign);

        // 打印原始方法返回的结果
        console.log(`RequestUtil.paraMap result=${result}`);
        console.log("data" + result);

        // 将结果转换为字符串形式
        let data = result.toString();

        // 将请求体数据发送给 Frida 客户端，以便进一步分析
        let sendData = {"TAG": "Request", "RequestBody": data}
        send(sendData);

        // 定义一个空对象，用于存储修改后的请求体
        let reqModify = {}

        // 接收来自 Frida 客户端的修改请求体并等待该操作完成
        recv(function (reqObj) {
            reqModify.reqModfyStr = reqObj.modify_requestBody; // 获取修改后的请求体
        }).wait();

        // 返回修改后的请求体
        return reqModify.reqModfyStr;
    };

    // Hook RequestUtil 类中的 "decodeDesJson" 方法，拦截该方法的输入和输出
    RequestUtil["decodeDesJson"].implementation = function (json, desKey, desIV) {

        // 打印 decodeDesJson 方法调用时的输入参数
        console.log(`RequestUtil.decodeDesJson is called: json=${json}, desKey=${desKey}, desIV=${desIV}`);

        // 调用原始的 decodeDesJson 方法并保存返回结果
        let result = this["decodeDesJson"](json, desKey, desIV);

        // 打印原始方法返回的结果
        console.log(`RequestUtil.decodeDesJson result=${result}`);

        // 将解密后的响应体数据发送给 Frida 客户端
        let data = result;
        let sendData = {"TAG": "Response", 'ResponseBody': data};
        send(sendData);

        // 定义一个空对象，用于存储修改后的响应体
        let respModify = {}

        // 接收来自 Frida 客户端的修改响应体并等待该操作完成
        recv(function (respObj) {
            respModify.respModfyStr = respObj.modify_responseBody; // 获取修改后的响应体
        }).wait();

        // 返回修改后的响应体
        return respModify.respModfyStr;
    };

    // let Utils = Java.use("com.dodonew.online.util.Utils");
    // Utils["md5"].implementation = function (string) {
    //     console.log(`Utils.md5 is called: string=${string}`);
    //     let data = string;
    //     let sendData =
    //     let result = this["md5"](string);
    //     console.log(`Utils.md5 result=${result}`);
    //     return result;
    // };


});
