from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.hooks import DashboardItemHook
from allianceauth.menu.hooks import MenuItemHook
from allianceauth.services.hooks import UrlHook

from incursions import urls
from incursions.views import dashboard_widget_active_incursions


class ActiveIncursions(DashboardItemHook):
    def __init__(self):
        DashboardItemHook.__init__(
            self,
            dashboard_widget_active_incursions,
            5
        )


class IncursionsMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("Incursions"),
            "fas fa-skull-crossbones fa-fw",
            "incursions:index",
            navactive=["incursions:index"],
        )

    def render(self, request):
        if request.user.has_perm("incursions.basic_incursions"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("dashboard_hook")
def register_dashboard_widget_active_incursions() -> ActiveIncursions:
    """
    Register our dashboard hook

    :return: The hook
    :rtype: AaEsiStatusDashboardHook
    """

    return ActiveIncursions()


@hooks.register('discord_cogs_hook')
def register_cogs() -> list[str]:
    return ["incursions.cogs.incursions"]


@hooks.register("menu_item_hook")
def register_menu() -> IncursionsMenuItem:
    return IncursionsMenuItem()


@hooks.register("url_hook")
def register_urls() -> UrlHook:
    return UrlHook(urls, "incursions", r"^incursions/")
