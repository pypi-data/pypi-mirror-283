class GableClient:
    def __init__(self, api_endpoint, api_key) -> None:
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def contracts_validate(self, contracts):
        return []

    def contracts_publish(self, contracts):
        return []
