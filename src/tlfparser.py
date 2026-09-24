import logging
from os.path import expanduser
import re

from summary import Summary, BANDS, MODES

def _count_mults(mult_list: list,
        mult1_re: re.Pattern, mult2_re: re.Pattern) -> tuple:

    if not mult1_re and not mult2_re:
        return (len(mult_list), 0)

    mult1 = 0
    mult2 = 0

    for m in mult_list:
        if mult1_re:
            if mult1_re.fullmatch(m):
                mult1 += 1
            else:
                mult2 += 1
        else:
            if mult2_re.fullmatch(m):
                mult2 += 1
            else:
                mult1 += 1

    return (mult1, mult2)


def build_log_summary(logfile: str,
        mult1_re: re.Pattern, mult2_re: re.Pattern) -> dict:

    summaries = {}
    for band in BANDS:
        for mode in MODES:
            summaries[(band,mode)] = Summary()

    lines = []

    try:
        with open(expanduser(logfile), mode='r') as f:
            for line in f.readlines():
                lines.append(line.rstrip())
    except OSError as e:
        logging.error('Unable to read log file: %s', e)
        return None

    for line in lines:
        band = line[0:3].strip()
        mode = line[3:6].strip()
        point = int(line[76:78])
        mult_str = line[68:76]  # FIXME: correct start position
        mult_list = mult_str.strip().split()
        mult1, mult2 = _count_mults(mult_list, mult1_re, mult2_re)

        summaries[(band,mode)].add_qso(point, mult1, mult2)

    return summaries
