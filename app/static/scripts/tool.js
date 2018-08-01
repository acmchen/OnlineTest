/**
 * Created by chen on 17-7-5.
 */

$(document).ready(function () {
    getToolValues();
})

function getToolValues() {
    var winurl = window.location.href;
    var urlarr;
    urlarr = winurl.split('/');

    var key = urlarr[urlarr.length-2];
    var value = urlarr[urlarr.length-1];
    console.log(key);
    value = decodeURIComponent(value);
    console.log(value);
    if (key == 'values') {
        var base = new Base64();
        var values = base.decode(value);
        setValuesToTool(values);
    }
}

function setValuesToTool(values) {
    var valueDict = JSON.parse(values);
    for (var key in valueDict){
        $("#"+key).val(valueDict[key]);
    }
}