from argparse import ArgumentParser, RawDescriptionHelpFormatter
from platform import python_version
from operator import itemgetter
import sys
import os
import re
import time


module_name = '%(prog)s: Normalizes filenames downloaded from sharing services'
script_name = os.path.basename(__file__)
__version__ = '0.1.0'
acaronyms_re_langs = (
        r'\b(AAR|AA|ABK|AB|AFR|AF|AKA|AK|ALB|SQ|AMH|AM|ARA|AR|ARG|AN|ARM|'
        r'HY|ASM|AS|AVA|AV|AVE|AE|AYM|AY|AZE|AZ|BAK|BA|BAM|BM|BAQ|EU|BEL|'
        r'BE|BEN|BN|BIH|BH|BIS|BI|BOS|BS|BRE|BR|BUL|BG|BUR|MY|CAT|CA|CHA|'
        r'CH|CHE|CE|CHI|ZH|CHV|CV|COR|KW|COS|CO|CRE|CR|CZE|CS|DAN|'
        r'DA|DIV|DV|DUT|NL|DZO|DZ|ENG|EN|EPO|EO|EST|ET|EWE|EE|FAO|FO|FIJ|'
        r'FJ|FIN|FI|FRE|FR|FRY|FY|FUL|FF|GEO|KA|GER|DE|GLA|GD|GLE|GA|GLG|'
        r'GL|GLV|GV|GRE|EL|GRN|GN|GUJ|GU|HAT|HT|HAU|HA|HEB|HE|HER|HZ|HIN|'
        r'HI|HMO|HO|HRV|HR|HUN|HU|IBO|IG|ICE|IS|IDO|IO|III|II|IKU|IU|'
        r'IND|ID|IPK|IK|ITA|IT|JAV|JV|JPN|JA|KAL|KL|KAN|KN|KAS|'
        r'KS|KAU|KR|KAZ|KK|KHM|KM|KIK|KI|KIN|RW|KIR|KY|KOM|KV|KON|KG|KOR|'
        r'KO|KUA|KJ|KUR|KU|LAO|LO|LAT|LA|LAV|LV|LIM|LI|LIN|LN|LIT|LT|LTZ|'
        r'LB|LUB|LU|LUG|LG|MAC|MK|MAH|MH|MAL|ML|MAO|MI|MAR|MR|MAY|MS|MLG|'
        r'MG|MLT|MT|MON|MN|NAU|NA|NAV|NV|NBL|NR|NDE|ND|NDO|NG|NEP|NE|NNO|'
        r'NN|NOB|NB|NOR|NO|NYA|NY|OCI|OC|OJI|OJ|ORI|OR|ORM|OM|OSS|OS|PAN|'
        r'PA|PLI|PI|POL|PL|POR|PT|PUS|PS|QUE|QU|ROH|RM|RUM|RO|RUN|'
        r'RN|RUS|RU|SAG|SG|SIN|SI|SLO|SK|SLV|SL|SME|SE|SMO|SM|SNA|'
        r'SN|SND|SD|SOM|SO|SOT|ST|SPA|ES|SRD|SC|SRP|SR|SSW|SS|SUN|SU|SWA|'
        r'SW|SWE|SV|TAH|TY|TAM|TA|TAT|TT|TEL|TE|TGK|TG|TGL|TL|THA|TH|TIB|'
        r'BO|TIR|TI|TON|TO|TSN|TN|TSO|TS|TUK|TK|TUR|TR|TWI|TW|UIG|UG|UKR|'
        r'UK|URD|UR|UZB|UZ|VEN|VE|VIE|VI|WEL|CY|WLN|WA|WOL|WO|XHO|'
        r'XH|YID|YI|YOR|YO|ZHA|ZA|ZUL|ZU|ITAL|'
        r'AFAR|ABKHAZIAN|AFRIKAANS|AKAN|ALBANIAN|AMHARIC|ARABIC|ARAGONESE|'
        r'ARMENIAN|ASSAMESE|AVARIC|AVESTAN|AYMARA|AZERBAIJANI|BASHKIR|BAMBARA|'
        r'BASQUE|BELARUSIAN|BENGALI|BIHARI LANGUAGES|BISLAMA|BOSNIAN|BRETON|'
        r'BULGARIAN|BURMESE|CATALAN|VALENCIAN|CHAMORRO|CHECHEN|CHINESE|CHUVASH|'
        r'CORNISH|CORSICAN|CREE|CZECH|DANISH|DIVEHI|DHIVEHI|MALDIVIAN|DUTCH|'
        r'FLEMISH|DZONGKHA|ENGLISH|ESPERANTO|ESTONIAN|EWE|FAROESE|FIJIAN|'
        r'FINNISH|FRENCH|WESTERN FRISIAN|FULAH|GEORGIAN|GERMAN|GAELIC|SCOTTISH|'
        r'IRISH|GALICIAN|MANX|"GREEK|GUARANI|GUJARATI|HAITIAN|HAITIAN CREOLE|HAUSA|'
        r'HEBREW|HERERO|HINDI|HIRI MOTU|CROATIAN|HUNGARIAN|IGBO|ICELANDIC|IDO|'
        r'SICHUAN YI|NUOSU|INUKTITUT|INTERLINGUE|INDONESIAN|INUPIAQ|ITALIAN|'
        r'JAVANESE|JAPANESE|KALAALLISUT|GREENLANDIC|KANNADA|KASHMIRI|KANURI|'
        r'KAZAKH|CENTRAL KHMER|KIKUYU|GIKUYU|KINYARWANDA|KIRGHIZ|KYRGYZ|KOMI|KONGO|'
        r'KOREAN|KUANYAMA|KWANYAMA|KURDISH|LAO|LATIN|LATVIAN|LIMBURGAN|LIMBURGER|'
        r'LIMBURGISH|LINGALA|LITHUANIAN|LUXEMBOURGISH|LETZEBURGESCH|LUBA-KATANGA|'
        r'GANDA|MACEDONIAN|MARSHALLESE|MALAYALAM|MAORI|MARATHI|MALAY|MALAGASY|'
        r'MALTESE|MONGOLIAN|NAURU|NAVAJO|NAVAHO|"NDEBELE|NDEBELE|NDONGA|NEPALI|'
        r'NORWEGIAN|NYNORSK|CHICHEWA|CHEWA|NYANJA|OCCITAN|PROVENÇAL|OJIBWA|ORIYA|'
        r'OROMO|OSSETIAN|OSSETIC|PANJABI|PERSIAN|PALI|POLISH|PORTUGUESE|PUSHTO|'
        r'PASHTO|QUECHUA|ROMANSH|ROMANIAN|MOLDAVIAN|MOLDOVAN|RUNDI|RUSSIAN|SANGO|'
        r'SINHALA|SINHALESE|SLOVAK|SLOVENIAN|NORTHERN SAMI|SAMOAN|SHONA|'
        r'SINDHI|SOMALI|SOTHO|SPANISH|CASTILIAN|SARDINIAN|SERBIAN|SWATI|SUNDANESE|'
        r'SWAHILI|SWEDISH|TAHITIAN|TAMIL|TATAR|TELUGU|TAJIK|TAGALOG|THAI|TIBETAN|'
        r'TIGRINYA|TONGA|TSWANA|TSONGA|TURKMEN|TURKISH|TWI|UIGHUR|UYGHUR|UKRAINIAN|'
        r'URDU|UZBEK|VENDA|VIETNAMESE|WELSH|WALLOON|WOLOF|XHOSA|YIDDISH|YORUBA|'
        r'ZHUANG|CHUANG|ZULU)\b')


def get_acronyms_re(langs):
    acronyms_re_begin = (
        r'(?:^|(?<=))('
        r'CAM|TS|TC|DV|MiniDV|R3|R4|R5|R6|VHSSCR|DVDSCR|DVDRip|DVDMux|'
        r'DVD5|DVD9|BRRip|BDRip|BDMux|BluRay|VU|SBS|WEB-DL|WEBRip|HDTV|HDTS|PDTV|'
        r'SATRip|SAT RIP|DVBRip|DVDRip|DRip|DVB-S|DTTRip|TVRip|TV TIP|WP|SCREENER|'
        r'HQ|TV|RIP|SUBS|1080p|HEVC|'
        r'AAC|AC3|MP3|DTS|MD|LD|DD|DSP|DSP2|AVC|'
        r'H 264|HD|HD 720|DivX|XviD|x264|x265|')
    acronyms_re_end = \
        r')(?:(?=)|$)'

    if langs:
        return acronyms_re_begin + acaronyms_re_langs + acronyms_re_end
    return acronyms_re_begin + acronyms_re_end


def normalize(filename, acronyms_re):
    basename, ext = itemgetter(0,1)(os.path.splitext(filename))
    
    # Turn dots to spaces
    basename = re.sub(r'[.]', ' ', basename)
    # Remove text in parenthesis
    basename = re.sub(r'(\().+?(\))', '', basename)
    basename = re.sub(r'(\[).+?(\])', '', basename)
    # Remove acronyms
    basename = acronyms_re.sub('', basename)
    # Remove exceeding spaces
    basename = ' '.join(basename.split())

    return f'{basename}{ext}'


def shorten(filename):
    if len(filename) >= 30:
        return f'{filename[:15]}...{filename[len(filename)-15:]}'
    return filename


def print_preview(normalized):
    preview = normalized[:10]
    total = len(normalized) 

    if len(normalized) > 10:
        print(f'Operations on first 10 files on a total of {total}:')

    for oldname, newname in preview:
        print(f'{shorten(oldname)} -> {newname}')

    if len(preview) > 0:
        print('')


def print_failed(failed):
    print('\n')
    print(f'{script_name}: impossible to rename the following file(s):')
    for f in failed:
        print(f)


def confirm(target_dir, file_count):
    what_to_rename = f'all {file_count} files' if file_count > 1 else 'the file'

    proceed = input(f'{script_name}: sure you want to rename {what_to_rename} in {target_dir} [yn]?')

    if len(proceed) == 1 and proceed == 'y':
        return True
    elif len(proceed) == 1 and (proceed == 'n' or proceed == 'q'):
        return False

    return confirm(target_dir, file_count)


def is_hidden(filepath):
    return os.path.basename(filepath)[:1] == '.'


def is_subtitle(filepath):
    ext = os.path.splitext(filepath)[1][1:]
    return ext.lower() in ['srt', 'ssa', 'ttml', 'sbv', 'dfxp', 'vtt', 'cap', 'mcc', 'sami', 'stl', 'qt.txt']


def try_rename(oldname, newname):
    try:
        os.rename(oldname, newname)
        return True
    except:
        return False


def main():
    version_string = f'{module_name}\n' + \
                     f'Version: {__version__}\n' + \
                     f'Python:  {python_version()}'

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f'{module_name} (Version {__version__})')
    parser.add_argument('--version',
                        action='version',  version=version_string,
                        help='display version information')
    parser.add_argument('--force', '-f',
                        action='store_true',  dest='force', default=False,
                        help='attempt to rename the files without prompting for confirmation')
    parser.add_argument('--skip-subtitle', '-s',
                        action='store_true',  dest='skip_subtitle', default=False,
                        help='skip files with common subtitle extensions')
    parser.add_argument('--remove-langs', '-l',
                        action='store_true',  dest='remove_langs', default=False,
                        help='remove language codes from filename')
    parser.add_argument('directory',
                        nargs='?', metavar='DIRECTORY',
                        action='store',
                        help='directory containg the files to rename')

    args = parser.parse_args()

    target_dir = os.path.realpath(args.directory if args.directory != None else '.')
    if not os.path.exists(target_dir):
        sys.exit(f'{script_name}: {target_dir}: no such file or directory')

    # Filter files excluding directories
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    if len(files) == 0:
        sys.exit(f'{script_name}: {target_dir}: contains no files')

    # Skip subtitle files if requested
    if args.skip_subtitle:
        files = [f for f in files if not is_subtitle(f)]

    # Normalize excluding hidden files
    acronyms_re = re.compile(get_acronyms_re(args.remove_langs), re.IGNORECASE)
    normalized = [(f, normalize(f, acronyms_re)) for f in files if not is_hidden(os.path.join(target_dir, f))]

    # Remove files that don't need rename
    normalized = [(oldname, newname) for oldname, newname in normalized if oldname != newname]

    file_count = len(normalized)
    if file_count == 0:
        sys.exit(f'{script_name}: {target_dir}: contains no filenames to normalize')

    proceed = True
    if not args.force:
        print_preview(normalized)
        proceed = confirm(target_dir, file_count)

    if proceed:
        print(f'Renaming into \'{target_dir}\'...')
        print(f'Renaming files 0% 0/{file_count}', end="\r", flush=True)

        completed = 0
        step_perc = 100 / file_count
        failed = []

        for n, (oldname, newname) in enumerate(normalized):
            time.sleep(0.1)
            if not try_rename(os.path.join(target_dir, oldname), os.path.join(target_dir, newname)):
                failed.append(oldname)

            completed += step_perc
            print(f'Renaming files {int(completed)}% {n + 1}/{file_count}', end='\r', flush=True)       

        print(f'Renaming files 100% {n + 1}/{file_count}, done.', end='\r', flush=True)
        print('')

        if len(failed) > 0:
            print_failed(failed)


if __name__ == '__main__':
    main()