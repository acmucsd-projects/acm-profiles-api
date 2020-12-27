from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from django.http.response import HttpResponseNotFound
import requests
import os

PORTAL_URL = os.environ["MEMBERSHIP_PORTAL_API"]
PORTAL_USER_URL = PORTAL_URL + "api/v2"

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = True
        if request.path != "/api/user/login":
            auth = self.authenticate(request.headers)
        if auth:
            response = self.get_response(request)
            if type(response) != Response:
                if type(response) == HttpResponseNotFound:
                    return JsonResponse(data={"error" : "HTTP Response Not Found. Invalid URL."}, status = status.HTTP_404_NOT_FOUND)
                return JsonResponse(data={"error" : "Invalid Response"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response = JsonResponse(data={"error" : "Invalid JWT"}, status = status.HTTP_401_UNAUTHORIZED)
        return response

    def authenticate(self, headers):
        if "Authorization" not in headers:
            return False
        response = requests.get(PORTAL_USER_URL + "/user", headers={"Authorization": headers["Authorization"]}, data={}).json()
        if response["error"] is not None:
            return False
        return True