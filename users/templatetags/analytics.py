from django import template
from django.utils.html import format_html, json_script

from users.analytics import SESSION_KEY

register = template.Library()


@register.simple_tag(takes_context=True)
def analytics_events(context):
    # Викликається лише в base.html (не в листах), тож подія забирається з сесії рівно один раз
    request = context.get('request')
    session = getattr(request, 'session', None)
    if session is None or SESSION_KEY not in session:
        return ''
    events = session.pop(SESSION_KEY)
    return format_html(
        '{}<script>JSON.parse(document.getElementById("dk-analytics-events").textContent)'
        '.forEach(function (e) {{ window.dkTrack(e.name, e.params); }});</script>',
        json_script(events, 'dk-analytics-events'),
    )
