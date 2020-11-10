/*
 * @作者: weimo
 * @创建日期: 2020-11-10 20:44:40
 * @上次编辑时间: 2020-11-10 20:44:42
 * @一个人的命运啊,当然要靠自我奋斗,但是...
 */
function printfields(obj, fields){
    for (var field in fields){
        var key = fields[field];
        var value = obj[key + "_"].value;
        console.log(String(key).padEnd(15, " ") + ":" + value)
    }
}