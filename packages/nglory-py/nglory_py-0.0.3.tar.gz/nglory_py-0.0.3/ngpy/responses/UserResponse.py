class UserResponse:
    api = ""

    username = ""

    def __init__(self, api, username):
        self.api = api
        self.username = username

    def getUser(self):
        return self.api.getResponse(self.getSpecificEndpoint()).json()

    def getSpecificEndpoint(self):
        return f"{self.api.endpoints['User']}{self.username}"
