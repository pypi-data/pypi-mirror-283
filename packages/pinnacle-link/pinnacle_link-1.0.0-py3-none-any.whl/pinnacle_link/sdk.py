from .services.fixtures import FixturesService
from .services.odds import OddsService
from .services.line import LineService
from .services.others import OthersService
from .net.environment import Environment

class PinnacleLink:
    def __init__(self,base_url: str = Environment.DEFAULT.value):
        """
        Initializes PinnacleLink the SDK class.
        """
        self.fixtures = FixturesService(base_url=base_url)
        self.odds = OddsService(base_url=base_url)
        self.line = LineService(base_url=base_url)
        self.others = OthersService(base_url=base_url)

    def set_base_url(self, base_url):
        """
        Sets the base URL for the entire SDK.
        """
        self.fixtures.set_base_url(base_url)
        self.odds.set_base_url(base_url)
        self.line.set_base_url(base_url)
        self.others.set_base_url(base_url)

        return self









# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c

