class NotationResponse:
    api = ""

    week = ""
    country = ""
    server = ""

    def __init__(self, api, week, country, server):
        self.api = api

        self.week = week
        self.country = country
        self.server = server

    def getNotation(self):
        return self.api.getResponse(self.getSpecificEndpoint()).json()

    def getSpecificEndpoint(self):
        return f"{self.api.endpoints['Notations']}week={self.week}&country={self.country}&server={self.server}"
