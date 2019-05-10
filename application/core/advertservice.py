from typing import Optional, Tuple

from application import db
from application.core.models import AdCampaign
from application.core import userservice


coverages_by_budget = {
    'small': (5, 15),
    'medium': (15, 30),
    'large': (30, 40),
    'very_large': (40, 50)
}


def get_current_campaign(user_id: int) -> AdCampaign:
    """
    Get current campaign by user
    :param user_id: User's Telegram-ID
    :return: current campaign
    """
    user = userservice.get_user_by_id(user_id)
    return user.campaigns.filter(AdCampaign.confirmed != True).first()


def get_all_campaigns():
    """
    All campaigns
    :return: list of ad campaigns
    """
    return AdCampaign.query.all()


def create_campaign(user_id: int):
    """
    Create a new campaign or reset not confirmed current campaign
    :param user_id: User's Telegram-ID
    :return: void
    """
    current_campaign = get_current_campaign(user_id)
    if not current_campaign:
        new_campaign = AdCampaign(user_id=user_id)
        db.session.add(new_campaign)
    else:
        current_campaign.age_of_audience = None
        current_campaign.product_name = None
        current_campaign.target_audience = None
    db.session.commit()


def set_product_name(user_id: int, product_name: str):
    """
    Set product name to current user's campaign
    :param user_id: User's Telegram-ID
    :param product_name: product name
    :return: void
    """
    current_campaign = get_current_campaign(user_id)
    current_campaign.product_name = product_name
    db.session.commit()
    return current_campaign


def set_target_audience(user_id: int, target: str) -> AdCampaign:
    """
    Set target audience for current campaign
    :param user_id: User's Telegram-ID
    :param target: Value of application.core.models.AdCampaign.TargetAudiences
    :return: Current Campaign
    """
    current_campaign = get_current_campaign(user_id)
    current_campaign.target_audience = target
    db.session.commit()
    return current_campaign


def add_age_audience(user_id: int, age: str) -> AdCampaign:
    """
    Add age of audience for current campaign
    :param user_id: User's Telegram-ID
    :param age: age
    :return: Current ad order
    """
    current_campaign = get_current_campaign(user_id)
    if not current_campaign.age_of_audience:
        current_campaign.age_of_audience = ''
    if age == AdCampaign.AudienceAges.ALL:
        current_campaign.age_of_audience = age
    else:
        current_campaign.age_of_audience += (age + ', ')
    db.session.commit()
    return current_campaign


def reset_audience_ages(user_id: int) -> AdCampaign:
    """
    Resrt current value of audience ages
    :param user_id:
    :return: Current ad order
    """
    current_campaign = get_current_campaign(user_id)
    current_campaign.age_of_audience = None
    db.session.commit()
    return current_campaign


def set_budget(user_id: int, budget: str) -> AdCampaign:
    """
    Set budget for current campaign and return coverages by it
    :param user_id: User's Telegram-ID
    :param budget: value of budget
    :return: Current Ad Order
    """
    current_campaign = get_current_campaign(user_id)
    current_campaign.budget = budget
    db.session.commit()
    return current_campaign


def confirm_campaign(user_id: int) -> AdCampaign:
    """
    Confirm the order of ad campaign
    :param user_id: User's Telegram-ID
    :return: confirmed AdCampaign
    """
    current_campaign = get_current_campaign(user_id)
    current_campaign.confirmed = True
    db.session.commit()
    return current_campaign


def get_coverages_by_budget(budget: str) -> Optional[Tuple[int, int]]:
    if budget in coverages_by_budget:
        return coverages_by_budget[budget]
    return None
