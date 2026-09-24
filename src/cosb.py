import logging
import xml.etree.ElementTree as ET
import datetime
import requests
from requests.auth import HTTPBasicAuth

from contests import Contest

_CLASS_KEYS = [
    'power', 'assisted', 'transmitter', 'ops', 'bands', 'mode', 'overlay'
]

_CLASS_DATA_KEY = '_class_data'

_URL = 'https://contestonlinescore.com/post/'
_HEADERS = {
    'Content-Type': 'application/xml',
}


def _is_class_key_mandatory(k: str) -> bool:
    return k != 'overlay'


def build_class_data(settings: dict) -> None:
    class_data = {}
    for k in _CLASS_KEYS:
        if _is_class_key_mandatory(k) and not k in settings:
            logging.error('Missing mandatory class key "%s"', k)
            raise ValueError

        class_data[k] = settings.get(k, 'n/a').upper()

    logging.info(class_data)
    settings[_CLASS_DATA_KEY] = class_data


def _add_sub_element(root: ET.Element, name: str,
        attributes: dict, value: object) -> ET.Element:

    element = ET.SubElement(root, name, attributes)
    if value:
        element.text = str(value)

    return element


def _map_dig_mode(mode: str, digital_mode: str) -> str:
    if mode == 'DIG' and digital_mode:
        return digital_mode.upper()

    return mode


def build_payload(settings: dict, summaries: dict, contest: Contest) -> bytes:
    total_all = summaries[('total','ALL')]
    score = total_all.points * total_all.mults()
    logging.info('score=%s  %s', score, total_all)

    # 1. Initialize root node
    root = ET.Element('dynamicresults')

    # 2. Map standard fields and class information
    fields = {
        'contest': contest.cabrillo_name,
        'call': settings['call'].upper(),
        # note: 'ops' is optional + would clash with 'ops' of class data
        'ops': settings.get('operators', '').upper(),
        'score': str(score),
        'soft': 'TLF',
        'version': '1.5',
        'timestamp': datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
    }

    for key, val in fields.items():
        if val:
            _add_sub_element(root, key, {}, val)

    _add_sub_element(root, 'class', settings[_CLASS_DATA_KEY], None)

    # 3. Add band+mode details and totals
    digimode = settings.get('digimode')
    breakdown = ET.SubElement(root, 'breakdown')
    for key, val in summaries.items():
        if val.qsos:
            mode = _map_dig_mode(key[1], digimode)
            band_mode = {'band': key[0], 'mode': mode}
            _add_sub_element(breakdown, 'qso', band_mode, val.qsos)
            _add_sub_element(breakdown, 'point', band_mode, val.points)
            if contest.mult1_type and val.mult1:
                band_mode.update({'type': contest.mult1_type})
                _add_sub_element(breakdown, 'mult', band_mode, val.mult1)
            if contest.mult2_type and val.mult2:
                band_mode.update({'type': contest.mult2_type})
                _add_sub_element(breakdown, 'mult', band_mode, val.mult2)

    # 4. Generate byte string representation
    return ET.tostring(root, encoding='utf-8')


def submit(callsign: str, password: str, xml_data: bytes) -> None:
    try:
        auth = HTTPBasicAuth(callsign, password)
        response = requests.post(_URL, data=xml_data, headers=_HEADERS, auth=auth, timeout=10)
        text = response.text
        if response.status_code == 200:
            if 'OK-Full' in text:
                logging.info('Submitted OK')
                logging.debug('text: %s', text)
            else:
                logging.warning('Submitted with error: %s', text)

        else:
            logging.error('Score submission failed. Status: %s, text: %s',
                response.status_code, text)
    except requests.exceptions.RequestException as err:
        logging.error('Network error: %s', err)
