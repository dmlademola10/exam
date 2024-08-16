// Admins

document.body.onload = function () {
    event_listeners();
}

function fscreen(child) {
    $all("#fscreen div.fscreen_cont").forEach(function (val) {
        val.style.display = "none";
    })
    $(child).style.display = "flex";
    $("#fscreen").style.display = "flex";
}

function msg_box_view(message) {
    if ($('body').contains($('div.msg_box'))) {
        clearTimeout(del_msg_box);
        $('div.msg_box p.text1').innerHTML = message;
        del_msg_box = setTimeout(function () {
            if ($('body').contains($('div.msg_box'))) {
                $('div.msg_box').parentNode.removeChild($('div.msg_box'));
            }
        }, 10000);
        return;
    }
    var msg_box = document.createElement("div");
    var _class = document.createAttribute("class");
    _class.value = "msg_box";
    msg_box.attributes.setNamedItem(_class);
    var close = document.createElement("span");
    var _class = document.createAttribute("class");
    _class.value = 'close1';
    close.attributes.setNamedItem(_class);
    var click_fun = document.createAttribute("onclick");
    click_fun.value = "$('div.msg_box').parentNode.removeChild($('div.msg_box'));";
    close.attributes.setNamedItem(click_fun);
    var title = document.createAttribute("title");
    title.value = "Close.";
    close.attributes.setNamedItem(title);
    close.innerHTML = '&times;';
    msg_box.appendChild(close);
    document.body.insertBefore(msg_box, document.body.childNodes[0]);

    var text1 = document.createElement("p");
    var _class = document.createAttribute("class");
    _class.value = "text1";
    text1.attributes.setNamedItem(_class);
    // var text = document.createTextNode(message);
    text1.innerHTML = message;
    // text1.appendChild(text);
    msg_box.appendChild(text1);
    del_msg_box = setTimeout(function () {
        if ($('body').contains($('div.msg_box'))) {
            $('div.msg_box').parentNode.removeChild($('div.msg_box'));
        }
    }, 10000)
}

function get_admin_detail(id) {
    if (isNaN(id)) {
        msg_box_view("Sorry, an error occurred!");
        return false;
    }
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                response = JSON.parse(this.responseText);
                if (response.success === true) {
                    adm = JSON.parse(response.message);
                    $("#admin_view .title").innerHTML = adm["title"];
                    $("#admin_view .details").innerHTML = adm["details"];
                    $("#admin_view .announcer #announcer").innerHTML = adm["announcer"];
                    $("#admin_view .announcer #datetime").innerHTML = adm["datetime"];
                    fscreen("#admin_view");
                    if ($("#admins .admin#a" + id + " .status").contains($("#admins .admin#a" + id + " .status .new"))) {
                        $("#admins .admin#a" + id + " .status").removeChild($("#admins .admin#a" + id + " .status .new"));
                    }
                } else {
                    $("#fscreen").style.display = "none";
                    msg_box_view(response.message);
                }
            } else {
                msg_box_view('Sorry, an error occurred.');
            }
        }
    }

    xmlhttp.onerror = function () {
        msg_box_view('Failed to connect to the internet.');
    }

    xmlhttp.open("GET", "/exam/admins/" + id + "/", true);
    xmlhttp.send();
}

function delete_admin(id) {
    if (isNaN(id)) {
        msg_box_view("Sorry, an error occurred!");
        return false;
    }
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                response = JSON.parse(this.responseText);
                msg_box_view(response.message);
                if (response.success === true) {
                    refresh_admins();
                }
            } else {
                msg_box_view('Sorry, an error occurred.');
            }
        }
    }

    xmlhttp.onerror = function () {
        msg_box_view('Failed to connect to the internet.');
    }

    xmlhttp.open("GET", "/exam/admins/delete/" + id, true);
    xmlhttp.send();
}

function edit_admin_setup(id) {
    if (isNaN(id)) {
        msg_box_view("Sorry, an error occurred!");
        return false;
    }
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                response = JSON.parse(this.responseText);
                if (response.success === true) {
                    adm = JSON.parse(response.message);
                    $("#message02").innerHTML = "";
                    $forms("edit_admin", "edit_id").value = adm["id"];
                    $forms("edit_admin", "edit_title").value = adm["title"];
                    $forms("edit_admin", "edit_details").value = adm["details"];
                    fscreen("#edit_adm");
                } else {
                    $("#fscreen").style.display = "none";
                    msg_box_view(response.message);
                }
            } else {
                msg_box_view('Sorry, an error occurred.');
            }
        }
    }

    xmlhttp.onerror = function () {
        msg_box_view('Failed to connect to the internet.');
    }

    xmlhttp.open("GET", "/exam/admins/" + id + "/?edit=true", true);
    xmlhttp.send();
}

function add_admin(event) {
    event.preventDefault();
    if ($forms("new_admin", "new_fullname").value.length == 0 || $forms("new_admin", "new_email").value.length == 0) {
        $("#message01").innerHTML = "<span class='err'>Fill all fields.</span>";
        return false;
    }
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                response = JSON.parse(this.responseText);
                if (response.success === true) {
                    $("#message01").innerHTML = "<span class='suc'>" + response.message + "</span>";
                    refresh_admins();
                } else {
                    $("#message01").innerHTML = "<span class='err'>" + response.message + "</span>";
                }
            } else {
                msg_box_view('Sorry, an error occurred.');
            }
        }
    }

    xmlhttp.onerror = function () {
        msg_box_view('Failed to connect to the internet.');
    }

    var form_s = $forms('new_admin');
    var data = new FormData(form_s);
    xmlhttp.open("POST", "/exam/admins/new/", true);
    xmlhttp.send(data);
}

function mod_admin(event) {
    event.preventDefault();
    if ($forms("edit_admin", "edit_title").value.length == 0 || $forms("edit_admin", "edit_details").value.length == 0) {
        $("#message02").innerHTML = "<span class='err'>Title or Details can't be empty.</span>";
        return false;
    }
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                response = JSON.parse(this.responseText);
                if (response.success === true) {
                    $("#message02").innerHTML = "<span class='suc'>" + response.message + "</span>";
                    refresh_admins();
                } else {
                    $("#message02").innerHTML = "<span class='err'>" + response.message + "</span>";
                }
            } else {
                msg_box_view('Sorry, an error occurred.');
            }
        }
    }

    xmlhttp.onerror = function () {
        msg_box_view('Failed to connect to the internet.');
    }

    var form_s = $forms('edit_admin');
    var data = new FormData(form_s);
    xmlhttp.open("POST", "/exam/admins/edit/", true);
    xmlhttp.send(data);
}


function refresh_admins() {
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                response = JSON.parse(this.responseText);
                if (response.success === true) {
                    $("#admins").innerHTML = response.message;
                    event_listeners();
                } else {
                    msg_box_view(response.message)
                }
            } else {
                msg_box_view('Sorry, an error occurred.');
            }
        }
    }

    xmlhttp.onerror = function () {
        msg_box_view('Failed to connect to the internet.');
    }

    xmlhttp.open("GET", "/exam/admins/refresh/", true);
    xmlhttp.send();
}

function event_listeners() {
    $("#fscreen").onclick = function () {
        $("#fscreen").style.display = "none";
    }

    $("#add_new").onclick = function () {
        fscreen("#new_admin");
    }

    $all(".input_group span.clear").forEach(function (val) {
        val.onclick = function () {
            $("input#" + this.getAttribute("data-attachment")).value = "";
            $("input#" + this.getAttribute("data-attachment")).focus();
        }
    })

    $all(".fscreen_cont").forEach(function (val) {
        val.onclick = function (event) {
            event.stopImmediatePropagation();
        }
    })

    $all(".fscreen_cont form .form_bottom button[type=reset]").forEach(function (val) {
        val.onclick = function () {
            $("#" + this.getAttribute("data-attachment")).innerHTML = "";
        }
    })

    $forms("new_admin", "new_fullname").onkeydown = function () {
        $("#message01").innerHTML = "";
    }

    $forms("new_admin", "new_email").onkeydown = function () {
        $("#message01").innerHTML = "";
    }

    $all("input[type=radio]").forEach(function (val) {
        val.onclick = function () {
            $("#message01").innerHTML = "";
        }
    })

    $forms("edit_admin", "edit_title").onkeydown = function () {
        $("#message02").innerHTML = "";
    }

    $forms("edit_admin", "edit_details").onkeydown = function () {
        $("#message02").innerHTML = "";
    }

    $all("#admins .admin").forEach(function (val) {
        val.onclick = function () {
            get_admin_detail(this.getAttribute("id").replace("a", ""));
        }
    })

    $all(".admin .action .act_btn.edit").forEach(function (val) {
        val.onclick = function (event) {
            event.stopImmediatePropagation();
            edit_admin_setup(this.parentNode.parentNode.id.replace("a", ""));
        }
    })

    $all(".admin .action .act_btn.del").forEach(function (val) {
        val.onclick = function (event) {
            event.stopImmediatePropagation();
            if (confirm("Are you sure you want to delete this admin? You can't undo this.")) {
                delete_admin(this.parentNode.parentNode.id.replace("a", ""));
            }
        }
    })
}
