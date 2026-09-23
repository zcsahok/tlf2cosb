import argparse
import logging
import time
from datetime import timedelta
import configparser
import re

from contests import Contest, CONTESTS
from summary import Summary, BANDS, MODES
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


def find_contest(name: str) -> Contest:
    name_lower = name.lower()

    contest = None

    # 1. try to find it by long name
    for c in CONTESTS:
        if c.name.lower() == name_lower:
            if contest:
                raise ValueError()
            contest = c

    if contest:
        return contest

    # 2. try to find it by Cabrillo name
    for c in CONTESTS:
        if c.cabrillo_name.lower() == name_lower:
            if contest:
                raise ValueError()
            contest = c

    return contest


CATEGORY_PATTERN = re.compile(r'^SO(?P<band>(AB|\d{2,3}))-(?P<power>(LP|HP|QRP))$')

def parse_category(cat: str) -> dict:
    result = dict()
    if not cat:
        return result

    cat = cat.strip().upper()
    m = CATEGORY_PATTERN.match(cat)
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
                    help='debug logging')
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

settings = None
contest = None

def load_settings(filename: str, contest_name: str) -> None:
    config = configparser.ConfigParser()
    config.read(filename)

    if not config.has_section('User'):
        logging.error(f'File {filename} contains no [User] section')
        raise SystemExit

    global settings
    settings = dict(config['User'].items())

    if config.has_section('Contest'):
        settings.update(dict(config['Contest'].items()))

    if contest_name:
        key = 'Contest-' + contest_name
        if  config.has_section(key):
            settings.update(dict(config[key].items()))
        else:
            logging.info(f'No section [{key}], using settings from [Contest] and [User]')
            settings['name'] = contest_name

    if 'name' not in settings:
        logging.error(f'Could not determine contest name')
        raise SystemExit

    contest_name = settings['name']
    logging.debug(f'{contest_name=}')
    global contest
    try:
        contest = find_contest(contest_name)
    except ValueError:
        logging.error(f'Contest "{contest_name}" is ambiguous')
        raise SystemExit

    if not contest:
        logging.error(f'Contest "{contest_name}" not found')
        raise SystemExit

    logging.info(f'{contest}')

    assisted = 'ASSISTED'
    if not parse_boolean(settings.get('assisted', 'yes')):
        assisted = 'NON-ASSISTED'

    settings['assisted'] = assisted

    category = settings.get('category')
    logging.debug(f'{category=}')

    try:
        settings.update(parse_category(category))
    except ValueError:
        logging.error('Invalid category designator')
        raise SystemExit


def build_total(summaries: dict) -> None:
    total_all = Summary()

    for band in BANDS:
        for mode in MODES:
            k = (band,mode)
            s = summaries[k]
            if s.qsos:
                logging.debug(f'{k}: {s}')
                total_all.add(s)

    summaries[('total','ALL')] = total_all


def compile_mult_patterns(contest: Contest) -> tuple:
    mult1_pattern = None
    if contest.mult1_type:
        mult1_pattern = contest.mult1_pattern

    mult2_pattern = None
    if contest.mult2_type:
        mult2_pattern = contest.mult2_pattern

    if mult1_pattern and mult2_pattern:
        logging.error('Invalid contest definition: both mult patterns must not be set')
        raise SystemExit

    mult1_re = None
    if mult1_pattern:
        mult1_re = re.compile(mult1_pattern)

    mult2_re = None
    if mult2_pattern:
        mult2_re = re.compile(mult2_pattern)

    return (mult1_re, mult2_re)


def main():
    args = process_args()

    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s',
        level=log_level)

    logging.info(f'Loading {args.inifile}')

    load_settings(args.inifile, args.contest)

    global settings
    logging.debug(f'{settings=}')

    try:
        cosb.build_class_data(settings)
    except ValueError:
        raise SystemExit

    if args.logfile:
        logfile = args.logfile
    else:
        logfile = settings['logfile']
    logging.info(f'Log file: {logfile}')

    global contest
    mult1_re, mult2_re = compile_mult_patterns(contest)

    while True:
        summaries = tlfparser.build_log_summary(logfile, mult1_re, mult2_re)
        if not summaries:
            raise SystemExit

        build_total(summaries)

        payload = cosb.build_payload(settings, summaries, contest)

        if args.no_submit:
            logging.info(payload)
            logging.warn('Submission disabled; exiting.')
            raise SystemExit

        logging.debug(payload)
        cosb.submit(settings['call'], settings['password'], payload)

        time.sleep(timedelta(minutes=2).total_seconds())

