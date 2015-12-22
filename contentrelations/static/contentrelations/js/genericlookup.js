function showRelatedResourceLookupPopup(triggeringLink, ctArray) {
    var realName = triggeringLink.id.replace(/^lookup_/, '');
    var name = id_to_windowname(realName);
    realName = realName.replace(/object_id/, 'object_type');
    var select = document.getElementById(realName);
    if (select.selectedIndex === 0) {
        alert("Select a content type first.");
        return false;
    }
    var selectedItem = select.item(select.selectedIndex).value;
    var href = ctArray[selectedItem];
    if (href.search(/\?/) >= 0) {
        href = href + '&_popup=1&_to_field=id';
    } else {
        href = href + '?_popup=1&_to_field=id';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function showGenericRelatedObjectLookupPopup(triggeringLink, ctArray) {
    var realName = triggeringLink.id.replace(/^lookup_/, '');
    var name = id_to_windowname(realName);
    realName = realName.replace(/object_id/, 'content_type');
    var select = document.getElementById(realName);
    if (select.selectedIndex === 0) {
        alert("Select a content type first.");
        return false;
    }
    var selectedItem = select.item(select.selectedIndex).value;
    var href = ctArray[selectedItem];
    if (href.search(/\?/) >= 0) {
        href = href + '&_popup=1&_to_field=id';
    } else {
        href = href + '?_popup=1&_to_field=id';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

(function($){
    $(document).ready(function(){
        $('a.gen-related-lookup').click(function(e) {
            e.preventDefault();
            var event = $.Event('django:gen-lookup-related');
            var ctypes = $(this).data('contenttypes').replace(/'/g, '"');
            var ctypesObj = JSON.parse(ctypes);
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                showGenericRelatedObjectLookupPopup(this, ctypesObj);
            }
        });
    })
})(django.jQuery);
