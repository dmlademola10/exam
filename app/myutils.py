import re, random, html


# ***************VARS***************
class Person:
    fullname: str
    email: str
    role: str
    access: int()

    def __init__(self, fullname, email, role, access):
        self.fullname = fullname
        self.email = email
        self.role = role
        self.access = access

    def escape(self):
        return {
            "fullname": html.escape(self.fullname),
            "email": html.escape(self.email),
            "role": html.escape(self.role),
            "access": html.escape(self.role),
        }


def authenticate_user(req):
    return req.session.get("active_user", False)
    # return False


def trim(string):
    # print(re.findall(r"\s+\n+", string))
    # string = re.sub(r"\s+\n+", "\n", string.strip())
    # string = re.sub(r"\s+\n+", "\n", string)
    return re.sub(r"\s+", " ", string.strip())


def format_announcements(anns):
    html_fmt = str()
    for ann in anns:
        html_fmt += '<div class="announcement" id="a' + str(ann.id) + '">'
        html_fmt += '<div class="status">'
        if ann.status == "new":
            html_fmt += '<div class="new" title="Unread Announcement."></div>'

        html_fmt += "</div>"
        html_fmt += '<div class="ann_title">'
        html_fmt += "<h2>" + ann.title + "</h2>"
        html_fmt += "</div>"
        html_fmt += '<div class="action">'
        html_fmt += '<div class="act_btn edit" title="Edit.">'
        html_fmt += '<span class="icon icon4"></span>'
        html_fmt += "</div>"
        html_fmt += '<div class="act_btn del" title="Delete.">'
        html_fmt += '<span class="icon icon3"></span>'
        html_fmt += "</div>"
        html_fmt += "</div>"
        html_fmt += "</div>"
    return html_fmt


def key_gen():
    chars = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "0",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    key = str()
    i = 1
    while i <= 20:
        key += chars[random.randint(0, len(chars) - 1)]
        i += 1
    return key
