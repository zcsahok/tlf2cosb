import argparse
import logging
import time
from datetime import timedelta
import configparser
import re

from summary import Summary, BANDS, MODES
import contests
import tlfparser
import cosb

DEFAULT_INI = 'tlf2cosb.ini'

def parse_boolean(s: str) -> bool:
    s = s.strip().lower()
    if s in {'y', 'yes', 'true'}:
        return True
    if s in {'n', 'no', 'false'}:
        return False
    raise ValueError()


_CATEGORY_PATTERN = re.compile(r'^SO(?P<band>(AB|\d{2,3}))-(?P<power>(LP|HP|QRP))$')

def parse_category(cat: str) -> dict:
    result = {}
    if not cat:
        return result

    cat = cat.strip().upper()
    m = _CATEGORY_PATTERN.match(cat)
    if not m:
        raise ValueError()

    band = m.group('band')
    if band == 'AB':
        band = 'ALL'
    else:
        if band not in BANDS:
            raise ValueError()
        band += 'M'

    result['bands'] = band

    power = m.group('power')
    if power == 'LP':
        power = 'LOW'
    elif power == 'HP':
        power = 'HIGH'

    result['power'] = power

    result['transmitter'] = 'ONE'
    result['ops'] = 'SINGLE-OP'

    return result


def process_args():
    parser = argparse.ArgumentParser(description='TLF to Contest Online Score Board converter')

    parser.add_argument('-d', '--debug', action='store_true',
                    help='debug log level')
    parser.add_argument('-n', '--no-submit', action='store_true',
                    help='do not submit score, just display XML (dry run)')
    parser.add_argument('-c', '--contest', type=str, metavar='CONTEST',
                    help='contest name (default: defined by ini file)')
    parser.add_argument('-l', '--logfile', type=str, metavar='LOGFILE',
                    help='TLF log file (default: defined by ini file)')
    parser.add_argument('-i', '--inifile', type=str, metavar='INIFILE',default=DEFAULT_INI,
                    help=f'configuration file to use (default: {DEFAULT_INI})')

    parsed_args, unparsed_args = parser.parse_known_args()
    if unparsed_args:
        parser.print_help()
        raise SystemExit

    return parsed_args


def load_settings_and_contest(filename: str, contest_name: str) -> tuple:
    config = configparser.ConfigParser()
    config.read(filename)

    if not config.has_section('User'):
        logging.error('File %s contains no [User] section', filename)
        raise SystemExit

    settings = dict(config['User'].items())

    if config.has_section('Contest'):
        settings.update(dict(config['Contest'].items()))

    if contest_name:
        key = 'Contest-' + contest_name
        if  config.has_section(key):
            settings.update(dict(config[key].items()))
        else:
            logging.info('No section [%s], using settings from [Contest] and [User]', key)
            settings['name'] = contest_name

    if 'name' not in settings:
        logging.error('Could not determine contest name')
        raise SystemExit

    contest_name = settings['name']
    logging.debug('contest_name=%s', contest_name)

    try:
        contest = contests.find(contest_name)
    except ValueError:
        logging.error('Contest "%s" is ambiguous', contest_name)
        raise SystemExit

    if not contest:
        logging.error('Contest "%s" not found', contest_name)
        raise SystemExit

    logging.info(contest)

    assisted = 'ASSISTED'
    if not parse_boolean(settings.get('assisted', 'yes')):
        assisted = 'NON-ASSISTED'

    settings['assisted'] = assisted

    category = settings.get('category')
    logging.debug('category=%s', category)

    try:
        settings.update(parse_category(category))
    except ValueError:
        logging.error('Invalid category designator "%s"', category)
        raise SystemExit

    return settings, contest


def build_total(summaries: dict) -> None:
    total_all = Summary()

    for band in BANDS:
        for mode in MODES:
            k = (band,mode)
            s = summaries[k]
            if s.qsos:
                logging.debug('%s: %s', k, s)
                total_all.add(s)

    summaries[('total','ALL')] = total_all


def main():
    args = process_args()

    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s',
        level=log_level)

    logging.info('Loading %s', args.inifile)

    settings, contest = load_settings_and_contest(args.inifile, args.contest)

    logging.debug('settings=%s', settings)

    try:
        cosb.build_class_data(settings)
    except ValueError:
        raise SystemExit

    if args.logfile:
        logfile = args.logfile
    else:
        logfile = settings['logfile']
    logging.info('Log file: %s', logfile)

    try:
        mult1_re, mult2_re = contests.compile_mult_patterns(contest)
    except ValueError:
        raise SystemExit

    while True:
        summaries = tlfparser.build_log_summary(logfile, mult1_re, mult2_re)
        if not summaries:
            raise SystemExit

        build_total(summaries)

        payload = cosb.build_payload(settings, summaries, contest)

        if args.no_submit:
            logging.info(payload)
            logging.warning('Submission disabled; exiting.')
            raise SystemExit

        logging.debug(payload)
        cosb.submit(settings['call'], settings['password'], payload)

        time.sleep(timedelta(minutes=2).total_seconds())
