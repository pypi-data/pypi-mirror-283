import re

from django.conf import settings


def get_site_url():  # regex sso url
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for m in matches:
        url = m.groups()[0]  # first match

    return url


INCURSIONS_AUTO_HIGHSEC_STATIC = getattr(settings, 'INCURSIONS_AUTO_HIGHSEC_STATIC', True)
