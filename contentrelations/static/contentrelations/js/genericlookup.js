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
    var realName = triggeringLink.id.replace(/^lookup_/, ''),
        name = id_to_windowname(realName),
        names,
        select;
    names = "#" + realName.replace(/object_id/, 'object_type');
    names += ",#" + realName.replace(/object_id/, 'content_type');
    select = django.jQuery(names).first()[0];
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
        $('a.gen-related-lookup').unbind('click').click(function(e) {
            e.preventDefault();
            e.stopPropagation();
            var event = $.Event('django:gen-lookup-related'),
                ctypes = $(this).data('contenttypes'),
                ctypesObj;
            if (typeof ctypes == "string") {
                ctypes = ctypes.replace(/'/g, '"');
                ctypesObj = JSON.parse(ctypes);
            } else {
                ctypesObj = ctypes;
            }
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                showGenericRelatedObjectLookupPopup(this, ctypesObj);
                return false;
            }
        });
    });
})(django.jQuery);
