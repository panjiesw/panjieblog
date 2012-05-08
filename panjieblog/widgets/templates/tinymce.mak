<%namespace name="tw" module="tw2.core.mako_util"/>\
<textarea ${tw.attrs(attrs=w.attrs)}>${w.value or ''}</textarea>
<script type="text/javascript">
    tinyMCE.init({
        theme : "advanced",
        mode : "textareas",
        width: "600",
        plugins : "fullscreen,inlinepopups",
        theme_advanced_toolbar_location: "top",
        theme_advanced_buttons1_add : "fullscreen",
        dialog_type : "modal"
    });
</script>