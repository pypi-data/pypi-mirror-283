from math import sin, cos, sqrt, atan2, radians

# Approximate radius of earth in km
R = 6373.0


def define_distance(user1: dict, user2: dict, unit: str = 'm', user1_to_user2=True, precision=1) -> float:
    """

    :param user1:
    :param user2:
    :param unit:
    :param user1_to_user2:
    :param precision:
    :return:

    user1 = {
    "lat": "",
    "lng": "" }
    like this you should give location
    """
    if not (user1 and user2):
        return None
    try:
        client_lat = radians(user1.get('lat'))
        client_lot = radians(user1.get('lng'))
        sitter_lat = radians(user2.get('lat'))
        sitter_lot = radians(user2.get('lng'))

        delta_lon = sitter_lot - client_lot if user1_to_user2 else client_lot - sitter_lot
        delta_lat = sitter_lat - client_lat if user1_to_user2 else client_lat - sitter_lat

        a = sin(delta_lat / 2) ** 2 + cos(client_lat) * cos(sitter_lat) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        if unit == 'm':
            return round(distance * 1000)
        elif unit == 'km':
            return round(distance, precision)
    except TypeError:
        return None
