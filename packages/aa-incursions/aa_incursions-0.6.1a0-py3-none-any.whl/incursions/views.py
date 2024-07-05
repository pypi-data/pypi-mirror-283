from eveuniverse.models.universe_2 import EveConstellation

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from allianceauth.services.hooks import get_extension_logger

from incursions.models import Incursion

logger = get_extension_logger(__name__)


def dashboard_widget_active_incursions(request: WSGIRequest) -> str:
    """
    Returns the current Active incursions as a dashboard Widget

    :param request: request
    :type request: WSGIRequest
    :return: Template Rendered to String
    :rtype: str
    """
    incursions = Incursion.objects.exclude(state=Incursion.States.ENDED).all()
    return render_to_string(
        template_name="incursions/dashboard-widget/incursion-status.html", request=request,
        context={"incursions": incursions})


def history_constellations(request: WSGIRequest) -> HttpResponse:
    """
    Returns a list of all the constellations in EVE, and how many incursions they have had.

    :param request: request
    :type request: WSGIRequest
    :return: Template Rendered to String
    :rtype: str
    """
    constellations = EveConstellation.objects.filter(
        id__lt=21000001
    ).annotate(
        incursions_count=Count("incursion")
    ).values(
        'name',
        'eve_region__name',
        'incursions_count',
    )

    return render(
        template_name="incursions/history/constellations.html", request=request,
        context={"constellations": constellations})


def history_incursions(request: WSGIRequest) -> HttpResponse:
    """
    Returns all the incursions

    :param request: request
    :type request: WSGIRequest
    :return: Template Rendered to String
    :rtype: str
    """
    incursions = Incursion.objects.all(
    ).values(
        'constellation__name',
        'constellation__eve_region__name',
        'faction__faction_name',
        'staging_solar_system__name'
        'staging_solar_system__eve_faction'
        'established_timestamp',
        'ended_timestamp',
    )

    return render(
        template_name="incursions/history/incursions.html", request=request,
        context={"incursions": incursions})


def index(request: WSGIRequest) -> HttpResponse:
    """
    Returns active incursions

    :param request: request
    :type request: WSGIRequest
    :return: Template Rendered to String
    :rtype: str
    """
    incursions = Incursion.objects.exclude(
        state=Incursion.States.ENDED
    ).values(
        'constellation__name',
        'state',
        'constellation__eve_region__name',
        'faction__faction_name',
        'established_timestamp',
        'ended_timestamp',
    )

    return render(
        template_name="incursions/index.html", request=request,
        context={"incursions": incursions})
