import requests


def get_toponym(address, optional_params=None):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}
    try:
        if optional_params:
            for k, v, in optional_params.items():
                geocoder_params[k] = v
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        return json_response['response']["GeoObjectCollection"]["featureMember"][0]['GeoObject']
    except Exception as error:
        print('ERROR: get_toponym-', error)
        return


def get_coordinates(toponym):
    try:
        return ",".join(list(toponym["Point"]["pos"].split()))
    except Exception as error:
        print('ERROR: get_coordinates-', error)
        return


def calculation_spn(toponym):
    try:
        a = list(map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split()))
        b = list(map(float, toponym['boundedBy']['Envelope']['upperCorner'].split()))
        return str(b[0] - a[0]) + ',' + str(b[1] - a[1])
    except Exception as error:
        print('ERROR: calculation_spn-', error)
