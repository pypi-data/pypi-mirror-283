from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class PromotionBasicPresentationModel(BaseModel):
    """Following object is for get/set the presentational side of the promotion.
    This data uses to displey in different kind of views, for an example in Email messages etc.

    This fields populates the "Presentation" section in the admin UI.

    :param heading: Heading for the promotion.
    <br>Uses to show up in different kind of views., defaults to None
    :type heading: str, optional
    :param description: Description for the promotion.
    <br>Uses to show up in different kind of views., defaults to None
    :type description: str, optional
    :param link: A external link for the promotion.
    <br>Uses to show up in different kind of views., defaults to None
    :type link: str, optional
    """

    def __init__(self, heading: str = None, description: str = None, link: str = None):
        if heading is not None:
            self.heading = heading
        if description is not None:
            self.description = description
        if link is not None:
            self.link = link
