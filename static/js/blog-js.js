$(document).ready(function() {
    $("#navbarResponsive .navbar-nav > li.nav-item").each(function(){
        if($(">a",this)[0].href==String(window.location)){
            $(">div",this).eq(0).addClass("active-bg");
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