/**
 * Created by Sun on 2017/3/29.
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
    submitAns();
    //saveAns();
    //getimes();
});

function getpage() {
    var winurl = window.location.href;
    var urlarr;
    urlarr = winurl.split('/');
    var id = urlarr[urlarr.length - 2];
    var count = urlarr[urlarr.length - 1];
    var url = '/examing/getpage/' + id +'/'+ count;
    //var url = '/examing/getpage/1'; //测试用
    $.get(url, function (data) {
        testJson = data;
        addTest(JSON.parse(data));
        addProgress();
    });
}

function timer() {
    $("#hint").hide();
    // var time = times;
    var timer = window.setInterval(function () {
        var hour = Math.floor(time / (60 * 60));
        var minute = Math.floor((time - hour * 3600) / 60);
        var seconds = Math.floor(time % 60);
        if (hour < 10) {
            hour = '0' + hour;
        }
        if (minute < 10) {
            minute = '0' + minute;
        }
        if (seconds < 10) {
            seconds = '0' + seconds;
        }
        var text = hour + ":" + minute + ":" + seconds;
        $("#timer").text(text);
        if (time === 0) {
            $("header").hide();
            $(".testCon").hide();
            $(".progress_save_con").hide();
            $(".top").hide();
            $(".timeWarn").hide();
            $("#hint").show();
            window.clearInterval(timer);
            var t = window.setTimeout(function () {
                autoSubmit();
            }, 1000);
        }
        --time;
    }, 1000);
}

function addTest(arr) {
    var answer = arr['answer'];
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
            str += '</ul></div></div></div>';
        });
    }

    if (arr['blank'].length !== 0) {
        str += '<div class="testTile">填空题：共' + arr.blank.length + '题，每题' + (arr.blank_score / (arr.blank.length)) + '分，共' + arr.blank_score + '分。</div>';
        $.each(arr['blank'], function (indexs, contents) {
            str += '<div class="ques_ans_con"><div class="question">' + (indexs + 1) + '.' + contents.desc_main + '<div class="blank_answers">';
            blank_ids.push(contents.pid);
            blank_ids.join(",");
            if(!!answer['blank'] && !!answer['blank'][contents.pid]) {
                str += '<div>请在下面文本框中按填空顺序填写答案：</div><div class="blank_ans_con"><textarea name="blank_ans' + contents.pid + '" class="blank_ans" cols="100" rows="20">'+answer['blank'][contents.pid]+'</textarea></div>';
            }else{
                str += '<div>请在下面文本框中按填空顺序填写答案：</div><div class="blank_ans_con"><textarea name="blank_ans' + contents.pid + '" class="blank_ans" cols="100" rows="20"></textarea></div>';
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
                str += '<div>请在下面文本框中填写简答题答案：</div><div class="short_ans_con"><textarea name="short_ans' + contents.pid + '" class="short_ans" cols="100" rows="20">'+answer['short_answer'][contents.pid]+'</textarea></div>';
            }else{
                str += '<div>请在下面文本框中填写简答题答案：</div><div class="short_ans_con"><textarea name="short_ans' + contents.pid + '" class="short_ans" cols="100" rows="20"></textarea></div>';
            }
            str += '</div></div></div>';
        });
    }

    // });
    $(".text_list").append(str);
    time = (arr.end_time - arr.now_time) ;
    timer();

}

function addProgress() {
    var c_str = '';
    var b_str = '';
    var s_str = '';
    /*choice */
    if (choice_ids.length !== 0) {
        c_str = '<div class="choice_progress_cnt">选择题：</div><div class="progress progress-striped active"><div class="progress-bar progress-bar-success choice-progress-bar" role="progressbar"aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 0"></div></div>';
        $('.choice_progress').html(c_str);

        var checkedObjNameArr = [];
        $(".choice_progress_cnt").text("选择题：" + (choice_cnt + "/" + choice_ids.length));
        $(".choice_ans").click(function () {
            if (this.checked) {
                var objName = $(this).attr("name");
                if ($.inArray(objName, checkedObjNameArr) === -1) {
                    choice_cnt++;
                    checkedObjNameArr.push(objName);
                }
            }
            $(".choice_progress_cnt").text("选择题：" + (choice_cnt + "/" + choice_ids.length));
            var wid = (choice_cnt / choice_ids.length) * 100 + '%';
            $('.choice-progress-bar').css('width', wid);
        });
    }
    /*end choice*/

    /*blank*/
    if (blank_ids.length !== 0) {
        b_str = '<div class="blank_progress_cnt">填空题：</div><div class="progress progress-striped active"><div class="progress-bar progress-bar-info blank-progress-bar" role="progressbar"aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 0;"></div></div>';
        $('.blank_progress').append(b_str);

        $(".blank_progress_cnt").text("填空题：" + (blank_cnt + "/" + blank_ids.length));

        var blankObjNameArr = [];
        $('.blank_ans').blur(function () {
            var objName = $(this).attr("name");
            var blank_ans = $(this).val();
            if ($.inArray(objName, blankObjNameArr) === -1) {
                if ($.trim(blank_ans) !== '') {
                    blankObjNameArr.push(objName);
                    if (blank_cnt < blank_ids.length) {
                        blank_cnt++;
                    }

                } else {
                    if ($.inArray(objName, blankObjNameArr) !== -1) {
                        blankObjNameArr.splice($.inArray(objName, blankObjNameArr), 1);
                        if (blank_cnt > 0) {
                            blank_cnt--;
                        }
                    }
                }
            } else {
                if ($.trim(blank_ans) == '') {
                    blankObjNameArr.splice($.inArray(objName, blankObjNameArr), 1);
                    if (blank_cnt > 0) {
                        blank_cnt--;
                    }
                }
            }

            $(".blank_progress_cnt").text("填空题：" + (blank_cnt + "/" + blank_ids.length));
            var wid = (blank_cnt / blank_ids.length) * 100 + '%';
            $('.blank-progress-bar').css('width', wid);
        });
    }
    /*end blank*/

    /*short_answer*/
    if (short_ids.length !== 0) {
        s_str = ' <div class="short_ans_progress_cnt">简答题：</div><div class="progress progress-striped active"><div class="progress-bar progress-bar-warning short-ans-progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 0;"> </div></div>';
        $('.short_ans_progress').append(s_str);

        $(".short_ans_progress_cnt").text("简答题：" + (short_ans_cnt + "/" + short_ids.length));

        var shortObjNameArr = [];
        $('.short_ans').blur(function () {
            var objName = $(this).attr("name");
            var short_ans = $(this).val();
            if ($.inArray(objName, shortObjNameArr) === -1) {
                if ($.trim(short_ans) !== '') {
                    shortObjNameArr.push(objName);
                    if (short_ans_cnt < short_ids.length) {
                        short_ans_cnt++;
                    }
                } else {
                    if ($.inArray(objName, shortObjNameArr) !== -1) {
                        shortObjNameArr.splice($.inArray(objName, shortObjNameArr), 1);
                        if (short_ans_cnt > 0) {
                            short_ans_cnt--;
                        }
                    }
                }
            } else {
                if ($.trim(short_ans) == '') {
                    shortObjNameArr.splice($.inArray(objName, shortObjNameArr), 1);
                    if (short_ans_cnt > 0) {
                        short_ans_cnt--;
                    }
                }
            }


            $(".short_ans_progress_cnt").text("简答题：" + (short_ans_cnt + "/" + short_ids.length));
            var wid = (short_ans_cnt / short_ids.length) * 100 + '%';
            $('.short-ans-progress-bar').css('width', wid);
        });

    }
    /*end short_answer*/

    var btn_save = '<input type="button" id="btn-save" class="btn btn-success" onclick="saveAns()" value="保存答案">';
    $('.progress_save_con').append(btn_save);

}

function submitAns() {
    $('#submit').click(function () {
        var ans = getAns();
        if (checkAns() === 1){
        time = 0;
        }
    })
}

function autoSubmit() {
    var ans = getAns();
    var winurl = window.location.href;
    var urlarr;
    urlarr = winurl.split('/');
    var id = urlarr[urlarr.length - 2];
    var count = urlarr[urlarr.length - 1];
    var url = '/examing/finish/' + id +'/'+ count;

    $.ajax({
        url:url,
        data:ans,
        type:'post',
        dataType:'json',
        headers:{
            Accept:"application/json",
            "Content-Type":"application/json"
        },
        success:function (data) {
            window.location.href = "/exam-list";
        }
    });
}

function saveAns() {
    var ans = getAns();
    var winurl = window.location.href;
    var urlarr;
    urlarr = winurl.split('/');
    var id = urlarr[urlarr.length - 2];
    var count = urlarr[urlarr.length - 1];
    var url = '/examing/save/' + id +'/'+ count;

    $.ajax({
        url:url,
        data:ans,
        type:'post',
        dataType:'json',
        headers:{
            Accept:"application/json",
            "Content-Type":"application/json"
        },
        success:function (data) {
            alert("保存成功!");
        }
    });
}

function getAns() {
    var answers = {};  //答案对象

    var choice_answers = {}; //选择题部分答案对象
    var choice_ans = []; //选择题答案数组

    var blank_answers = {};  //填空题部分答案对象
    var blank_ans = []; //填空题答案数组

    var short_answers = {}; //简答题部分答案
    var short_ans = []; //简答题答案数组

    //初始化
    check_ans = {}; //检查答案对象，判空
    check_choice = [];//检查选择题空答案
    check_blank = []; //检查填空题空答案
    check_short_ans = []; //检查简答题空答案

    /*选择题部分*/
    $(".choice_answers").each(function (i) {
        var ans_cnt = 0;
        $(this).find(".choice_ans").each(function (j) {
            if (this.checked) {
                var an = $(this).val();
                choice_ans.push(an);
                choice_ans.join(",");
            } else {
                ans_cnt++;
            }
        });
        if ($(this).find(".choice_ans").length === ans_cnt) {
            choice_ans.push('');
            choice_ans.join(",");

            check_choice.push(i + 1);
            check_choice.join(",");
        }
    });
    // answers = {ids: arrids, ans: ans};
    //构建 json串 以id为键 以答案为值
    $.each(choice_ids, function (index, content) {
        var key = content;  //id值为键
        var value = choice_ans[index]; //答案值为值
        choice_answers[key] = value;
    });
    answers.choice = choice_answers;
    /*end 选择题*/

    /*填空题部分*/
    $(".blank_answers").each(function (i) {
        $(this).find(".blank_ans").each(function (j) {
            var an = $.trim($(this).val());
            if (an !== '' && an !== null) {
                blank_ans.push(an);
                blank_ans.join(",");
            } else {
                an = '';
                blank_ans.push(an);
                blank_ans.join(",");

                check_blank.push(i + 1);
                check_blank.join(",");
            }
        });
    });
    // answers = {ids: arrids, ans: ans};
    //构建 json串 以id为键 以答案为值
    $.each(blank_ids, function (index, content) {
        var key = content;  //id值为键
        var value = blank_ans[index]; //答案值为值
        blank_answers[key] = value;
    });
    answers.blank = blank_answers;
    /*end 填空题*/

    /*简答题部分*/
    $(".short_ans_answers").each(function (i) {
        $(this).find(".short_ans").each(function (j) {
            var an = $.trim($(this).val());
            if (an !== '' && an !== null) {
                short_ans.push(an);
                short_ans.join(",");
            } else {
                an = '';
                short_ans.push(an);
                short_ans.join(",");

                check_short_ans.push(i + 1);
                check_short_ans.join(",");
            }
        });
    });
    // answers = {ids: arrids, ans: ans};
    //构建 json串 以id为键 以答案为值
    $.each(short_ids, function (index, content) {
        var key = content;  //id值为键
        var value = short_ans[index]; //答案值为值
        short_answers[key] = value;
    });
    answers.short_answer = short_answers;
    /*end 简答题*/


    check_ans.choice = check_choice;
    check_ans.blank = check_blank;
    check_ans.short_answer = check_short_ans;

    var ansJson = JSON.stringify(answers); //转json串
    return ansJson;
    // alert(ansJson);

}

function checkAns() {
    var promptStr = '';
    if (check_ans.choice.length !== 0) {
        promptStr += '选择题：';
        $.each(check_choice, function (index, content) {
            promptStr += '第' + content + '题' + ' ';
        });
        promptStr += '\n';
    }
    if (check_ans.blank.length !== 0) {
        promptStr += '填空题：';
        $.each(check_blank, function (index, content) {
            promptStr += '第' + content + '题' + ' ';
        });
        promptStr += '\n';
    }

    if (check_ans.short_answer.length !== 0) {
        promptStr += '简答题：';
        $.each(check_short_ans, function (index, content) {
            promptStr += '第' + content + '题' + ' ';
        });
    }

    if (promptStr.length !== 0) {
        promptStr += '\n\n确定提交吗？';
        promptStr = '你有以下题目没填写：\n' + promptStr;
        if (confirm(promptStr)) {
            return 1;
        } else {
            return 0;
        }
    } else {
        if (confirm('确定提交吗?')) {
            return 1;
        } else {
            return 0;
        }
    }

}

function getimes() {
    var winurl = window.location.href;
    var urlarr;
    urlarr = winurl.split('/');
    var id = urlarr[urlarr.length - 2];
    var count = urlarr[urlarr.length - 1]
    var url = '/examing/getpage/' + id +'/'+ count;
    //var url = '/examing/getpage/1'; //测试用  得到考试剩余时间
    window.setInterval(function () {
        $.get(url, function (data) {
            var data = JSON.parse(data);
            time = (data.end_time-data.now_time);
        });
    }, 1000 * 60);
}

$("body").bind("contextmenu", function () {
    return false;
});

$("body").bind("selectstart", function () {
    return false;
});
