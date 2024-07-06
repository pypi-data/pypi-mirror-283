from .services.achievements import AchievementsService
from .services.automation import AutomationService
from .services.bisnode import BisnodeService
from .services.bonuschecks import BonuschecksService
from .services.challenges import ChallengesService
from .services.consents import ConsentsService
from .services.contactoverview import ContactoverviewService
from .services.contacts import ContactsService
from .services.interactions import InteractionsService
from .services.interactionschemas import InteractionschemasService
from .services.inventory import InventoryService
from .services.memberstatus import MemberstatusService
from .services.orders import OrdersService
from .services.personlookup import PersonlookupService
from .services.point_accounts import PointAccountsService
from .services.posoffers import PosoffersService
from .services.promotions import PromotionsService
from .services.sms import SmsService
from .services.stores import StoresService
from .services.target_audiences import TargetAudiencesService
from .services.tracking import TrackingService
from .services.transactions import TransactionsService
from .net.environment import Environment


class VoyadoEngageSdk:
    def __init__(
        self,
        api_key: str = None,
        api_key_header: str = "apiKey",
        base_url: str = Environment.DEFAULT.value,
    ):
        """
        Initializes VoyadoEngageSdk the SDK class.
        """
        self.achievements = AchievementsService(base_url=base_url)
        self.automation = AutomationService(base_url=base_url)
        self.bisnode = BisnodeService(base_url=base_url)
        self.bonuschecks = BonuschecksService(base_url=base_url)
        self.challenges = ChallengesService(base_url=base_url)
        self.consents = ConsentsService(base_url=base_url)
        self.contactoverview = ContactoverviewService(base_url=base_url)
        self.contacts = ContactsService(base_url=base_url)
        self.interactions = InteractionsService(base_url=base_url)
        self.interactionschemas = InteractionschemasService(base_url=base_url)
        self.inventory = InventoryService(base_url=base_url)
        self.memberstatus = MemberstatusService(base_url=base_url)
        self.orders = OrdersService(base_url=base_url)
        self.personlookup = PersonlookupService(base_url=base_url)
        self.point_accounts = PointAccountsService(base_url=base_url)
        self.posoffers = PosoffersService(base_url=base_url)
        self.promotions = PromotionsService(base_url=base_url)
        self.sms = SmsService(base_url=base_url)
        self.stores = StoresService(base_url=base_url)
        self.target_audiences = TargetAudiencesService(base_url=base_url)
        self.tracking = TrackingService(base_url=base_url)
        self.transactions = TransactionsService(base_url=base_url)
        self.set_api_key(api_key, api_key_header)

    def set_base_url(self, base_url):
        """
        Sets the base URL for the entire SDK.
        """
        self.achievements.set_base_url(base_url)
        self.automation.set_base_url(base_url)
        self.bisnode.set_base_url(base_url)
        self.bonuschecks.set_base_url(base_url)
        self.challenges.set_base_url(base_url)
        self.consents.set_base_url(base_url)
        self.contactoverview.set_base_url(base_url)
        self.contacts.set_base_url(base_url)
        self.interactions.set_base_url(base_url)
        self.interactionschemas.set_base_url(base_url)
        self.inventory.set_base_url(base_url)
        self.memberstatus.set_base_url(base_url)
        self.orders.set_base_url(base_url)
        self.personlookup.set_base_url(base_url)
        self.point_accounts.set_base_url(base_url)
        self.posoffers.set_base_url(base_url)
        self.promotions.set_base_url(base_url)
        self.sms.set_base_url(base_url)
        self.stores.set_base_url(base_url)
        self.target_audiences.set_base_url(base_url)
        self.tracking.set_base_url(base_url)
        self.transactions.set_base_url(base_url)

        return self

    def set_api_key(self, api_key: str, api_key_header="apiKey"):
        """
        Sets the api key and the api key header for the entire SDK.
        """
        self.achievements.set_api_key(api_key, api_key_header)
        self.automation.set_api_key(api_key, api_key_header)
        self.bisnode.set_api_key(api_key, api_key_header)
        self.bonuschecks.set_api_key(api_key, api_key_header)
        self.challenges.set_api_key(api_key, api_key_header)
        self.consents.set_api_key(api_key, api_key_header)
        self.contactoverview.set_api_key(api_key, api_key_header)
        self.contacts.set_api_key(api_key, api_key_header)
        self.interactions.set_api_key(api_key, api_key_header)
        self.interactionschemas.set_api_key(api_key, api_key_header)
        self.inventory.set_api_key(api_key, api_key_header)
        self.memberstatus.set_api_key(api_key, api_key_header)
        self.orders.set_api_key(api_key, api_key_header)
        self.personlookup.set_api_key(api_key, api_key_header)
        self.point_accounts.set_api_key(api_key, api_key_header)
        self.posoffers.set_api_key(api_key, api_key_header)
        self.promotions.set_api_key(api_key, api_key_header)
        self.sms.set_api_key(api_key, api_key_header)
        self.stores.set_api_key(api_key, api_key_header)
        self.target_audiences.set_api_key(api_key, api_key_header)
        self.tracking.set_api_key(api_key, api_key_header)
        self.transactions.set_api_key(api_key, api_key_header)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
