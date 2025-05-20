import uuid
from django.utils.deprecation import MiddlewareMixin


class VisitorUUIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if visitor_uuid exists in cookies
        visitor_uuid = request.COOKIES.get("visitor_uuid")

        # If no UUID exists, create a new one
        if not visitor_uuid:
            visitor_uuid = str(uuid.uuid4())
            request.visitor_uuid = visitor_uuid
            request.set_cookie = True
        else:
            request.visitor_uuid = visitor_uuid
            request.set_cookie = False

    def process_response(self, request, response):
        # Set the cookie if it's a new visitor
        if getattr(request, "set_cookie", False):
            response.set_cookie(
                "visitor_uuid", request.visitor_uuid, max_age=365 * 24 * 60 * 60
            )  # 1 year
        return response
