from django.http import (
    HttpRequest,
    # HttpResponse,
)

# import time

# def setup_useragent_on_request_middleware(get_response):
#
#     print('initial call')
#     def middleware(request: HttpRequest):
#         print('before get response')
#         request.user_agent = request.META['HTTP_USER_AGENT']
#         response = get_response(request)
#         print('after get response')
#         return response
#
#     return middleware
#
# class ThrottlingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.ip = {}
#
#     def __call__(self, request: HttpRequest):
#         response = self.get_response(request)
#         ip = request.META.get('REMOTE_ADDR')
#         time_now = time.time()
#         if ip in self.ip:
#             if time_now - self.ip[ip] <= 0.1:
#                 print('with error', self.ip)
#                 self.ip[ip] = time_now
#                 raise Exception('Rate limit request')
#         self.ip[ip] = time_now
#         print('without error', self.ip)
#         return response


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests_count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses_count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")
