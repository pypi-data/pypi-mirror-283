class MarketResponse:
    api = ""

    server = ""

    def __init__(self, api, server):
        self.api = api

        self.server = server

    def getMarket(self):
        return self.api.getResponse(self.getSpecificEndpoint()).json()

    def getSpecificEndpoint(self):
        return f"{self.api.endpoints['Market'].replace('..', self.server)}"
