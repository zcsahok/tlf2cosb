import logging
import xml.etree.ElementTree as ET
import datetime
import requests
from requests.auth import HTTPBasicAuth

from contests import Contest

_CLASS_KEYS = [
    'power', 'assisted', 'transmitter', 'ops', 'bands', 'mode', 'overlay'
]

_URL = 'https://contestonlinescore.com/post/'
_HEADERS = {
    'Content-Type': 'application/xml',
}


def _is_class_key_mandatory(k: str) -> bool:
    return k != 'overlay'


def build_class_data(settings: dict) -> None:
    class_data = dict()
    for k in _CLASS_KEYS:
        if _is_class_key_mandatory(k) and not k in settings:
            logging.error(f'Missing mandatory class key "{k}"')
            raise ValueError

        class_data[k] = settings.get(k, 'n/a').upper()

    logging.info(f'{class_data}')
    settings['class_data'] = class_data


def _map_dig_mode(mode: str, digital_mode: str) -> str:
    if mode == 'DIG' and digital_mode:
        return digital_mode.upper()
    else:
        return mode


def build_payload(settings: dict, summaries: dict, contest: Contest) -> bytes:
    total_all = summaries[('total','ALL')]
    score = total_all.points * total_all.mults()
    logging.info(f'{score=}  {total_all}')

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
            element = ET.SubElement(root, key)
            element.text = str(val)

    ET.SubElement(root, 'class', settings['class_data'])

    # 3. Add band+mode details and totals
    digimode = settings.get('digimode')
    breakdown = ET.SubElement(root, 'breakdown')
    for key, val in summaries.items():
        if val.qsos:
            mode = _map_dig_mode(key[1], digimode)
            band_mode = {'band': key[0], 'mode': mode}
            qso = ET.SubElement(breakdown, 'qso', band_mode)
            qso.text = str(val.qsos)
            point = ET.SubElement(breakdown, 'point', band_mode)
            point.text = str(val.points)
            if contest.mult1_type and val.mult1:
                band_mode.update({'type': contest.mult1_type})
                mult1 = ET.SubElement(breakdown, 'mult', band_mode)
                mult1.text = str(val.mult1)
            if contest.mult2_type and val.mult2:
                band_mode.update({'type': contest.mult2_type})
                mult2 = ET.SubElement(breakdown, 'mult', band_mode)
                mult2.text = str(val.mult2)

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
                logging.debug(f'text: {text}')
            else:
                logging.warning(f'Submitted with error: {text}')

        else:
            logging.error(f'Score submission failed. Status: {response.status_code}, text: {text}')
    except requests.exceptions.RequestException as err:
        logging.error(f'Network error: {err}')
