from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PhoneOperator:
    """
    Store the phone operator data.
    This is used to cache the data we scrape from crdc.be which gives us the operator of a phone number.

    This is stored into the `phone_operators_cache` collection.
    """

    _id: str
    operator: str
    last_update: datetime | None
