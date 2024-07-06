import requests

class NGApi:
    token = ""
    URL = "https://publicapi.nationsglory.fr/"
    headers = {}

    inception_week = "2819"
    current_week = "2842"

    endpoints = {
        "Country": "country/",
        "Notations": "notations?",
        "User": "user/",
        "Market": "hdv/../list"
    }

    def __init__(self, token):
        self.token = token

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def getToken(self):
        return self.token

    def getEndpoint(self, end_point):
        return self.URL + end_point


    def getResponse(self, end_point):
        return requests.get(self.getEndpoint(end_point), headers=self.headers)
