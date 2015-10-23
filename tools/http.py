import sys
import settings
from tools import format_html
from urlparse import unquote

def render_html(filename, context={}):
    with open(settings.TEMPLATE_DIR + filename, 'rb') as f:
        HTML = f.read()
    HTML = format_html(HTML, context)
    resp = "\r\n".join(["HTTP/1.1 200 OK",
                        "Content-Type: text/html",
                        "Content-Length: {length}",
                        "\r\n{html}"])
    resp = resp.format(
        length=str(sys.getsizeof(HTML)),
        html=HTML
    )
    return resp

def redirect(uri):
    return "\r\n".join(["HTTP/1.1 303 See Other",
                        "Location: {}",
                        "\r\n"]).format(uri)


def parse_request(request):
    try:
        request = request.split("\r\n\r\n", 1)
        req = request[0].split("\r\n")
        par = request[1]
        for i, r in enumerate(req):
            req[i] = r.split()
        method = req[0][0].upper()
        uri = req[0][1]
        proto = req[0][2].upper()
        headers = {}
        for line in req[1:]:
            headers[line[0].upper()] = " ".join(line[1:])
        params = {}
        if par:
            for param in par.split("&"):
                param = param.split("=")
                params[param[0]] = unquote(" ".join(
                    param[1].split("+"))
                )
        data = {
            "method": method,
            "uri": uri,
            "protocol": proto,
            "headers": headers,
            "params": params,
        }
        return data
    except IndexError:
        raise SyntaxError("400 Bad Request")

def err_response(e):
    html = ("<html><head><title>oops</title></head>"
            "<body><p>{}</p></body></html>")
    html = html.format(e.message)
    resp = ("HTTP/1.1 {err}\r\n"
            "Content-Type: text/html\r\n"
            "Content-Length: {length}\r\n"
            "\r\n{html}")
    return resp.format(
        html=html,
        length=str(sys.getsizeof(html)),
        err=e.message
    )

