from django.shortcuts import redirect


class LanguagePrefixRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if path.startswith("/en-us/"):
            return redirect("/en/" + path[7:])
        if path.startswith("/ka-ge/"):
            return redirect("/ka/" + path[7:])
        if path.startswith("/ru-ru/"):
            return redirect("/ru/" + path[7:])
        # Add more rules if needed
        return self.get_response(request)
