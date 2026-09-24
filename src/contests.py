"""
contest definitions based on https://contestonlinescore.com/settings/
"""
# pylint: disable=too-many-lines

import logging
import re
from dataclasses import dataclass


@dataclass
class Contest:
    name: str
    cabrillo_name: str
    mult1_type: str = None
    mult1_pattern: str = None
    mult2_type: str = None
    mult2_pattern: str = None


def find(name: str) -> Contest:
    name_lower = name.lower()

    contest = None

    # 1. try to find it by long name
    for c in _CONTESTS:
        if c.name.lower() == name_lower:
            if contest:
                raise ValueError()
            contest = c

    if contest:
        return contest

    # 2. try to find it by Cabrillo name
    for c in _CONTESTS:
        if c.cabrillo_name.lower() == name_lower:
            if contest:
                raise ValueError()
            contest = c

    if contest:
        return contest

    # 3. last resort: look for a substring in either long or Cabrillo name
    for c in _CONTESTS:
        if (name_lower in c.name.lower()
                or name_lower in c.cabrillo_name.lower()):
            if contest:
                raise ValueError()
            contest = c

    return contest


def compile_mult_patterns(contest: Contest) -> tuple:
    mult1_pattern = None
    if contest.mult1_type:
        mult1_pattern = contest.mult1_pattern

    mult2_pattern = None
    if contest.mult2_type:
        mult2_pattern = contest.mult2_pattern

        if not mult1_pattern and not mult2_pattern:
            logging.warning('Two multipliers used, but no patterns defined')

    if mult1_pattern and mult2_pattern:
        logging.error('Invalid contest definition: both mult patterns must not be set')
        raise ValueError()

    mult1_re = None
    if mult1_pattern:
        mult1_re = re.compile(mult1_pattern)

    mult2_re = None
    if mult2_pattern:
        mult2_re = re.compile(mult2_pattern)

    return (mult1_re, mult2_re)


_CONTESTS = [
    Contest(
        name = '10-10 Day Sprint', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Int. Fall CW', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Int. Fall Digital', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Int. Open Season PSK', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Int. Spring CW', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Int. Spring Digital', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Int. Summer SSB', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Int. Winter SSB', cabrillo_name = '10-10',
    ),
    Contest(
        name = '10-10 Weak Signal', cabrillo_name = '10-10',
    ),
    Contest(
        name = '13 Colonies', cabrillo_name = '13-COLONIES',
        mult1_type = 'state', # Colonies
    ),
    Contest(
        name = '144 MHZ-UKAC', cabrillo_name = 'MHZ-UKAC',
    ),
    Contest(
        name = '144 MHz Fall Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # VHF grids
    ),
    Contest(
        name = '144 MHz Spring Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # VHF grids
    ),
    Contest(
        name = '2 de Julho', cabrillo_name = '2 DE JULHO',
        mult1_type = 'state', # Mult
    ),
    Contest(
        name = '222 MHz Fall Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # VHF grids
    ),
    Contest(
        name = '222 MHz Spring Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # VHF grids
    ),
    Contest(
        name = '4 States QRP Group SS Sprint', cabrillo_name = '4STQRP-SSS',
        mult1_type = 'state', # States/Provinces
    ),
    Contest(
        name = '432 MHz Fall Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # VHF grids
    ),
    Contest(
        name = '432 MHz Spring Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # VHF grids
    ),
    Contest(
        name = '50 MHz Spring Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = '50 MHz Sprint', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = '7th Call Area QSO Party', cabrillo_name = '7QP-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'A1 Club AWT', cabrillo_name = 'A1AWT',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'AGB New Year Snowball', cabrillo_name = 'AGB NYSB',
        mult1_type = 'country', # AGB/DXCC/WAE
    ),
    Contest(
        name = 'AGCW German Telegraphy', cabrillo_name = 'DTC',
    ),
    Contest(
        name = 'AGCW NTC QSO PARTY', cabrillo_name = 'AGCW-NTC-QSO-PARTY',
    ),
    Contest(
        name = 'AGCW QRP', cabrillo_name = 'AGCW-QRP',
        mult1_type = 'prefix', # Members
    ),
    Contest(
        name = 'AGCW QRP', cabrillo_name = 'AGCW-QRPC',
    ),
    Contest(
        name = 'AGCW QRP/QRP Party', cabrillo_name = 'AG-CW',
    ),
    Contest(
        name = 'AGCW Straight Key Party 40m', cabrillo_name = 'AG-CW',
    ),
    Contest(
        name = 'AGCW Straight Key Party 80m', cabrillo_name = 'AG-CW',
    ),
    Contest(
        name = 'AGCW VHF/UHF', cabrillo_name = 'AG-CW',
    ),
    Contest(
        name = 'ALARA', cabrillo_name = 'ALARA',
        mult1_type = 'country', # DXCC/Call Area
    ),
    Contest(
        name = 'ALL MIE 33', cabrillo_name = 'ALL-MIE-33',
        mult1_type = 'wpxprefix', # Age
    ),
    Contest(
        name = 'ARAM 50 Mhz', cabrillo_name = 'CONCURSO-50-MHZ',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'ARI 40/80', cabrillo_name = 'ARI-40-80',
        mult1_type = 'state', # Province
    ),
    Contest(
        name = 'ARI International DX', cabrillo_name = 'ARI-DX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # Provinces
    ),
    Contest(
        name = 'ARR BPSK63', cabrillo_name = 'ARR-PSK63',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # CT
    ),
    Contest(
        name = 'ARRL 10 GHz and up', cabrillo_name = 'ARRL-10-GHZ',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'ARRL 10 Meter', cabrillo_name = 'ARRL-10',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # VE/W/XE/ITU
    ),
    Contest(
        name = 'ARRL 160 Meter', cabrillo_name = 'ARRL-160',
        mult1_type = 'state', # ARRL/RAC
        mult2_type = 'country', # DXCC
    ),
    Contest(
        name = 'ARRL 222 MHz and Up', cabrillo_name = 'ARRL-VHF',
    ),
    Contest(
        name = 'ARRL DX CW', cabrillo_name = 'ARRL-DX-CW',
        mult1_type = 'country', # States/Prov./Countries
    ),
    Contest(
        name = 'ARRL DX SSB', cabrillo_name = 'ARRL-DX-SSB',
        mult1_type = 'country', # States/Prov./Countries
    ),
    Contest(
        name = 'ARRL EME', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # Grid
    ),
    Contest(
        name = 'ARRL Field Day', cabrillo_name = 'ARRL-FIELD-DAY',
    ),
    Contest(
        name = 'ARRL Inter. Digital', cabrillo_name = 'ARRL-DIGI',
    ),
    Contest(
        name = 'ARRL January VHF', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'ARRL June VHF', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'ARRL RTTY Roundup', cabrillo_name = 'ARRL-RTTY',
        mult1_type = 'state', # States/Prov.
        mult2_type = 'country', # DXCC
    ),
    Contest(
        name = 'ARRL Rookie Roundup, CW', cabrillo_name = 'ARRL-RR-CW',
        mult1_type = 'state', # States/Prov.
    ),
    Contest(
        name = 'ARRL Rookie Roundup, RTTY', cabrillo_name = 'ARRL-RR-RTTY',
        mult1_type = 'state', # States/Prov.
    ),
    Contest(
        name = 'ARRL Rookie Roundup, SSB', cabrillo_name = 'ARRL-RR-SSB',
        mult1_type = 'state', # States/Provinces/XE call areas
    ),
    Contest(
        name = 'ARRL School Club Roundup', cabrillo_name = 'ARRL-SCR',
        mult1_type = 'state', # St/Pr/DXCC/C/S
    ),
    Contest(
        name = 'ARRL September VHF', cabrillo_name = 'ARRL-VHF',
        mult1_type = 'gridsquare', # VHF Grids
    ),
    Contest(
        name = 'ARRL Sweepstakes CW', cabrillo_name = 'ARRL-SS-CW',
        mult1_type = 'state', # ARRL/RAC
    ),
    Contest(
        name = 'ARRL Sweepstakes SSB', cabrillo_name = 'ARRL-SS-SSB',
        mult1_type = 'state', # ARRL/RAC
    ),
    Contest(
        name = 'ARSI VU DX', cabrillo_name = 'ARSI-VU-DX',
        mult1_type = 'country', # DXCC/VU
    ),
    Contest(
        name = 'Aegean RTTY', cabrillo_name = 'Aegean-RTTY',
    ),
    Contest(
        name = 'Africa FT4 DX', cabrillo_name = 'AFRICA-FT4-DX',
        mult1_type = 'country', # AF DXCC
    ),
    Contest(
        name = 'Alabama QSO Party', cabrillo_name = 'AL-QSO-PARTY',
        mult1_type = 'state', # Count./St./Prov.
    ),
    Contest(
        name = 'All Africa', cabrillo_name = 'SARL-AAF',
        mult1_type = 'country', # AF-DXCC
    ),
    Contest(
        name = 'All Asian DX, CW', cabrillo_name = 'AA-CW',
        mult1_type = 'wpxprefix', # Prefixes/DXCC
    ),
    Contest(
        name = 'All Asian DX, Phone', cabrillo_name = 'AA-SSB',
        mult1_type = 'wpxprefix', # Prefixes/DXCC
    ),
    Contest(
        name = 'All Austrian 160m', cabrillo_name = 'AOEC-160',
        mult1_type = 'country', # WAE
        mult2_type = 'state', # Fed.States
    ),
    Contest(
        name = 'Araucaria WW VHF May', cabrillo_name = 'ARAUCARIA-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'Araucaria WW VHF Oct', cabrillo_name = 'ARAUCARIA-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'Argentina National 7 MHz', cabrillo_name = 'LU-40',
        mult1_type = 'wpxprefix', # First licensed
    ),
    Contest(
        name = 'Arizona QSO Party', cabrillo_name = 'AZ-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Arkansas QSO Party', cabrillo_name = 'AR-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Asia-Pacific Sprint, CW', cabrillo_name = 'AP-Sprint-CW',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'Asia-Pacific Sprint, SSB', cabrillo_name = 'AP-Sprint-SSB',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'Asian Russia Champ', cabrillo_name = 'AS-CHAMP',
    ),
    Contest(
        name = 'Astrakhan Open', cabrillo_name = 'R6U-Champ',
    ),
    Contest(
        name = 'Atlantic Canada QSO Party', cabrillo_name = 'AC-QSO-PARTY',
        mult1_type = 'state', # State/Prov/County
    ),
    Contest(
        name = 'Australia Day', cabrillo_name = 'WIA-AUSTRALIA DAY',
    ),
    Contest(
        name = 'BARTG HF RTTY', cabrillo_name = 'BARTG-RTTY',
        mult1_type = 'country', # DXCC/Areas
        mult2_type = 'zone', # Conts
    ),
    Contest(
        name = 'BARTG RTTY Sprint', cabrillo_name = 'BARTG-SPRINT',
        mult1_type = 'country', # DXCC/Areas
        mult2_type = 'zone', # Conts
    ),
    Contest(
        name = 'BARTG Sprint 75', cabrillo_name = 'BARTG-SPRINT',
        mult1_type = 'country', # DXCC/Areas
        mult2_type = 'zone', # Conts
    ),
    Contest(
        name = 'BARTG Sprint PSK63', cabrillo_name = 'BARTG-PSK63',
        mult1_type = 'country', # DXCC/Call Area
    ),
    Contest(
        name = 'BBK', cabrillo_name = 'BBK-CONTEST',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'BCC QSO Party', cabrillo_name = 'BCC-QSO-Party',
        mult1_type = 'prefix', # T-shirt
    ),
    Contest(
        name = 'BRASÍLIA', cabrillo_name = 'CBSB',
        mult1_type = 'state', # UF
    ),
    Contest(
        name = 'BSB VHF', cabrillo_name = 'BSBVHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'Balkan HF', cabrillo_name = 'BALKAN-HF',
        mult1_type = 'prefix', # Prefixes
    ),
    Contest(
        name = 'Baltic', cabrillo_name = 'BALTIC-CONTEST',
    ),
    Contest(
        name = 'Batalha Naval do Riachuelo', cabrillo_name = 'CBNR',
        mult1_type = 'state', # UF
    ),
    Contest(
        name = 'Batalha do Jenipapo', cabrillo_name = 'CBJ-DX',
        mult1_type = 'state', # UF
    ),
    Contest(
        name = 'Battle of Carabobo International', cabrillo_name = 'YVBC-SSB',
        mult1_type = 'state', # YV state
    ),
    Contest(
        name = 'Bitwa Warszawska', cabrillo_name = 'DOWOLNE-GR',
    ),
    Contest(
        name = 'Black Sea Cup International', cabrillo_name = 'BSCI-HF',
        mult1_type = 'country', # Zones/Countries/BSC
    ),
    Contest(
        name = 'Bogor Old and New', cabrillo_name = 'Bogor Old and New Contest',
        mult1_type = 'prefix', # Prefixes
    ),
    Contest(
        name = 'Brasil VHF', cabrillo_name = 'BRASILVHF',
        mult1_type = 'gridsquare', # Grid
    ),
    Contest(
        name = 'British Columbia QSO Party', cabrillo_name = 'BC-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Bucharest Digital', cabrillo_name = 'BUCURESTI',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # Buch. Sector
    ),
    Contest(
        name = 'CNCW', cabrillo_name = 'CNCW',
        mult1_type = 'state', # EA
    ),
    Contest(
        name = 'CONCURSO QRS-10', cabrillo_name = 'LABRE SP QRS10',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # PY
    ),
    Contest(
        name = 'COVID-19', cabrillo_name = 'COVID-19-STAYHOME',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # Stayhome
    ),
    Contest(
        name = 'CQ 160-Meter, CW', cabrillo_name = 'CQ-160-CW',
        mult1_type = 'country', # DXCC/WAE
        mult2_type = 'state', # States/Prov.
    ),
    Contest(
        name = 'CQ 160-Meter, SSB', cabrillo_name = 'CQ-160-SSB',
        mult1_type = 'country', # DXCC/WAE
        mult2_type = 'state', # States/Prov.
    ),
    Contest(
        name = 'CQ Bande Basse Italia', cabrillo_name = 'CQBBI',
        mult1_type = 'state', # Province
        mult2_type = 'prefix', # MDXC
    ),
    Contest(
        name = 'CQ RJ RTTY DX', cabrillo_name = 'CQRJRTTY-DX',
        mult1_type = 'state', # PY
        mult2_type = 'country', # DXCC
    ),
    Contest(
        name = 'CQ RJ VHF', cabrillo_name = 'CQRJVHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'CQ Vojvodina', cabrillo_name = 'CQV-SRB',
        mult1_type = 'state', # WAS
    ),
    Contest(
        name = 'CQ WPX CW', cabrillo_name = 'CQ-WPX-CW',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'CQ WPX RTTY', cabrillo_name = 'CQ-WPX-RTTY',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'CQ WPX SSB', cabrillo_name = 'CQ-WPX-SSB',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'CQ WW CW', cabrillo_name = 'CQ-WW-CW',
        mult1_type = 'country', # Countries
        mult2_type = 'zone', # Zones
    ),
    Contest(
        name = 'CQ WW RTTY', cabrillo_name = 'CQ-WW-RTTY',
        mult1_type = 'country', # DXCC+S/P
        mult2_type = 'zone', # Zones
    ),
    Contest(
        name = 'CQ WW SSB', cabrillo_name = 'CQ-WW-SSB',
        mult1_type = 'country', # Countries
        mult2_type = 'zone', # Zones
    ),
    Contest(
        name = 'CQ WW VHF DIGI', cabrillo_name = 'CQ-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'CQ WW VHF SSB/CW/FM', cabrillo_name = 'CQ-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'CQ World Scout', cabrillo_name = 'CQWS',
        mult1_type = 'prefix', # Mult
    ),
    Contest(
        name = 'CQ World Scout HF', cabrillo_name = 'CQWS_HF',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'CQ-M International DX', cabrillo_name = 'CQ-M',
        mult1_type = 'country', # R-150-S
    ),
    Contest(
        name = 'CQMM DX', cabrillo_name = 'CQMMDX',
        mult1_type = 'country', # DXCC
        mult2_type = 'wpxprefix', # SA Prefixes
    ),
    Contest(
        name = 'CVA DX CW', cabrillo_name = 'CVA-DX-CW',
        mult1_type = 'state', # Federal Units
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'CVA DX SSB', cabrillo_name = 'CVA-DX-SSB',
        mult1_type = 'state', # Federal Units
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'CWOps Open 1 (00-04z)', cabrillo_name = 'CW-OPEN',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'CWOps Open 2 (12-16z)', cabrillo_name = 'CW-OPEN',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'CWOps Open 3 (20-24z)', cabrillo_name = 'CW-OPEN',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'CWops Mini-CWT 1', cabrillo_name = 'CW-Ops',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'CWops Mini-CWT 2', cabrillo_name = 'CW-Ops',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'CWops Mini-CWT 3', cabrillo_name = 'CW-Ops',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'CWops Mini-CWT 4', cabrillo_name = 'CW-Ops',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'California QSO Party', cabrillo_name = 'CA-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Canadian Prairies QSO Party', cabrillo_name = 'CP-QSO-PARTY',
        mult1_type = 'state', # States/Provinces/Dist
    ),
    Contest(
        name = 'Carpathian CUP 1', cabrillo_name = 'KARPATY-CUP',
    ),
    Contest(
        name = 'Carpathian CUP 2', cabrillo_name = 'KARPATY-CUP',
    ),
    Contest(
        name = 'Carpathian SPRINT Autumn', cabrillo_name = 'CARPATHIAN',
    ),
    Contest(
        name = 'Carpathian SPRINT Spring', cabrillo_name = 'CARPATHIAN',
    ),
    Contest(
        name = 'Carpathian SPRINT Summer', cabrillo_name = 'CARPATHIAN',
    ),
    Contest(
        name = 'Carpathian SPRINT Winter', cabrillo_name = 'CARPATHIAN',
    ),
    Contest(
        name = 'Central Federal District Champ', cabrillo_name = 'CFO-CHAMP',
    ),
    Contest(
        name = 'Collegiate-QSO-Party', cabrillo_name = 'Collegiate-QSO-Party',
        mult1_type = 'state', # Shool/State/Prov/DX
    ),
    Contest(
        name = 'Colorado QSO Party', cabrillo_name = 'CO-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Concurso Farroupilha HF', cabrillo_name = 'Concurso-Farroupilha-HF',
        mult1_type = 'state', # Estados
    ),
    Contest(
        name = 'Concurso Farroupilha VHF', cabrillo_name = 'Concurso-Farroupilha-VHF',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'Concurso Municipios Españoles', cabrillo_name = 'CME',
        mult1_type = 'state', # Mun/HQ
    ),
    Contest(
        name = 'Croatian Amateur Radio CUP', cabrillo_name = 'HRK',
        mult1_type = 'prefix', # Prec
    ),
    Contest(
        name = 'Croatian DX', cabrillo_name = '9A-DX',
        mult1_type = 'country', # DXCC/WAE
    ),
    Contest(
        name = 'DARC 10-Meter', cabrillo_name = 'DARC-10M',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # DOKs
    ),
    Contest(
        name = 'DARC Easter', cabrillo_name = 'EASTER-CONTEST',
        mult1_type = 'state', # DOK
        mult2_type = 'prefix', # Prefixes
    ),
    Contest(
        name = 'DARC FT4', cabrillo_name = 'DARC-FT4',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'DARC XMAS', cabrillo_name = 'XMAS',
        mult1_type = 'state', # DOK
        mult2_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'DIG QSO Party', cabrillo_name = 'DIG-CW',
        mult1_type = 'country', # Country
        mult2_type = 'prefix', # DIG
    ),
    Contest(
        name = 'DL-DX RTTY', cabrillo_name = 'DL-DX-RTTY',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'DMC RTTY', cabrillo_name = 'DMC-RTTY',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'Day of the YLs', cabrillo_name = 'DAY-OF-YLS',
    ),
    Contest(
        name = 'Delaware QSO Party', cabrillo_name = 'DE-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Dutch Kingdom', cabrillo_name = 'DKC',
        mult1_type = 'country', # DXCC/PA
    ),
    Contest(
        name = 'Dutch PACC', cabrillo_name = 'PACC',
        mult1_type = 'state', # PA Provinces
    ),
    Contest(
        name = 'Dutch PACC Digi', cabrillo_name = 'PACCDIGI',
        mult1_type = 'state', # DXCC/Call Area/PA Grid
    ),
    Contest(
        name = 'EA PSK63', cabrillo_name = 'EA-PSK',
        mult1_type = 'state', # EADX/Provinces/Entities
    ),
    Contest(
        name = 'EA RTTY', cabrillo_name = 'EA-RTTY',
        mult1_type = 'state', # EA/W/VK/VE/JA
    ),
    Contest(
        name = 'EPC Ukraine DX', cabrillo_name = 'EPC-UKR-DX',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Oblasts
    ),
    Contest(
        name = 'ES Open HF Championship', cabrillo_name = 'ES-OPEN-HF',
        mult1_type = 'state', # ES Regions
    ),
    Contest(
        name = 'EU DX', cabrillo_name = 'EUDXC',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # EU Regions
    ),
    Contest(
        name = 'EUCW 160m', cabrillo_name = 'EUCW-160',
        mult1_type = 'state', # EUCW
    ),
    Contest(
        name = 'EURASIA HF', cabrillo_name = 'EURASIA-CHAMP',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'Esenin Russia', cabrillo_name = 'R3S-ER',
        mult1_type = 'state', # RR/DXCC
    ),
    Contest(
        name = 'European HF Championship', cabrillo_name = 'EUHFC',
        mult1_type = 'state', # First licensed
    ),
    Contest(
        name = 'European PSK DX', cabrillo_name = 'EU-PSK-DX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # EU
    ),
    Contest(
        name = 'F9AA Cup CW', cabrillo_name = 'F9AA-CUP',
        mult1_type = 'country', # Club/LB/DXCC
    ),
    Contest(
        name = 'FL State Parks on the Air', cabrillo_name = 'FL-SPOTA',
        mult1_type = 'state', # Parks/Stations
    ),
    Contest(
        name = 'FOC 80th Anniversary Challenge', cabrillo_name = 'FOC-80-ANIVERSARY',
    ),
    Contest(
        name = 'FOC Marathon', cabrillo_name = 'FOC',
    ),
    Contest(
        name = 'FOC Old School Classic', cabrillo_name = 'FOC',
    ),
    Contest(
        name = 'FOC QSO Party March', cabrillo_name = 'FOC',
        mult1_type = 'state', # FOC members
    ),
    Contest(
        name = 'FOC QSO Party September', cabrillo_name = 'FOC',
        mult1_type = 'state', # FOC members
    ),
    Contest(
        name = 'FOC Silent Key Memorial', cabrillo_name = 'SKMC',
        mult1_type = 'prefix', # SK
    ),
    Contest(
        name = 'FRAPR 10M', cabrillo_name = 'FRAPR-10M',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # FRAP
    ),
    Contest(
        name = 'FT Challenge', cabrillo_name = 'FT-CHALLENGE',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'FT8 DX', cabrillo_name = 'ARRL-RTTY',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # States/Prov.
    ),
    Contest(
        name = 'Falcons', cabrillo_name = 'Falcons',
        mult1_type = 'country', # Mult
    ),
    Contest(
        name = 'Florida QSO Party', cabrillo_name = 'FL-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'GACW WWSA CW DX', cabrillo_name = 'GACW',
        mult1_type = 'country', # DXCC
        mult2_type = 'zone', # CQ zones
    ),
    Contest(
        name = 'Gedebage CW', cabrillo_name = 'GDBAGE-DX-TEST',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # Prefix
    ),
    Contest(
        name = 'Georgia QSO Party', cabrillo_name = 'GA-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'German districts HSW', cabrillo_name = 'DARC-HSW',
        mult1_type = 'state', # DOK/NM
    ),
    Contest(
        name = 'Gunung Jati DX', cabrillo_name = 'GUNUNG-JATI',
        mult1_type = 'country', # DXCC
        mult2_type = 'wpxprefix', # Prefix
    ),
    Contest(
        name = 'HA3NS Sprint Memorial', cabrillo_name = 'HA3NS-MEMORIAL',
    ),
    Contest(
        name = 'HAM SPIRIT', cabrillo_name = 'HAM-SPIRIT',
        mult1_type = 'zone', # ITU/QTH
    ),
    Contest(
        name = 'HF KUP- RRS', cabrillo_name = 'HF-KUP-SRRS',
    ),
    Contest(
        name = 'HM The King of Spain, CW', cabrillo_name = 'KING-OF-SPAIN-CW',
        mult1_type = 'state', # EA/DXCC/Ent.
    ),
    Contest(
        name = 'HM The King of Spain, SSB', cabrillo_name = 'KING-OF-SPAIN-SSB',
        mult1_type = 'state', # EA/DXCC/Ent.
    ),
    Contest(
        name = 'Hamcation QSO Party', cabrillo_name = 'HAMCATION-QSO-PARTY',
    ),
    Contest(
        name = 'Hamvention QSO Party', cabrillo_name = 'HAMVENTION-QP',
    ),
    Contest(
        name = 'Hawaii QSO Party', cabrillo_name = 'HI-QSO-PARTY',
        mult1_type = 'state', # St./Prov./Hw.Mult
    ),
    Contest(
        name = 'Helvetia', cabrillo_name = 'HELVETIA',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # HB cantons
    ),
    Contest(
        name = 'High Speed Club CW', cabrillo_name = 'HSC-CW',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'High Speed Club CW', cabrillo_name = 'HSC-CW',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'Hiram Percy Maxim 150', cabrillo_name = 'HPM150',
        mult1_type = 'state', # ARRL/RAC
    ),
    Contest(
        name = 'Holyland DX', cabrillo_name = 'HOLYLAND-DX',
        mult1_type = 'state', # 4X Areas
    ),
    Contest(
        name = 'Hungarian DX', cabrillo_name = 'HA-DX',
        mult1_type = 'state', # HA Counties/Members
    ),
    Contest(
        name = 'IARU HF World Champ', cabrillo_name = 'IARU-HF',
        mult1_type = 'zone', # Zones
        mult2_type = 'state', # HQ
    ),
    Contest(
        name = 'IARU Region 1 145 Mhz', cabrillo_name = 'VHF-REG-1',
    ),
    Contest(
        name = 'IARU Region 1 50 Mhz', cabrillo_name = 'VHF-REG-1',
    ),
    Contest(
        name = 'IARU Region 1 70 Mhz', cabrillo_name = 'VHF-REG-1',
    ),
    Contest(
        name = 'IARU Region 1 Field Day, CW', cabrillo_name = 'FIELDDAY-REGION-1',
        mult1_type = 'country', # DXCC/WAE
    ),
    Contest(
        name = 'IARU Region 1 Field Day, SSB', cabrillo_name = 'FIELDDAY-REGION-1',
        mult1_type = 'country', # DXCC/WAE
    ),
    Contest(
        name = 'ICWC-MST 1', cabrillo_name = 'ICWC-MST',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'ICWC-MST 2', cabrillo_name = 'ICWC-MST',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'ICWC-MST 3', cabrillo_name = 'ICWC-MST',
        mult1_type = 'state', # Unique Calls
    ),
    Contest(
        name = 'IG-RY WW RTTY', cabrillo_name = 'IG-WW-RY',
        mult1_type = 'prefix', # Prec
    ),
    Contest(
        name = 'IN7QPNE', cabrillo_name = 'IN7QPNE-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'IOC', cabrillo_name = 'IOC',
        mult1_type = 'gridsquare', # Grid
    ),
    Contest(
        name = 'IPARC CW', cabrillo_name = 'IPARC-CONTEST',
        mult1_type = 'country', # DXCC+IPA
    ),
    Contest(
        name = 'IPARC SSB', cabrillo_name = 'IPARC-CONTEST',
        mult1_type = 'country', # DXCC+IPA
    ),
    Contest(
        name = 'IRTS 80m Counties', cabrillo_name = 'IRTS80M',
        mult1_type = 'state', # EI/GI
        mult2_type = 'country', # DXCC
    ),
    Contest(
        name = 'Idaho QSO Party', cabrillo_name = 'ID-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Illinois QSO Party', cabrillo_name = 'IL-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Indiana QSO Party', cabrillo_name = 'IN-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'International Naval', cabrillo_name = 'NAVAL',
        mult1_type = 'wpxprefix', # Naval Club Members
    ),
    Contest(
        name = 'Iowa QSO Party', cabrillo_name = 'IA-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Italia 28 Mhz', cabrillo_name = 'MDXC10',
        mult1_type = 'state', # Provinces
        mult2_type = 'prefix', # MDXC
    ),
    Contest(
        name = 'JAKARTA', cabrillo_name = 'JAKARTA CONTEST',
        mult1_type = 'country', # DXCC
        mult2_type = 'wpxprefix', # Prefix
    ),
    Contest(
        name = 'JARTS WW RTTY', cabrillo_name = 'JARTS-WW-RTTY',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # Call Areas
    ),
    Contest(
        name = 'JIDX CW', cabrillo_name = 'JIDX-CW',
        mult1_type = 'country', # DXCC/Zones/Pref.
    ),
    Contest(
        name = 'JIDX Phone', cabrillo_name = 'JIDX-SSB',
        mult1_type = 'country', # DXCC/Zones/Pref.
    ),
    Contest(
        name = 'Jakarta RTTY', cabrillo_name = 'Jakarta RTTY Test',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # Prefix
    ),
    Contest(
        name = 'K1USN Slow Speed Fri', cabrillo_name = 'K1USNSST',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # St./Provs
    ),
    Contest(
        name = 'K1USN Slow Speed Mon', cabrillo_name = 'K1USNSST',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # St/Provs
    ),
    Contest(
        name = 'K1USN Slow Speed Open', cabrillo_name = 'K1USNSST-OPEN',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # St./Provs
    ),
    Contest(
        name = 'KALBAR DX', cabrillo_name = 'KALBAR CONTEST',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # Prefix
    ),
    Contest(
        name = 'KT SCWC', cabrillo_name = 'KT-SCWC',
        mult1_type = 'prefix', # SCWC
    ),
    Contest(
        name = 'KV Prvenstvo ZRS', cabrillo_name = 'KVP',
        mult1_type = 'state', # Prec
    ),
    Contest(
        name = 'Kansas QSO PARTY', cabrillo_name = 'KS-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Kawanua DX', cabrillo_name = 'KAWANUA-DX',
        mult1_type = 'prefix', # Prefixes
    ),
    Contest(
        name = 'Kentucky QSO Party', cabrillo_name = 'KY-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Keyman\'s Club of Japan', cabrillo_name = 'KCJ',
        mult1_type = 'state', # JA/Zones
    ),
    Contest(
        name = 'LABRE DX', cabrillo_name = 'LABRE-DX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # PY State
    ),
    Contest(
        name = 'LABRE RS DIGI', cabrillo_name = 'LABRE-RS-DIGI',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'LY Champ', cabrillo_name = 'LY-TBC',
        mult1_type = 'state', # Mult
    ),
    Contest(
        name = 'LZ DX Contest', cabrillo_name = 'LZ-DX',
        mult1_type = 'state', # LZ dist.
        mult2_type = '', # IARU
    ),
    Contest(
        name = 'LZ Open 40m Sprint', cabrillo_name = 'LZ-OPEN',
    ),
    Contest(
        name = 'Lithuanian CUP', cabrillo_name = 'LY-Cup',
        mult1_type = 'prefix', # LY19
    ),
    Contest(
        name = 'Louisiana QSO Party', cabrillo_name = 'LA-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'MARAC US Counties QSO Party', cabrillo_name = 'MARAC-QSO-PARTY',
        mult1_type = 'state', # US county
    ),
    Contest(
        name = 'MINITEST', cabrillo_name = 'Mini-Test-CW',
        mult1_type = 'wpxprefix', # Unique calls
    ),
    Contest(
        name = 'Maidenhead Mayhem', cabrillo_name = 'MAIDENHEAD-MAYHEM',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'Maidenhead Mayhem Sprint', cabrillo_name = 'MAIDENHEAD-MAYHEM',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'Maine QSO Party', cabrillo_name = 'ME-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Makrothen RTTY', cabrillo_name = 'MAKROTHEN-RTTY',
    ),
    Contest(
        name = 'Malaysia DX Contest', cabrillo_name = 'MYDX-SSB-CONTEST',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # 9M
    ),
    Contest(
        name = 'Maratona QRS 10M CW', cabrillo_name = 'Maratona QRS10 CW DX',
        mult1_type = 'country', # Mult
    ),
    Contest(
        name = 'Maratona QRS 10M CW', cabrillo_name = 'Maratona QRS10 CW',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # PY
    ),
    Contest(
        name = 'Marconi Club QSO Party', cabrillo_name = 'MCD-QSO-PARTY',
        mult1_type = 'state', # Marconi Club
    ),
    Contest(
        name = 'Marconi Club SCW QSO Party', cabrillo_name = 'MCD-QSO-PARTY',
        mult1_type = 'state', # Marconi Club
    ),
    Contest(
        name = 'Marconi Memorial HF CW', cabrillo_name = 'MARCONIMEMORIAL',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'Marechal Rondon', cabrillo_name = 'MarechalRondon',
        mult1_type = 'country', # Mult
    ),
    Contest(
        name = 'Maryland-DC QSO Party', cabrillo_name = 'MD-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Mexico RTTY', cabrillo_name = 'XE-RTTY',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # XE States
    ),
    Contest(
        name = 'Michigan QSO Party', cabrillo_name = 'MI-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Minnesota QSO Party', cabrillo_name = 'MN-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Mississippi QSO Party', cabrillo_name = 'MS-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Missouri QSO Party', cabrillo_name = 'MO-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'NA Collegiate Champ RTTY', cabrillo_name = 'NACC-RTTY',
        mult1_type = '', # State/Prov/NA
    ),
    Contest(
        name = 'NA Collegiate Champ SSB', cabrillo_name = 'NACC-SSB',
        mult1_type = 'state', # State/Prov/NA
    ),
    Contest(
        name = 'NA MS sprint', cabrillo_name = 'VHF-NAMSS',
    ),
    Contest(
        name = 'NAQP CW', cabrillo_name = 'NAQP-CW',
        mult1_type = 'state', # States/Provinces/NA
    ),
    Contest(
        name = 'NAQP RTTY', cabrillo_name = 'NAQP-RTTY',
        mult1_type = 'state', # States/Provinces/NA
    ),
    Contest(
        name = 'NAQP SSB', cabrillo_name = 'NAQP-SSB',
        mult1_type = 'state', # States/Provinces/NA
    ),
    Contest(
        name = 'NCCC 55th Anniversary Fiesta', cabrillo_name = 'NCCC-FIESTA',
    ),
    Contest(
        name = 'NCCC FT4 Sprint', cabrillo_name = 'NCCC-FT4-SPRINT',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'NCCC NA CW Sprint', cabrillo_name = 'NCCC-SPRINT-CW',
        mult1_type = 'state', # States/Provinces
    ),
    Contest(
        name = 'NCCC NA RTTY Sprint', cabrillo_name = 'NCCC-SPRINT-RTTY',
        mult1_type = 'state', # States/Provinces
    ),
    Contest(
        name = 'NJQRP Skeeter Hunt', cabrillo_name = 'SKEETER-HUNT',
        mult1_type = 'country', # Stae/Prov/DXCC
    ),
    Contest(
        name = 'NRAU 28MHz', cabrillo_name = 'NRAU-10M',
    ),
    Contest(
        name = 'NRAU NAC 1296 Mhz', cabrillo_name = 'NAC',
    ),
    Contest(
        name = 'NRAU NAC 144 Mhz', cabrillo_name = 'NAC',
    ),
    Contest(
        name = 'NRAU NAC 432 MHz', cabrillo_name = 'NAC',
    ),
    Contest(
        name = 'NRAU NAC 50 Mhz', cabrillo_name = 'NAC',
    ),
    Contest(
        name = 'NRAU NAC 70 Mhz', cabrillo_name = 'NAC',
    ),
    Contest(
        name = 'NRAU-Baltic, CW', cabrillo_name = 'NRAU-CW',
        mult1_type = 'state', # Region
    ),
    Contest(
        name = 'NRAU-Baltic, SSB', cabrillo_name = 'NRAU-SSB',
        mult1_type = 'state', # Region
    ),
    Contest(
        name = 'NRRL Field Day', cabrillo_name = 'NRRL-FIELDDAY',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'NRRL Fylkes', cabrillo_name = 'NRRLFYLKE',
        mult1_type = 'state', # Fylkes
    ),
    Contest(
        name = 'NRRL Telefoni', cabrillo_name = 'TELEFONITEST',
        mult1_type = 'state', # District
    ),
    Contest(
        name = 'NRRL Vintertest', cabrillo_name = 'NRRLVINTER',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'NSARA', cabrillo_name = 'NSARA',
        mult1_type = 'state', # NS Counties
    ),
    Contest(
        name = 'NZART Sangster Shield (Sat)', cabrillo_name = 'NZART',
        mult1_type = 'state', # ZL branches
    ),
    Contest(
        name = 'NZART Sangster Shield (Sun)', cabrillo_name = 'NZART',
        mult1_type = 'state', # ZL branches
    ),
    Contest(
        name = 'Nacional de Fonia', cabrillo_name = 'NACIONAL-FONIA',
        mult1_type = 'state', # Provincias
    ),
    Contest(
        name = 'Nebraska QSO Party', cabrillo_name = 'NE-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Nevada QSO Party', cabrillo_name = 'NV-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'New England QSO Party', cabrillo_name = 'NEWE-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'New Hampshire QSO Party', cabrillo_name = 'NH-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'New Jersey QSO Party', cabrillo_name = 'NJ-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'New Mexico QSO Party', cabrillo_name = 'NM-QSO-PARTY',
        mult1_type = 'country', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'New York QSO Party', cabrillo_name = 'NY-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'North American Sprint, CW', cabrillo_name = 'NA-SPRINT-CW',
        mult1_type = 'state', # States/Provinces
    ),
    Contest(
        name = 'North American Sprint, RTTY', cabrillo_name = 'NA-SPRINT-RTTY',
        mult1_type = 'state', # States/Provinces
    ),
    Contest(
        name = 'North American Sprint, SSB', cabrillo_name = 'NA-SPRINT-SSB',
        mult1_type = 'state', # States/Provinces
    ),
    Contest(
        name = 'North Carolina QSO Party', cabrillo_name = 'NC-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'North Dakota QSO Party', cabrillo_name = 'ND-QSO-PARTY',
        mult1_type = 'country', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'OK DX RTTY', cabrillo_name = 'OK-DX-RTTY',
        mult1_type = 'country', # Countries/OK
    ),
    Contest(
        name = 'OK-OM DX CW', cabrillo_name = 'OK-OM-DX',
        mult1_type = 'state', # Districts/Prefix
    ),
    Contest(
        name = 'OK-OM DX SSB', cabrillo_name = 'OK-OM-DX',
        mult1_type = 'country', # Country
        mult2_type = 'state', # OK/OM
    ),
    Contest(
        name = 'OK1WC Memorial (MWC)', cabrillo_name = 'OK1WC',
        mult1_type = 'wpxprefix', # Suffix Letter
    ),
    Contest(
        name = 'Oceania DX, CW', cabrillo_name = 'Oceania-DX-CW',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'Oceania DX, Phone', cabrillo_name = 'Oceania-DX-SSB',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'Ohio QSO PARTY', cabrillo_name = 'OH-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Oklahoma QSO Party', cabrillo_name = 'OK-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Old New Year', cabrillo_name = 'RADIO-ONY',
    ),
    Contest(
        name = 'Ontario QSO Party', cabrillo_name = 'ON-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Original QRP', cabrillo_name = 'OQRP',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'PA Beker, CW', cabrillo_name = 'PABEKER-CW',
        mult1_type = 'state', # Sect
    ),
    Contest(
        name = 'PA Beker, SSB', cabrillo_name = 'PABEKER-SSB',
        mult1_type = 'state', # Sect
    ),
    Contest(
        name = 'PGA TEST', cabrillo_name = 'PGA-TEST',
    ),
    Contest(
        name = 'PRO CW Contest', cabrillo_name = 'TAC',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'PRO Digi Contest', cabrillo_name = 'PDC',
        mult1_type = 'prefix', # Prefixes
    ),
    Contest(
        name = 'PVRC Reunion 1', cabrillo_name = 'PVRC',
    ),
    Contest(
        name = 'PVRC Reunion 2', cabrillo_name = 'PVRC',
    ),
    Contest(
        name = 'PVRC Reunion 3', cabrillo_name = 'PVRC',
    ),
    Contest(
        name = 'Pajajaran Bogor DX', cabrillo_name = 'PBDX-CONTEST',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # YB
    ),
    Contest(
        name = 'Pennsylvania QSO Party', cabrillo_name = 'PA-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Poisson d\'Avril', cabrillo_name = 'PDAC',
        mult1_type = 'wpxprefix', # les Poissons
    ),
    Contest(
        name = 'Portugal Day', cabrillo_name = 'Portugal',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # CT Region
    ),
    Contest(
        name = 'Portuguese Navy Day', cabrillo_name = 'CDM',
        mult1_type = 'state', # NRA members
    ),
    Contest(
        name = 'QRP FOX HUNT 40M Tuesday', cabrillo_name = 'QRP-FOX-HUNT',
    ),
    Contest(
        name = 'QRP FOX HUNT 80M Thursday', cabrillo_name = 'QRP-FOX-HUNT',
    ),
    Contest(
        name = 'Quebec QSO Party', cabrillo_name = 'QC-QSO-PARTY',
        mult1_type = 'state', # State/Prov//Reg/DXCC
    ),
    Contest(
        name = 'R3L CHAMP', cabrillo_name = 'R3L-CH-MIX',
        mult1_type = 'prefix', # R3L
    ),
    Contest(
        name = 'R4W Champ Open', cabrillo_name = 'R4W-CHAMP',
        mult1_type = 'gridsquare', # RDA/Grid
    ),
    Contest(
        name = 'R9S Champ', cabrillo_name = 'R9S-CHAMP',
        mult1_type = 'state', # RDA/QTH
    ),
    Contest(
        name = 'RAC Canada Day', cabrillo_name = 'RAC',
        mult1_type = 'state', # VE Prov./Terr.
    ),
    Contest(
        name = 'RAC Winter', cabrillo_name = 'RAC',
        mult1_type = 'state', # Provinces
    ),
    Contest(
        name = 'RAEM', cabrillo_name = 'RAEM',
    ),
    Contest(
        name = 'RCA Transatlantic', cabrillo_name = 'RCA-TQP',
    ),
    Contest(
        name = 'RCC CUP', cabrillo_name = 'RCC-CUP',
        mult1_type = 'country', # Members/Zones
    ),
    Contest(
        name = 'RCWC 4 Seasons (Winter)', cabrillo_name = 'RCWC-4-SEASONS',
    ),
    Contest(
        name = 'RDA', cabrillo_name = 'RDAC',
        mult1_type = 'state', # RDA
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'REF 160', cabrillo_name = 'REF-160',
        mult1_type = 'state', # Departments
    ),
    Contest(
        name = 'REF CW', cabrillo_name = 'REF',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Departments
    ),
    Contest(
        name = 'REF DDFM 6m', cabrillo_name = 'DDFM50',
        mult1_type = 'gridsquare', # F grid
        mult2_type = 'state', # F dept
    ),
    Contest(
        name = 'REF SSB', cabrillo_name = 'REF',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Departments
    ),
    Contest(
        name = 'RF Champ CW', cabrillo_name = 'RF-Champ-CW',
    ),
    Contest(
        name = 'RF HF CUP CW', cabrillo_name = 'RFC-CW',
        mult1_type = 'state', # QTH Locators
    ),
    Contest(
        name = 'RF HF CUP SSB', cabrillo_name = 'RFC-SSB',
        mult1_type = 'state', # QTH Locators
    ),
    Contest(
        name = 'RRTC', cabrillo_name = 'RRTC',
        mult1_type = 'zone', # ITU zones
    ),
    Contest(
        name = 'RSGB 1st 1.8 MHz, CW', cabrillo_name = 'RSGB-160',
    ),
    Contest(
        name = 'RSGB 2nd 1.8 MHz, CW', cabrillo_name = 'RSGB-160',
    ),
    Contest(
        name = 'RSGB 80M Autumn, SSB', cabrillo_name = 'RSGB-80M-CC',
    ),
    Contest(
        name = 'RSGB 80M CC CW', cabrillo_name = 'RSGB-80M-CC',
    ),
    Contest(
        name = 'RSGB 80M CC Data', cabrillo_name = 'RSGB-80M-CC',
    ),
    Contest(
        name = 'RSGB 80M CC SSB', cabrillo_name = 'RSGB-80M-CC',
    ),
    Contest(
        name = 'RSGB 80m Autumn, CW', cabrillo_name = 'RSGB-80M-CC',
    ),
    Contest(
        name = 'RSGB 80m Autumn, Data', cabrillo_name = 'RSGB-80M-CC',
    ),
    Contest(
        name = 'RSGB AFS, CW', cabrillo_name = 'RSGB-AFS',
    ),
    Contest(
        name = 'RSGB AFS, Data', cabrillo_name = 'RSGB-AFS',
    ),
    Contest(
        name = 'RSGB AFS, SSB', cabrillo_name = 'RSGB-AFS',
    ),
    Contest(
        name = 'RSGB Commonwealth (BERU)', cabrillo_name = 'RSGB-BERU',
    ),
    Contest(
        name = 'RSGB DX', cabrillo_name = 'RSGB-DX',
        mult1_type = 'country', # Countries
        mult2_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'RSGB Eclipse 3.5MHz CW', cabrillo_name = 'RSGB-Eclipse-3.5MHz-CW-Contest',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'RSGB Eclipse 7MHz FT8', cabrillo_name = 'RSGB-Eclipse-7MHz-FT8-Contest',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'RSGB FT4 Contest Series', cabrillo_name = 'RSGB-FT4',
    ),
    Contest(
        name = 'RSGB FT4 Int. Activity Day', cabrillo_name = 'RSGB-FT4-IAD',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'RSGB IOTA', cabrillo_name = 'RSGB-IOTA',
        mult1_type = 'state', # IOTA
    ),
    Contest(
        name = 'RSGB Low Power 1 (9-12z)', cabrillo_name = 'RSGB-LOW-POWER',
    ),
    Contest(
        name = 'RSGB Low Power 2 (13-16z)', cabrillo_name = 'RSGB-LOW-POWER',
    ),
    Contest(
        name = 'RSGB National Field Day', cabrillo_name = 'RSGB-NFD',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'RSGB RoLo CW', cabrillo_name = 'RSGB-ROLO',
    ),
    Contest(
        name = 'RSGB RoLo SSB', cabrillo_name = 'RSGB-ROLO',
    ),
    Contest(
        name = 'RTTY OPS Weekday', cabrillo_name = 'RTTY-OPS-WEEKDAY',
    ),
    Contest(
        name = 'RTTY OPS Weekend', cabrillo_name = 'RTTY-OPS-WEEKEND',
    ),
    Contest(
        name = 'RTTYOps WW DX RTTY', cabrillo_name = 'RTTY-OPS-WW-DX',
        mult1_type = 'state', # Prec.
        mult2_type = 'prefix', # Prexix
    ),
    Contest(
        name = 'Real Time Contest', cabrillo_name = 'RTC',
        mult1_type = 'gridsquare', # Grid
    ),
    Contest(
        name = 'Romanian Diaspora SSB', cabrillo_name = 'DIASPORA-SSB',
        mult1_type = 'state', # YO/ER
        mult2_type = 'country', # DXCC
    ),
    Contest(
        name = 'Russian 160m', cabrillo_name = 'RADIO-160',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # Oblasts
    ),
    Contest(
        name = 'Russian Cup Digital', cabrillo_name = 'RFC-DIGI',
    ),
    Contest(
        name = 'Russian RTTY WW', cabrillo_name = 'RADIO-WW-RTTY',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Oblasts
    ),
    Contest(
        name = 'Russian WW MultiMode', cabrillo_name = 'RUS-WW-MM',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Obl.
    ),
    Contest(
        name = 'Russian WW PSK', cabrillo_name = 'RUS-WW-PSK',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Oblasts
    ),
    Contest(
        name = 'Russian YL/OM', cabrillo_name = 'RADIO-YL-OM',
        mult1_type = 'state', # YL
    ),
    Contest(
        name = 'SA 160m Challenge', cabrillo_name = 'SA-160m',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'SA Sprint', cabrillo_name = 'SA-SPRINT',
        mult1_type = 'wpxprefix', # Prefix
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'SARL HF CW', cabrillo_name = 'SARLDX-CW',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'SARL HF Digital', cabrillo_name = 'SARLDX-DIGI',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'SARL HF Phone', cabrillo_name = 'SARLDX-SSB',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'SARTG New Year RTTY Contest', cabrillo_name = 'SARTG-NY-RTTY',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'SARTG WW RTTY', cabrillo_name = 'SARTG-RTTY',
        mult1_type = 'country', # DXCC/Call Area
    ),
    Contest(
        name = 'SCC RTTY Championship', cabrillo_name = 'SCC-RTTY',
        mult1_type = 'state', # Prec
    ),
    Contest(
        name = 'SCRY/RTTYOps WW RTTY', cabrillo_name = 'SCRY',
        mult1_type = 'state', # Prec
        mult2_type = 'prefix', # SCA Prfx
    ),
    Contest(
        name = 'SEANET', cabrillo_name = 'SEANET-CONTEST',
        mult1_type = 'country', # DXCC/SEANET
    ),
    Contest(
        name = 'SKCC QSO Party', cabrillo_name = 'SKCC',
        mult1_type = 'state', # States/Provinces
    ),
    Contest(
        name = 'SKCC\'s Weekend Sprintathon', cabrillo_name = 'Straight Key Contest',
        mult1_type = 'wpxprefix', # Unique Calls
    ),
    Contest(
        name = 'SMIRK', cabrillo_name = 'SMIRK',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'SP DX', cabrillo_name = 'SP-DX',
        mult1_type = 'state', # Provinces/Countries
    ),
    Contest(
        name = 'SP DX RTTY', cabrillo_name = 'SP-DX-RTTY',
        mult1_type = 'state', # Provinces
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'SSA Juldagen', cabrillo_name = 'SSA-JULTEST',
    ),
    Contest(
        name = 'Samovar', cabrillo_name = 'SAMOVAR',
    ),
    Contest(
        name = 'Samuel Morse Memorial', cabrillo_name = 'SMMC',
        mult1_type = 'country', # DXCC
    ),
    Contest(
        name = 'Scandinavian Activity, CW', cabrillo_name = 'SAC-CW',
        mult1_type = 'country', # Countries/Scan.area
    ),
    Contest(
        name = 'Scandinavian Activity, SSB', cabrillo_name = 'SAC-SSB',
        mult1_type = 'country', # Countries/Scan.area
    ),
    Contest(
        name = 'Scandinavian Baltic RTTY', cabrillo_name = 'RTTY-OPS-WW-DX',
        mult1_type = 'country', # DXCC
        mult2_type = 'wpxprefix', # Prec
    ),
    Contest(
        name = 'Scottish DX', cabrillo_name = 'SDXC',
        mult1_type = 'state', # Regions
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'Sezioni ARI', cabrillo_name = 'ARI-SEZIONI',
        mult1_type = 'state', # Sezioni ARI
    ),
    Contest(
        name = 'Slobozhansky Sprint', cabrillo_name = 'UT5L',
        mult1_type = 'state', # Oblasts
    ),
    Contest(
        name = 'Solar Eclipse QSO Party', cabrillo_name = 'ECLIPSE-QSO',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'South America 10 Meter', cabrillo_name = 'SA10_SA',
        mult1_type = 'wpxprefix', # Prefixes
        mult2_type = 'zone', # Zones
    ),
    Contest(
        name = 'South American Integration CW', cabrillo_name = 'SACW',
        mult1_type = 'country', # SA
        mult2_type = 'wpxprefix', # Prefix
    ),
    Contest(
        name = 'South Carolina QSO Party', cabrillo_name = 'SC-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'South Dakota QSO Party', cabrillo_name = 'SD-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Stew Perry Topband Challenge', cabrillo_name = 'STEW-PERRY',
    ),
    Contest(
        name = 'TA VHF/UHF', cabrillo_name = 'TA-VHF-UHF',
    ),
    Contest(
        name = 'TISZA Cup', cabrillo_name = 'TISZA-CUP',
        mult1_type = 'zone', # Zones
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'TN POTA', cabrillo_name = 'TNPOTA',
        mult1_type = 'state', # POTA
    ),
    Contest(
        name = 'TRC DX', cabrillo_name = 'TRCDX',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'TRC Digi', cabrillo_name = 'TRC-DIGI',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # TRC
    ),
    Contest(
        name = 'TRIATHLON DX', cabrillo_name = 'TRIATHLON-DX-CONTEST',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # SV's
    ),
    Contest(
        name = 'TX State Parks on the Air', cabrillo_name = 'POTA',
        mult1_type = 'country', # Parks
    ),
    Contest(
        name = 'Tennessee QSO Party', cabrillo_name = 'TN-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Tesla Memorial HF CW', cabrillo_name = 'HF-TESLA',
    ),
    Contest(
        name = 'Texas QSO Party', cabrillo_name = 'TX-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Tiplayo DX', cabrillo_name = 'TIPALAYO-DX-CONTEST',
        mult1_type = 'prefix', # Prefixes
    ),
    Contest(
        name = 'Tuesday\'s Telegraphy', cabrillo_name = 'TTC-SPCWC',
    ),
    Contest(
        name = 'Turkey HF SSB', cabrillo_name = 'TR-HF',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # TA City
    ),
    Contest(
        name = 'UA1DZ CUP', cabrillo_name = 'ALRS-UA1DZ-CUP',
    ),
    Contest(
        name = 'UBA DX, CW', cabrillo_name = 'UBA-DX',
        mult1_type = 'country', # Prov./Prefixes/DXCC
    ),
    Contest(
        name = 'UBA DX, SSB', cabrillo_name = 'UBA-DX',
        mult1_type = 'state', # Prov./Prefixes/DXCC
    ),
    Contest(
        name = 'UBA ON SSB', cabrillo_name = 'UBA-ON',
        mult1_type = 'state', # Section
    ),
    Contest(
        name = 'UBA ON, 2m', cabrillo_name = 'UBA-ON',
        mult1_type = 'state', # Sections
    ),
    Contest(
        name = 'UBA ON, 6m', cabrillo_name = 'UBA-ON',
        mult1_type = 'state', # Sections
    ),
    Contest(
        name = 'UBA ON, CW', cabrillo_name = 'UBA-ON',
        mult1_type = 'state', # Sections
    ),
    Contest(
        name = 'UBA PSK63 Prefix', cabrillo_name = 'UBA-PSK63-PREFIX',
        mult1_type = 'state', # UBA sec.
        mult2_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'UBA Spring 2m', cabrillo_name = 'UBA-SPRING',
        mult1_type = 'state', # UBA sections
    ),
    Contest(
        name = 'UBA Spring HF CW', cabrillo_name = 'UBA-SPRING',
        mult1_type = 'state', # UBA sections
    ),
    Contest(
        name = 'UBA Spring HF Phone', cabrillo_name = 'UBA-SPRING',
        mult1_type = 'state', # UBA sections
    ),
    Contest(
        name = 'UBA Spring VHF/6m', cabrillo_name = 'UBA-SPRING',
        mult1_type = 'state', # UBA sections
    ),
    Contest(
        name = 'UCC CUP SSB', cabrillo_name = 'UCC-CUP',
        mult1_type = 'state', # UCC
    ),
    Contest(
        name = 'UCC PARTY RTTY', cabrillo_name = 'UCC-PARTY',
        mult1_type = 'state', # Oblasts
    ),
    Contest(
        name = 'UCC PARTY SSB', cabrillo_name = 'UCC-PARTY',
        mult1_type = 'state', # Oblasts
    ),
    Contest(
        name = 'UFT Meeting', cabrillo_name = 'UFT-HF',
        mult1_type = 'state', # UFT
    ),
    Contest(
        name = 'UK/EI DX, CW', cabrillo_name = 'UKEIDX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # UK/EI
    ),
    Contest(
        name = 'UK/EI DX, SSB', cabrillo_name = 'UKEIDX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # DC
    ),
    Contest(
        name = 'UKEICC 80m CW', cabrillo_name = 'UKEICC-80M',
    ),
    Contest(
        name = 'UKEICC 80m SSB', cabrillo_name = 'UKEICC-80M',
    ),
    Contest(
        name = 'UKSMG Summer', cabrillo_name = 'UKSMG',
    ),
    Contest(
        name = 'UN DIGI', cabrillo_name = 'UN-DIGI-CONTEST',
        mult1_type = 'prefix', # Prefixes
    ),
    Contest(
        name = 'UN DX', cabrillo_name = 'UN DX Contest',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # KDA
    ),
    Contest(
        name = 'URAL CUP', cabrillo_name = 'URAL-CUP',
        mult1_type = 'gridsquare', # VHF grids
    ),
    Contest(
        name = 'URC DX RTTY', cabrillo_name = 'URC-DX-RY',
        mult1_type = 'country', # Territory
    ),
    Contest(
        name = 'Ukraine CW Champ', cabrillo_name = 'UKR-CHAMP-CW',
        mult1_type = 'state', # Oblasts
    ),
    Contest(
        name = 'Ukraine RTTY Champ', cabrillo_name = 'UKR-CHAMP-RTTY',
    ),
    Contest(
        name = 'Ukraine SSB Champ', cabrillo_name = 'UKR-CHAMP-SSB',
        mult1_type = 'state', # Oblasts
    ),
    Contest(
        name = 'Ukrainian Contest Club', cabrillo_name = 'UCC-CONTEST',
        mult1_type = 'prefix', # UCC
    ),
    Contest(
        name = 'Ukrainian DX', cabrillo_name = 'UKRAINIAN-DX',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Oblasts
    ),
    Contest(
        name = 'Ukrainian DX Classic RTTY', cabrillo_name = 'UKRAINIAN-DX',
        mult1_type = 'country', # DXCC/WAE
        mult2_type = 'state', # UR-Oblast
    ),
    Contest(
        name = 'Ukrainian DX DIGI', cabrillo_name = 'UKRAINIAN-DX',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # Oblasts
    ),
    Contest(
        name = 'VK Shires', cabrillo_name = 'VK-SHIRES',
        mult1_type = 'zone', # CQ zone/Shire
    ),
    Contest(
        name = 'VOLTA WW RTTY', cabrillo_name = 'VOLTA-RTTY',
        mult1_type = 'country', # Countries/Call areas
    ),
    Contest(
        name = 'Venezuelan Independence', cabrillo_name = 'YV',
        mult1_type = 'wpxprefix', # Call areas
        mult2_type = 'country', # Countries
    ),
    Contest(
        name = 'Vermont QSO Party', cabrillo_name = 'VT-QSO-PARTY',
        mult1_type = 'state', # Counties/States/Prov.
    ),
    Contest(
        name = 'Virginia QSO Party', cabrillo_name = 'VA-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'W/VE Island QSO Party', cabrillo_name = 'USI-WVE-IS-QP',
        mult1_type = 'state', # Islands/States/Prov.
    ),
    Contest(
        name = 'WAB 1.8 MHz Phone/CW', cabrillo_name = 'WAB-HF',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # WAB
    ),
    Contest(
        name = 'WAB 144 MHz Low Power Phone', cabrillo_name = 'WAB-PHONE',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # WAB
    ),
    Contest(
        name = 'WAB 144 MHz QRO Phone', cabrillo_name = 'WAB-PHONE',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # WAB
    ),
    Contest(
        name = 'WAB 3.5 Mhz Phone/CW', cabrillo_name = 'WAB-PHONE-CW',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # WAB
    ),
    Contest(
        name = 'WAB 3.5/7/14 MHz Data', cabrillo_name = 'WAB-DATA',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # WAB
    ),
    Contest(
        name = 'WAB 50 MHz Phone', cabrillo_name = 'WAB-PHONE',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # WAB
    ),
    Contest(
        name = 'WAB 7 MHz Phone', cabrillo_name = 'WAB-PHONE',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # WAB
    ),
    Contest(
        name = 'WAE DX RTTY', cabrillo_name = 'DARC-WAEDC-RTTY',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'WAE DX SSB', cabrillo_name = 'DARC-WAEDC-SSB',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'WAE DX, CW', cabrillo_name = 'DARC-WAEDC-CW',
        mult1_type = 'country', # Countries
    ),
    Contest(
        name = 'WI SPOTA', cabrillo_name = 'WI-SPOTA',
        mult1_type = 'state', # WI Park
    ),
    Contest(
        name = 'WIA Remembrance Day', cabrillo_name = 'WIA-Remembrance',
    ),
    Contest(
        name = 'WRTC Practice', cabrillo_name = 'WRTC',
        mult1_type = 'country', # Country
        mult2_type = 'hq', # HQ
    ),
    Contest(
        name = 'WW Argentina DX', cabrillo_name = 'WWPDX',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'WW Digi DX', cabrillo_name = 'WW-DIGI',
        mult1_type = 'gridsquare', # Grids
    ),
    Contest(
        name = 'WW PMC', cabrillo_name = 'WW-PMC',
        mult1_type = 'wpxprefix', # PMC
    ),
    Contest(
        name = 'WW Side Band Activity', cabrillo_name = 'WWSAC',
        mult1_type = 'wpxprefix', # WPX
    ),
    Contest(
        name = 'Washington State Salmon Run', cabrillo_name = 'WA-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Weekly RTTY', cabrillo_name = 'WRT',
        mult1_type = 'state', # Calls
    ),
    Contest(
        name = 'West Virginia QSO Party', cabrillo_name = 'WV-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Winter Field Day', cabrillo_name = 'WFDA-CONTEST',
        mult1_type = 'wpxprefix', # Modes
    ),
    Contest(
        name = 'Wisconsin QSO Party', cabrillo_name = 'WI-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'Worked All Germany', cabrillo_name = 'WAG',
        mult1_type = 'country', # Countries/Districts
    ),
    Contest(
        name = 'Worked All Provinces of China CW', cabrillo_name = 'WAPC-DX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # BY prov.
    ),
    Contest(
        name = 'Worked All Provinces of China SSB', cabrillo_name = 'WAPC-DX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # BY prov.
    ),
    Contest(
        name = 'YARC Summer QSO Party', cabrillo_name = 'YARC-QSO-PARTY',
        mult1_type = 'state', # Count./DXCC/St./Prov.
    ),
    Contest(
        name = 'YB Banggai DX', cabrillo_name = 'Banggai-DX',
        mult1_type = 'country', # DXCC/Prefix/Age
    ),
    Contest(
        name = 'YB Bekasi Merdeka', cabrillo_name = 'Bekasi-Merdeka-Contest',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # YB
    ),
    Contest(
        name = 'YB DX', cabrillo_name = 'YB-DX-CONTEST',
        mult1_type = 'country', # DXCC
        mult2_type = '', # YB pref.
    ),
    Contest(
        name = 'YB DX RTTY', cabrillo_name = 'YB-DX-CONTEST',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # YB pref.
    ),
    Contest(
        name = 'YB ORARI DX', cabrillo_name = 'ORARI-DX',
        mult1_type = 'country', # YB/DXCC/Prefix
    ),
    Contest(
        name = 'YB7 DX', cabrillo_name = 'YB7-DX CONTEST',
        mult1_type = 'wpxprefix', # Prefixes
    ),
    Contest(
        name = 'YBDXPI FT8', cabrillo_name = 'YBDXPIFT8',
        mult1_type = 'country', # DXCC
        mult2_type = 'prefix', # Prefix
    ),
    Contest(
        name = 'YBDXPI SSB', cabrillo_name = 'YBDXPI-SSB-DX',
        mult1_type = 'country', # DXCC
        mult2_type = 'state', # YBDXPI
    ),
    Contest(
        name = 'YO DX HF', cabrillo_name = 'YO-DX-HF',
        mult1_type = 'country', # Countries
        mult2_type = 'state', # YO Counties
    ),
    Contest(
        name = 'YOTA Round 1', cabrillo_name = 'YOTA',
        mult1_type = 'prefix', # Age
    ),
    Contest(
        name = 'YOTA Round 2', cabrillo_name = 'YOTA',
        mult1_type = 'prefix', # Age
    ),
    Contest(
        name = 'YOTA Round 3', cabrillo_name = 'YOTA',
        mult1_type = 'prefix', # Age
    ),
    Contest(
        name = 'YU DX', cabrillo_name = 'YU-DX',
        mult1_type = 'country', # Countries
        mult2_type = 'wpxprefix', # YU prefixes
        mult2_pattern = '[A-Z]{3}'
    ),
    Contest(
        name = 'Yuri Gagarin International DX', cabrillo_name = 'GC',
        mult1_type = 'zone', # ITU/SS
    ),
    Contest(
        name = 'ZOMBIE Shuffle', cabrillo_name = 'Zombie Shuffle',
        mult1_type = 'state', # Zombie/Areas
    ),
    Contest(
        name = 'Zimski KV KUP 9A5K Memorial', cabrillo_name = 'HRV-ZIMSKI-KUP',
        mult1_type = 'state', # Mult
    ),
    Contest(
        name = '070 Club Three Day Weekend', cabrillo_name = 'PODXS_TDW',
        mult1_type = 'state', # Club numbers
    ),
]
