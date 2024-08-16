// General

function $(sel) {
    return document.querySelector(sel);
}
function $all(sels) {
    return document.querySelectorAll(sels);
}
function $forms(form, field) {
    if (field != undefined) {
        return document.forms[form][field];
    }
    return document.forms[form];
}

$all("#nav .nav_item").forEach(function (elem) {
    elem.onclick = function () {
        window.location.assign(this.getAttribute("data-url"))
    }
})
$("#nav .nav_item.logout").onclick = function (event) {
    event.stopImmediatePropagation();
    if (confirm("Are you sure you want to signout?")) {
        window.location.assign("/exam/?action=signout")
    }
}
