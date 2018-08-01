/**
 * Created by chen on 17-7-8.
 */
var choice_ids = []; //选择题id数组
var blank_ids = []; //填空题id数组
var short_ids = []; //简答题id数组

var check_ans = {}; //检查答案对象，判空
var check_choice = [];//检查选择题空答案
var check_blank = []; //检查填空题空答案
var check_short_ans = []; //检查简答题空答案

var choice_cnt = 0;
var blank_cnt = 0;
var short_ans_cnt = 0;
var time = 0;

var testJson = null;
$(document).ready(function () {
    getpage();
});

function getpage() {
    var winurl = window.location.href;
    var urlarr;
    urlarr = winurl.split('/');
    var id = urlarr[urlarr.length - 3];
    var count = urlarr[urlarr.length - 1];
     var url = '/examing/getpage-result/' + id +'/'+ count;
    $.get(url, function (data) {
        testJson = data;
        addTest(JSON.parse(data));
    });
}

function addTest(arr) {
    var answer = arr['answer'];
    var true_answer = arr['true_answer'];
    console.log(true_answer);
    arr = arr['page'];
    var str = '';
    var desc_text = '';
    desc_text = '选择题' + arr['choice'].length + '道，分值' + arr.choice_score +
        '。填空题' + arr['blank'].length + '道，分值' + arr.blank_score +
        '。简答题' + arr['short_answer'].length + '道，分值' + arr.short_answer_score +
        '。共' + (arr['choice'].length + arr['short_answer'].length + arr['short_answer'].length) +
        '题，总分' + (arr.choice_score + arr.blank_score + arr.short_answer_score) +
        '。考试时长' + arr.times + '分钟。';

    $('#testTitle').text(arr.name);
    $('.description').text(desc_text);

    if (arr['choice'].length !== 0) {
        str += '<div class="testTile">选择题：共' + arr.choice.length + '题，每题' + arr.choice_score  + '分，共' + (arr.choice_score * arr.choice.length) + '分。</div>';
        $.each(arr['choice'], function (indexs, contents) {
            choice_ids.push(contents.pid);
            choice_ids.join(",");
            str += '<div class="ques_ans_con"><div class="question">' + (indexs + 1) + '.' + contents.desc_main + '<div class="choice_answers"> <ul>';
            $.each(contents.desc_other, function (indexed, contented) {
                if (!!answer['choice']&& !!answer['choice'][contents.pid] && answer['choice'][contents.pid] === contented){
                    str += '<li><input type="radio" class="choice_ans" name="answer' + contents.pid + '" value="' + contented + '" checked="checked">&nbsp;&nbsp;' + contented + '</li>';
                }else{
                    str += '<li><input type="radio" class="choice_ans" name="answer' + contents.pid + '" value="' + contented + '" >&nbsp;&nbsp;' + contented + '</li>';
                }

            });
            str += '</ul>';
            if (!!answer['choice']&& !!answer['choice'][contents.pid]) {
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>你的答案：'+answer['choice'][contents.pid]+'</p>'
            }else{
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>你的答案：</p>'
            }
            if(!!true_answer&& !!true_answer[contents.pid]){
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>正确答案：'+true_answer[contents.pid]+'</p>'
            }else{
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>正确答案：</p>'
            }
            str += '</div></div></div>';
        });
    }

    if (arr['blank'].length !== 0) {
        str += '<div class="testTile">填空题：共' + arr.blank.length + '题，每题' + (arr.blank_score / (arr.blank.length)) + '分，共' + arr.blank_score + '分。</div>';
        $.each(arr['blank'], function (indexs, contents) {
            str += '<div class="ques_ans_con"><div class="question">' + (indexs + 1) + '.' + contents.desc_main + '<div class="blank_answers">';
            blank_ids.push(contents.pid);
            blank_ids.join(",");
            if(!!answer['blank'] && !!answer['blank'][contents.pid]) {
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>你的答案：'+answer['blank'][contents.pid]+'</p>'
            }else{
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>你的答案：</p>'
            }
            if(!!true_answer&& !!true_answer[contents.pid]){
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>正确答案：'+true_answer[contents.pid]+'</p>'
            }else{
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>正确答案：</p>'
            }
            str += '</div></div></div>';
        });
    }

    if (arr['short_answer'].length !== 0) {
        str += '<div class="testTile">简答题：共' + arr.short_answer.length + '题，每题' + (arr.short_answer_score / (arr.short_answer.length)) + '分，共' + arr.short_answer_score + '分。</div>';
        $.each(arr['short_answer'], function (indexs, contents) {
            str += '<div class="ques_ans_con"><div class="question">' + (indexs + 1) + '.' + contents.desc_main + '<div class="short_ans_answers">';
            short_ids.push(contents.pid);
            short_ids.join(",");
            if(!!answer['short_answer'] && !!answer['short_answer'][contents.pid]) {
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>你的答案：'+answer['short_answer'][contents.pid]+'</p>'
            }else{
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>你的答案：</p>'
            }
            if(!!true_answer&& !!true_answer[contents.pid]){
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>正确答案：'+true_answer[contents.pid]+'</p>'
            }else{
                str += '<p><i class="glyphicon glyphicon-ok-sign" style="color: rgb(18, 255, 22);"></i>正确答案：</p>'
            }
            str += '</div></div></div>';
        });
    }

    // });
    $(".text_list").append(str);
}


$("body").bind("contextmenu", function () {
    return false;
});

$("body").bind("selectstart", function () {
    return false;
});
