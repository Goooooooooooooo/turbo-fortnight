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
var move = document.getElementById("move_comment");
if(move){
    move.addEventListener('click', function(){
        var target = document.getElementById('comment_display');
        target.scrollIntoView(false);
    })
}

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
function initEvents() {
    document.addEventListener('keyup', function(ev) {
        // escape key.
        if( ev.keyCode == 27 ) {
            closeSearch();
        }
    });
}
initEvents();

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