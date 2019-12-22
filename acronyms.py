import os
import json
import re

ACRONYMS_FILENAME = "acronyms.json"

RE_COMMON = (
    'CAM|TS|TC|DV|MiniDV|R3|R4|R5|R6|VHSSCR|DVDSCR|DVDRip|Mux|DVDMux|'
    'WEBMux|DLMux|DVD5|DVD9|BRRip|BDRip|BDMux|BluRay|VU|SBS|WEBDL|'
    'WEB-DL|WEBRip|WEB-RIP|HDTV|HDTS|PDTV|SATRip|SAT RIP|DVBRip|DVDRip|'
    'DRip|DVB-S|DTTRip|TVRip|TV TIP|WP|SCREENER|HQ|TV|RIP|SUBS|'
    '1080p|HEVC|720p|AAC|AC3|MP3|DTS|MD|LD|DD|DSP|DSP2|AVC|H264|H 264|'
    'HD|HD 720|DivX|XviD|x264|x265'
)
RE_LANGUAGES = (
    'ITAL|ITALIAN|ENGLISH|SPANISH|FRENCH|GERMAN|'
    'ITA|ENG|SPA|FRA|GER|DEU|'   
    )


def build_re(args):
    extra_path = os.path.join('.', ACRONYMS_FILENAME)
    if os.path.exists(extra_path):
        extra = [re.escape(acronym) \
            for acronym in json.loads(open(extra_path).read())]
    more_acronyms = ''
    if args.remove_langs:
        more_acronyms = RE_LANGUAGES
    if args.remove_noise:
        if more_acronyms:
            more_acronyms += '|'
        more_acronyms += '|'.join(extra)
    acronyms = '(?:^|(?<=))({})|'.format(RE_COMMON)
    if more_acronyms:
        acronyms += r'\b(' + more_acronyms + r')\b'
    return acronyms + r'(?:(?=)|$)'