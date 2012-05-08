$(function(){


    var last_active;
    $('.sidelink').click(function(event){
        var url = this.href;
        if (last_active)    last_active.removeClass("active");
        $.get(
                url,
                function (data) {
                    $('#content_wrap').html(data);
                }
        );
        $(this).parent().addClass("active");
        last_active = $(this).parent();
        return false;
    });

    $('.table thead tr th a').live("click", function(event){
        var url = this.href;
        $.get(
                url,
                function (data) {
                    $('#content_wrap').html(data);
                }
        );
        return false;
    });

    $('#btn_edit,#btn_new').live("click",function(event){
        var url = this.href;
        $.get(
                url,
                function(data) {
                    $('#content_wrap').html(data);
                    $('input:submit').remove();
                    $('input#sx__id').hide();
                    $('<button>').attr({
                        type:'submit',
                        id:'submit',
                        name:'submit',
                        class:'btn btn-primary'
                    }).html('Save').appendTo('form');
                }
        );
        return false;
    });

    $('#back_one').live("click",function(event){
        var url = this.href;
        $.get(
                url,
                function(data) {
                    $('#content_wrap').html(data);
                }
        );
        return false;
    });

    $('.crd_new > form, .crd_edit > form').live("submit", function(){
        var action = this.action;
        $.post(
                action,
                $(this).serialize()+"&groups=4f980af95e3518a113edccdb",
                function(data) {
                    if (data != "success"){
                        $('#content_wrap').html(data);
                        $('input:submit').remove();
                        $('input#sx__id').hide();
                        $('<button>').attr({
                            type:'submit',
                            id:'submit',
                            name:'submit',
                            class:'btn btn-primary'
                        }).html('Save').appendTo('form');
                        $('form').attr('action',action);
                    }else {
                        $.get(
                                action,
                                function(data) {
                                    $('#content_wrap').html(data);
                                }
                        );
                    }
                }
        );
        return false;
    });
})