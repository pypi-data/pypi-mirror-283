class CountryResponse:
    api = ""

    country = ""
    server = ""

    def __init__(self, api, country, server):
        self.api = api
        self.country = country
        self.server = server

    def getCountry(self):
        return self.api.getResponse(self.getSpecificEndpoint()).json()

    def getSpecificEndpoint(self):
        return f"{self.api.endpoints['Country']}{self.server}/{self.country}"
