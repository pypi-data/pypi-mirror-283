from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "last_updated": "lastUpdated",
        "purchase_amount_all": "purchaseAmountAll",
        "number_of_article_purchases_all": "numberOfArticlePurchasesAll",
        "average_receipt_all": "averageReceiptAll",
        "latest_receipt_date": "latestReceiptDate",
        "purchase_frequency_all": "purchaseFrequencyAll",
        "purchase_amount_last_year": "purchaseAmountLastYear",
        "number_of_article_purchases_last_year": "numberOfArticlePurchasesLastYear",
        "average_receipt_last_year": "averageReceiptLastYear",
        "purchase_frequency_last_year": "purchaseFrequencyLastYear",
        "purchase_amount_last_two_years": "purchaseAmountLastTwoYears",
        "number_of_article_purchases_last_two_years": "numberOfArticlePurchasesLastTwoYears",
        "average_receipt_last_two_years": "averageReceiptLastTwoYears",
        "purchase_frequency_last_two_years": "purchaseFrequencyLastTwoYears",
    }
)
class PurchaseHistorySummary(BaseModel):
    """PurchaseHistorySummary

    :param last_updated: last_updated, defaults to None
    :type last_updated: str, optional
    :param purchase_amount_all: purchase_amount_all, defaults to None
    :type purchase_amount_all: float, optional
    :param number_of_article_purchases_all: number_of_article_purchases_all, defaults to None
    :type number_of_article_purchases_all: float, optional
    :param average_receipt_all: average_receipt_all, defaults to None
    :type average_receipt_all: float, optional
    :param latest_receipt_date: latest_receipt_date, defaults to None
    :type latest_receipt_date: str, optional
    :param purchase_frequency_all: purchase_frequency_all, defaults to None
    :type purchase_frequency_all: float, optional
    :param purchase_amount_last_year: purchase_amount_last_year, defaults to None
    :type purchase_amount_last_year: float, optional
    :param number_of_article_purchases_last_year: number_of_article_purchases_last_year, defaults to None
    :type number_of_article_purchases_last_year: float, optional
    :param average_receipt_last_year: average_receipt_last_year, defaults to None
    :type average_receipt_last_year: float, optional
    :param purchase_frequency_last_year: purchase_frequency_last_year, defaults to None
    :type purchase_frequency_last_year: float, optional
    :param purchase_amount_last_two_years: purchase_amount_last_two_years, defaults to None
    :type purchase_amount_last_two_years: float, optional
    :param number_of_article_purchases_last_two_years: number_of_article_purchases_last_two_years, defaults to None
    :type number_of_article_purchases_last_two_years: float, optional
    :param average_receipt_last_two_years: average_receipt_last_two_years, defaults to None
    :type average_receipt_last_two_years: float, optional
    :param purchase_frequency_last_two_years: purchase_frequency_last_two_years, defaults to None
    :type purchase_frequency_last_two_years: float, optional
    """

    def __init__(
        self,
        last_updated: str = None,
        purchase_amount_all: float = None,
        number_of_article_purchases_all: float = None,
        average_receipt_all: float = None,
        latest_receipt_date: str = None,
        purchase_frequency_all: float = None,
        purchase_amount_last_year: float = None,
        number_of_article_purchases_last_year: float = None,
        average_receipt_last_year: float = None,
        purchase_frequency_last_year: float = None,
        purchase_amount_last_two_years: float = None,
        number_of_article_purchases_last_two_years: float = None,
        average_receipt_last_two_years: float = None,
        purchase_frequency_last_two_years: float = None,
    ):
        if last_updated is not None:
            self.last_updated = last_updated
        if purchase_amount_all is not None:
            self.purchase_amount_all = purchase_amount_all
        if number_of_article_purchases_all is not None:
            self.number_of_article_purchases_all = number_of_article_purchases_all
        if average_receipt_all is not None:
            self.average_receipt_all = average_receipt_all
        if latest_receipt_date is not None:
            self.latest_receipt_date = latest_receipt_date
        if purchase_frequency_all is not None:
            self.purchase_frequency_all = purchase_frequency_all
        if purchase_amount_last_year is not None:
            self.purchase_amount_last_year = purchase_amount_last_year
        if number_of_article_purchases_last_year is not None:
            self.number_of_article_purchases_last_year = (
                number_of_article_purchases_last_year
            )
        if average_receipt_last_year is not None:
            self.average_receipt_last_year = average_receipt_last_year
        if purchase_frequency_last_year is not None:
            self.purchase_frequency_last_year = purchase_frequency_last_year
        if purchase_amount_last_two_years is not None:
            self.purchase_amount_last_two_years = purchase_amount_last_two_years
        if number_of_article_purchases_last_two_years is not None:
            self.number_of_article_purchases_last_two_years = (
                number_of_article_purchases_last_two_years
            )
        if average_receipt_last_two_years is not None:
            self.average_receipt_last_two_years = average_receipt_last_two_years
        if purchase_frequency_last_two_years is not None:
            self.purchase_frequency_last_two_years = purchase_frequency_last_two_years
