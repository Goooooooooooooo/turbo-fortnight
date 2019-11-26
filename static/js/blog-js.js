
$(document).ready(function() {
    $("#header-nav > nav > ul.main-nav > li").each(function(){
        var ele = $(">a",this);
        var attr = ele.attr('href');
        if(typeof attr !== typeof undefined && attr !== false){
            if(ele[0].href==String(window.location)){
                $(this).eq(0).addClass("current");
                //$("#blog-nav > div").eq(0).removeClass("active-bg")
            }
        }
    });
});

// 移除 ckeditor 元素，是 CKeditor 能够自适应大小
$(function(){
    $(".django-ckeditor-widget").removeAttr('style');
});

//detail.html article-delete
function confirm_safe_delete() {
    $('form#safe_delete button').click();
}

//detail.html 评论锚点定位
/*
var move = document.getElementById("move_comment");
if(move){
    move.addEventListener('click', function(){
        var target = document.getElementById('comment_display');
        target.scrollIntoView(false);
    })
}
*/
//detail.html 加载 iframe ckeditor
$("#replyModal").on('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = $(event.relatedTarget)
    // Extract info from data-* attributes
    var recipient = button.data('whatever')
    var res = recipient.split(",");
    var modal = $(this)
    modal.find('.modal-title').text('reply to ' + res[0])
    if(modal.find('.modal-body').children().length === 0){
        let content = '<iframe id="myiframe" src="/comment/post-comment/' +
            res[1] + '/' + res[2] + '" frameborder="0" style="width:100%;height:100%;" ></iframe>';
        modal.find('.modal-body').append(content);
    }
})


//comment/reply.html 清空 ckeditor 文本内容
function text_clear(){
    CKEDITOR.instances['id_body'].setData(' ');
}

//header.html search-form
function search_form_submit() {
    //获取form表单的dom对象
    var form = document.getElementById('search-form');
    //调用对象的submit方法
    form.submit();
}

// 画面小于 992px 时 菜单打开关闭控制
$("#btn").click(function(){
    /*if($("#nav-menu").css("display")=="none"){
        $("#nav-menu").css("display", "block");
    }else{
        $("#nav-menu").css("display", "none");
    }*/
    window.onresize = function(){
        var w = document.documentElement.clientWidth;
        if(w >= 992){
            $("#nav-menu").css("display", "block");
        }
    }
    $("#nav-menu").toggle("normal");
});
// 点击任意选项之后，隐藏菜单
//$("#nav-menu > ul > li > a").click(function(){
//    $("#nav-menu").toggle("normal");
//});

// 搜索栏 弹出控制
function openSearch() {
    document.getElementById("searchOverlay").style.display = "block";
}
function closeSearch() {
    document.getElementById("searchOverlay").style.display = "none";
}
$(function() {
    document.addEventListener('keyup', function(ev) {
        // escape key.
        if( ev.keyCode == 27 ) {
            closeSearch();
        }
    });
});

// 用户菜单弹出控制
function openNav() {
  document.getElementById("side-user-menu").style.width = "250px";
  document.getElementById("wrapper").style.marginRight = "250px";
}
function closeNav() {
  document.getElementById("side-user-menu").style.width = "0";
  document.getElementById("wrapper").style.marginRight= "0";
}

//detail.html 加载 iframe ckeditor
$("#signOutModal").on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var modal = $(this)
    //modal.find('.modal-title').text('Sign Out')
    if(modal.find('.modal-body').children().length === 0){
        let content = '<iframe id="myiframe" src="/accounts/logout/" onload="this.height=iFrame1.document.body.scrollHeight" frameborder="0" style="width:100%;height:100%;" ></iframe>';
        modal.find('.modal-body').append(content);
    }
})

/////////////////////////////////////////////////////////////////////
// 滚动函数
// jQuery for page scrolling feature - requires jQuery Easing plugin
/////////////////////////////////////////////////////////////////////
$(function () {

    $('a.page-scroll').click(function() {
        var bool_animate = false;
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = (target && target.length) ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
                $('html,body').animate({scrollTop: target.offset().top}, 1000);
                bool_animate = true;
            }
            if (bool_animate){
                $('.animation-name',target).each(function(){
                    $(this).addClass("zoomIn animated slower");
                })
            }
        }
    });
});

$(function(){
    $("#about,#skills,#my-blog,#my-work").each(function(){
        var target = $('.animation-name',this);
        var win = $(window);
        win.on('scroll', function(){
            var position = target.offset().top - win.height();
            if (win.scrollTop() > position) {
                target.addClass('zoomIn animated slower');
            }
        });
    })
});
/////////////////////////////////////////////////////////////////////
// ajax 发送送信请求
/////////////////////////////////////////////////////////////////////
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ajax_sendmail(){

    var csrftoken = getCookie('csrftoken');

    var error = false;
    var name = $('#name').val();
    var email = $('#email').val();
    var subject = $('#subject').val();
    var message = $('#message').val();

    if(email.length == 0 || email.indexOf('@') == '-1'){
        var error = true;
        // $('#email_error').fadeIn(500);
        $('#email').addClass("validation");
    }else{
        $('#email').removeClass("validation");
    }
    if(subject.length == 0){
        var error = true;
        $('#subject').addClass("validation");
    }else{
        $('#subject').removeClass("validation");
    }
    if(message.length == 0){
        var error = true;
        $('#message').addClass("validation");
    }else{
        $('#message').removeClass("validation");
    }
    if(error == false){
        var ajax_url;
        ajax_url = '/sendmail/';

        $.ajaxSetup({
            data: {csrfmiddlewaretoken: csrftoken },
        });

        $.ajax({
            url: ajax_url,
            type: 'POST',
            data: {'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message
            },
            success: function(e){
                    //parent.location.reload();
                    $('#mail_fail').text(e);
                    $('#mail_fail').fadeIn(500);
            }
        })
    }
}
