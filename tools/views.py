URLS = []

class ViewConfig(object):
    def __init__(self, url, method):
        self.method = method
        self.url = url

    def __call__(self, func):
        def view(*args, **kwargs):
            return func(*args, **kwargs)

        for u in URLS:
            if u[0] == self.url:
                if self.method == "*":
                    for m in ["GET", "HEAD", "POST",
                              "OPTIONS", "PUT", "DELETE",
                              "TRACE", "CONNECT"]:
                        u[1][m] = view
                else:
                    u[1][self.method] = view
                return view
        URLS.append((self.url, {self.method: view}))
        return view
