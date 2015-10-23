import transaction
from tools.http import render_html, redirect
from tools.views import ViewConfig

from models import BlogPost


@ViewConfig(r"^/$", "GET")
def homeview(request, session):
    context = {"posts": []}
    posts = BlogPost.get_all(session)
    for post in posts:
        context["posts"].append([post.title, post.id])
    return render_html("index.html", context)


@ViewConfig(r"^/about$", "GET")
def aboutview(request, session):
    return render_html("about.html")


@ViewConfig(r"^/post/\d+$", "GET")
def postview(request, session):
    uri = request["uri"].split("/")
    post_id = int(uri[-1])
    try:
        post = BlogPost.get_by_id(post_id, session)
        title = post.title
        text = post.text
    except Exception as e:
        print e.message
        raise Exception("404 Not Found")
    return render_html("post.html", context={
        "title": title,
        "text": text
    })


@ViewConfig(r"^/new$", "GET")
def newview(request, session):
    return render_html("new.html")


@ViewConfig(r"^/new$", "POST")
def add(request, session):
    new = BlogPost.write(session=session, **request["params"])
    _id = new.id
    transaction.commit()
    print _id
    return redirect("/post/{}".format(_id))
