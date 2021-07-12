from copy import deepcopy
from functools import reduce
from typing import Dict, List
from .email import EmailManager


def deep_merge(*dicts: List[Dict], update=False) -> Dict:
    """
    Merges dicts deeply.
    Parameters
    ----------
    dicts : list[dict]
        List of dicts.
    update : bool
        Whether to update the first dict or create a new dict.
    Returns
    -------
    merged : dict
        Merged dict.
    """
    def merge_into(d1: Dict, d2: Dict):
        for key in d2:
            if key not in d1 or not isinstance(d1[key], dict):
                d1[key] = deepcopy(d2[key])
            else:
                d1[key] = merge_into(d1[key], d2[key])
        return d1

    if update:
        return reduce(merge_into, dicts[1:], dicts[0])
    else:
        return reduce(merge_into, dicts, {})



def send_email(addrs, subject, content):
    '''
    发送邮件
    '''
    from config import get_app_config
    email_config = get_app_config().email
    emailer = EmailManager(
        user=email_config.user,
        pwd=email_config.password,
        host=email_config.host,
        port=email_config.port,
        nickname=email_config.nickname,
    )
    emailer.send_html_mail(addrs, subject, content)
