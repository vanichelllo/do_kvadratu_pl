SESSION_KEY = 'analytics_events'


def queue_event(request, name, params=None):
    """Запам'ятовує подію для Google Analytics: її надішле наступна сторінка сайту
    (і лише якщо відвідувач дозволив аналітику в банері cookie)."""
    events = request.session.get(SESSION_KEY, [])
    events.append({'name': name, 'params': params or {}})
    request.session[SESSION_KEY] = events[-10:]
