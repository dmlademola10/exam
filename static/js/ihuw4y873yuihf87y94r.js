// Announcements

document.body.onload = function () {
    event_listeners();
}

function fscreen(child) {
    $all("#fscreen div.fscreen_cont").forEach(function (val, ind, arr) {
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

function get_announcement(id) {
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
                    ann = JSON.parse(response.message);
                    $("#ann_view .title").innerHTML = ann["title"];
                    $("#ann_view .details").innerHTML = ann["details"];
                    $("#ann_view .announcer #announcer").innerHTML = ann["announcer"];
                    $("#ann_view .announcer #datetime").innerHTML = ann["datetime"];
                    fscreen("#ann_view");
                    if ($("#announcements .announcement#a" + id + " .status").contains($("#announcements .announcement#a" + id + " .status .new"))) {
                        $("#announcements .announcement#a" + id + " .status").removeChild($("#announcements .announcement#a" + id + " .status .new"));
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

    xmlhttp.open("GET", "/exam/announcements/" + id + "/", true);
    xmlhttp.send();
}

function delete_announcement(id) {
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
                    refresh_announcements();
                }
            } else {
                msg_box_view('Sorry, an error occurred.');
            }
        }
    }

    xmlhttp.onerror = function () {
        msg_box_view('Failed to connect to the internet.');
    }

    xmlhttp.open("GET", "/exam/announcements/delete/" + id, true);
    xmlhttp.send();
}

function edit_announcement_setup(id) {
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
                    ann = JSON.parse(response.message);
                    $("#message02").innerHTML = "";
                    $forms("edit_announcement", "edit_id").value = ann["id"];
                    $forms("edit_announcement", "edit_title").value = ann["title"];
                    $forms("edit_announcement", "edit_details").value = ann["details"];
                    fscreen("#edit_ann");
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

    xmlhttp.open("GET", "/exam/announcements/" + id + "/?edit=true", true);
    xmlhttp.send();
}

function add_announcement(event) {
    event.preventDefault();
    if ($forms("new_announcement", "new_title").value.length == 0 || $forms("new_announcement", "new_details").value.length == 0) {
        $("#message01").innerHTML = "<span class='err'>Title or Details can't be empty.</span>";
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
                    refresh_announcements();
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

    var form_s = $forms('new_announcement');
    var data = new FormData(form_s);
    xmlhttp.open("POST", "/exam/announcements/new/", true);
    xmlhttp.send(data);
}

function mod_announcement(event) {
    event.preventDefault();
    if ($forms("edit_announcement", "edit_title").value.length == 0 || $forms("edit_announcement", "edit_details").value.length == 0) {
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
                    refresh_announcements();
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

    var form_s = $forms('edit_announcement');
    var data = new FormData(form_s);
    xmlhttp.open("POST", "/exam/announcements/edit/", true);
    xmlhttp.send(data);
}


function refresh_announcements() {
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
                    $("#announcements").innerHTML = response.message;
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

    xmlhttp.open("GET", "/exam/announcements/refresh/", true);
    xmlhttp.send();
}

function event_listeners() {
    $("#fscreen").onclick = function () {
        $("#fscreen").style.display = "none";
    }

    $("#add_new").onclick = function () {
        fscreen("#new_ann");
    }

    $all(".input_group span.clear").forEach(function (val, ind, arr) {
        val.onclick = function () {
            $("input#" + this.getAttribute("data-attachment")).value = "";
            $("input#" + this.getAttribute("data-attachment")).focus();
        }
    })

    $all(".fscreen_cont").forEach(function (val, ind, arr) {
        val.onclick = function (event) {
            event.stopImmediatePropagation();
        }
    })

    $all(".fscreen_cont form .form_bottom button[type=reset]").forEach(function (val, ind, arr) {
        val.onclick = function () {
            $("#" + this.getAttribute("data-attachment")).innerHTML = "";
        }
    })

    $forms("new_announcement", "new_title").onkeydown = function () {
        $("#message01").innerHTML = "";
    }

    $forms("new_announcement", "new_details").onkeydown = function () {
        $("#message01").innerHTML = "";
    }

    $forms("edit_announcement", "edit_title").onkeydown = function () {
        $("#message02").innerHTML = "";
    }

    $forms("edit_announcement", "edit_details").onkeydown = function () {
        $("#message02").innerHTML = "";
    }

    $all("#announcements .announcement").forEach(function (val, ind, arr) {
        val.onclick = function () {
            get_announcement(this.getAttribute("id").replace("a", ""));
        }
    })

    // $all(".announcement").forEach(function (val, ind, arr) {
    //     val.onmouseover = function () {
    //         $(".announcement#" + this.id + " .action").style.opacity = 1;
    //     }
    // })

    // $all(".announcement").forEach(function (val, ind, arr) {
    //     val.onmouseout = function () {
    //         $(".announcement#" + this.id + " .action").style.opacity = 0;
    //     }
    // })

    $all(".announcement .action .act_btn.edit").forEach(function (val, ind, arr) {
        val.onclick = function (event) {
            event.stopImmediatePropagation();
            edit_announcement_setup(this.parentNode.parentNode.id.replace("a", ""));
        }
    })

    $all(".announcement .action .act_btn.del").forEach(function (val, ind, arr) {
        val.onclick = function (event) {
            event.stopImmediatePropagation();
            if (confirm("Are you sure you want to delete this announcement? You can't undo this.")) {
                delete_announcement(this.parentNode.parentNode.id.replace("a", ""));
            }
        }
    })
}
