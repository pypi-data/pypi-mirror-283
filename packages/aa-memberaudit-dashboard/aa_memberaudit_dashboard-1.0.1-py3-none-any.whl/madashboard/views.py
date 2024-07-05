from django.template.loader import render_to_string

from allianceauth.authentication.models import CharacterOwnership

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


def dashboard_memberaudit_check(request):
    unregistered = CharacterOwnership.objects.filter(
        user=request.user, character__memberaudit_character__isnull=True
    )

    chars = {}

    for char in unregistered:
        chars[char.character.character_id] = {
            "id": char.character.character_id,
            "name": char.character.character_name,
        }

    context = {
        "chars": chars if chars else None,
    }
    return render_to_string(
        "madashboard/dashboard.html", context=context, request=request
    )
