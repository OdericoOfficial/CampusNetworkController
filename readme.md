app.get("/send")
随机发送10个TCP数据包

app.get("/sniff")
开始嗅探

app.get("/clear")
清空sketch

app.post("/sketch")
body:
{
    "src": "",
    "dst": "",
    "sport": "",
    "dport": ""
}
return:
{
    // 该次查询的键
    "Key": "",
    // 计数
    “Value”: int
}