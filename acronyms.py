import os
import json


EXTRA_FILENAME = "extra.json"


class RE:
    COMMON = (
        'CAM|TS|TC|DV|MiniDV|R3|R4|R5|R6|VHSSCR|DVDSCR|DVDRip|DVDMux|'
        'WEBMux|DLMux|DVD5|DVD9|BRRip|BDRip|BDMux|BluRay|VU|SBS|WEB-DL|'
        'WEBRip|WEB-RIP|HDTV|HDTS|PDTV|SATRip|SAT RIP|DVBRip|DVDRip|'
        'DRip|DVB-S|DTTRip|TVRip|TV TIP|WP|SCREENER|HQ|TV|RIP|SUBS|'
        '1080p|HEVC|720p|AAC|AC3|MP3|DTS|MD|LD|DD|DSP|DSP2|AVC|H 264|'
        'HD|HD 720|DivX|XviD|x264|x265'
    )
    LANGUAGES = (
        'ITA|ENG|SPA|FRA|GER|DEU|'
        'ITAL|ITALIAN|ENGLISH|SPANISH|FRENCH|GERMAN'
        )


def build_re(args):
    extra_path = os.path.join('.', EXTRA_FILENAME)
    if os.path.exists(extra_path):
        extra = json.loads(open(extra_path).read())
    more_acronyms = ''
    if args.remove_langs:
        more_acronyms = RE.LANGUAGES
    if args.remove_noise:
        if not more_acronyms:
            more_acronyms += '|'
        more_acronyms += '|'.join(extra)
    acronyms = f'(?:^|(?<=))({RE.COMMON})|'
    if more_acronyms:
        acronyms += r'\b(' + more_acronyms + r')\b'
    return acronyms + r'(?:(?=)|$)'