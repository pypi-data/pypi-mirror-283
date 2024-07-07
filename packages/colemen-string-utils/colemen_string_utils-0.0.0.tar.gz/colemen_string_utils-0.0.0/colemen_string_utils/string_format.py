# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    A module of utility methods used for formatting strings.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:00:27
    `memberOf`: string_utils
'''


# import json
# import hashlib
import logging as _logging
from pathlib import Path, PurePath
# import colemen_config as _config
from typing import Union as _Union
import re as _re
import os as _os
import urllib.parse



# import colemen_utilities.dict_utils as _obj
# import colemen_utilities.console_utils as _con
# from pyparsing import And, Suppress,Dict, Word, Literal, Group, Optional, ZeroOrMore, OneOrMore, Regex, restOfLine, alphanums,nums, printables, string, CaselessKeyword,nestedExpr,ParseException,quotedString,removeQuotes,originalTextFor,delimitedList,QuotedString
# from pyparsing import QuotedString



from colemen_string_utils.settings.control import inflect_engine
from colemen_string_utils.string_escaping import escape_regex
from colemen_string_utils.string_strip import strip_end
from colemen_string_utils.support import get_kwarg as _get_kwarg

logger = _logging.getLogger(__name__)


def to_pascal_case(subject:str,first_char_lower=False,first_char_alpha=True)->str:
    '''
        Convert a string to PascalCase.

        ----------

        Arguments
        -------------------------
        `subject` {str}
            The string to format to PascalCase

        [`first_char_lower`=False] {bool}
            If True the first charact will be lower case, essentially making it camelCase.

        [`first_char_alpha`=True] {bool}
            If True, any leading not alphabetic characters are stripped.

        Return {str}
        ----------------------
        The string formatted as PascalCase

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:23:01
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: to_pascal_case
        * @xxx [06-03-2022 09:26:00]: documentation for to_pascal_case
    '''


    subject = _re.sub(r'[^a-zA-Z0-9_\s]', ' ', subject)

    subject = to_snake_case(subject)
    subject = _re.sub(r'([a-zA-Z0-9])([a-zA-Z0-9]*)', lambda x: x.group(1).upper() + x.group(2).lower(), subject)

    if first_char_alpha:
        subject = _re.sub(r'^[^a-zA-Z]*', r'', subject)
    else:
        first_char_lower=False
    subject = _re.sub(r'_', '', subject)

    if first_char_lower:
        subject = _re.sub(r'^([A-Za-z])', lambda x: x.group(1).upper(), subject)

    return subject

def to_camel_case(subject:str,first_char_lower=True,first_char_alpha=True)->str:
    '''
        Convert a string to camelCase.

        ----------

        Arguments
        -------------------------
        `subject` {str}
            The string to format to camelCase

        [`first_char_lower`=True] {bool}
            If True the first charact will be lower case.

        [`first_char_alpha`=True] {bool}
            If True, any leading not alphabetic characters are stripped.

        Return {str}
        ----------------------
        The string formatted as camelCase

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:23:01
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: to_camel_case
        * @xxx [06-03-2022 09:26:00]: documentation for to_camel_case
    '''
    subject = _re.sub(r'[^a-zA-Z0-9_\s]', ' ', subject)

    subject = to_snake_case(subject)
    subject = _re.sub(r'([a-zA-Z0-9])([a-zA-Z0-9]*)', lambda x: x.group(1).upper() + x.group(2).lower(), subject)

    if first_char_alpha:
        subject = _re.sub(r'^[^a-zA-Z]*', r'', subject)
    else:
        first_char_lower=False
    subject = _re.sub(r'_', '', subject)

    if first_char_lower:
        subject = _re.sub(r'^([A-Za-z])', lambda x: x.group(1).lower(), subject)

    return subject

def to_snake_case(subject:str,first_char_alpha=False)->str:
    '''
        Convert a subject to snake_case.

        ----------

        Arguments
        -----------------
        `subject` {str}
            The subject to convert

        [`first_char_alpha`=False] {bool}
            If True any leading non-alphabetic characters will be removed.

        Return
        ----------
        `return` {str}
            The subject converted to snake_case

        Example
        ----------
        BeepBoop Bleep blorp => beep_boop_bleep_blorp
    '''
    subject = str(subject)

    if first_char_alpha:
        subject = _re.sub(r'^[^a-zA-Z]*',"",subject)

    subject = _re.sub(r'[^a-zA-Z0-9_\s]'," ",subject)
    subject = _re.sub(r'(\s|_)+',"_",subject)
    subject = _re.sub(r'([a-z])(?:\s|_)?([A-Z])',r"\1_\2",subject)
    return subject.lower()

def to_screaming_snake(subject:str):
    '''
        Convert a subject to SCREAMING_SNAKE_CASE.

        ----------

        Arguments
        -----------------
        `subject` {str}
            The subject to convert

        Return
        ----------
        `return` {str}
            The subject converted to SCREAMING_SNAKE_CASE

        Example
        ----------
        BeepBoop Bleep blorp => BEEP_BOOP_BLEEP_BLORP
    '''

    return to_snake_case(subject).upper()

def to_kebab_case(subject:str)->str:
    '''
        Convert a string to kebab-case

        ----------

        Arguments
        -------------------------
        `subject` {str}
            The string to convert to kebab-case.

        Return {str}
        ----------------------
        The string in kebab-case.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:30:05
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: to_kebab_case
        * @xxx [06-03-2022 09:30:57]: documentation for to_kebab_case
    '''


    subject = to_snake_case(subject)
    return subject.replace("_","-")

def to_dot_notation(subject:str)->str:
    '''
        Convert a string to dot.notation

        ----------

        Arguments
        -------------------------
        `subject` {str}
            The string to convert to dot.notation


        Return {str}
        ----------------------
        The string converted to dot.notation.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:31:04
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: to_dot_notation
        * @xxx [06-03-2022 09:31:45]: documentation for to_dot_notation
    '''


    subject = to_snake_case(subject)
    dotted = subject.replace("_",".")
    output = _re.sub(r'^\.*','',dotted)
    return output

def to_title_case(value:str,reverse=False)->str:
    '''
        Convert A String To Title Case.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to convert to Title Case
        [`reverse`=False] {bool}
            If True, all letters except for the first of each word will be capitalized.

        Return {str}
        ----------------------
        The string in Title Case

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:38:23
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: title_case
        * @xxx [06-03-2022 09:39:51]: documentation for title_case
    '''


    orig_type = 'list'
    if isinstance(value,(str)):
        orig_type = 'string'
        value = [value]
    result = []
    if reverse is True:
        result = to_reverse_title_case(value)
    else:
        for word in value:
            result.append(word.title())

    if orig_type == 'list':
        return result
    if orig_type == 'string' and len(result) == 1:
        return result[0]
    else:
        return result

def to_reverse_title_case(value:str)->str:
    '''
        fORMAT a sTRING tO rEVERSE tITLE cASE.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to format to rEVERSE tITLE cASE

        Return {str}
        ----------------------
        The string formatted to rEVERSE tITLE cASE

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:40:53
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: reverse_title_case
        * @xxx [06-03-2022 09:42:31]: documentation for reverse_title_case
    '''


    orig_type = 'list'

    if isinstance(value,(str)):
        orig_type = 'string'
        value = [value]

    result = []
    for word in value:
        lower = word.lower()
        upper = word.upper()
        result.append(f"{lower[0]}{upper[1:]}")

    if orig_type == 'list':
        return result
    if orig_type == 'string' and len(result) == 1:
        return result[0]
    else:
        return result





def limit_length(subject, max_len=2, from_beginning=True):
    '''
        Limits the subject's character count to the max_len.

        ----------

        Arguments
        -------------------------
        `subject` {str}
            The subject to convert
        `max_len` {int}
            The maximum length of the subject, if >= max_len the subject will not be padded.

        [`limit_length`=False] {bool}
            If True the subject will have excess characters removed from the beginning or end.
        [`from_beginning`=True] {bool}
            If True the subject will have excess characters removed from the beginning.\n
            If False the subject will have excess characters removed from the end.

        Return {str}
        ----------------------
        The formatted string

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-20-2021 14:48:31
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: limit_length
    '''
    subject = str(subject)
    slen = len(subject)
    if slen <= max_len:
        return subject
    else:
        if from_beginning is True:
            return subject[:max_len]
        if from_beginning is False:
            return subject[max_len:]

def leftPad(subject, max_len=2, pad_char='0', limit_len=False, from_beginning=True):
    '''
        Convert a subject to snake_case.

        ----------
        Arguments
        -----------------
        `subject` {str}
            The subject to convert
        `max_len` {int}
            The maximum length of the subject, if >= max_len the subject will not be padded.
        `pad_char` {str}
            The character to pad the subject with

        [`limit_len`=False] {bool}
            If True the subject will have excess characters removed from the beginning or end.

        [`from_beginning`=True] {bool}
            If True the subject will have excess characters removed from the beginning.\n
            If False the subject will have excess characters removed from the end.
        Return
        ----------
        `return` {str}
            The subject formatted with left padding

        Example
        ----------
        leftPad("1",5,'0') // "00001"
        leftPad("/esls_test/server_source/TEST.scss",15,' ',True,True) // "/esls_test/serv"
        leftPad("/e/TEST.scss",15,' ',True,False) // "   /e/TEST.scss"
    '''
    if limit_len is True:
        subject = limit_length(subject, max_len, from_beginning)
    subject = str(subject)
    slen = len(subject)
    if slen <= max_len:
        subject = f"{pad_char * (max_len - slen)}{subject}"
    return subject

def rightPad(subject, max_len=2, pad_char='0'):
    '''
        Convert a subject to snake_case.

        ----------
        Arguments
        -----------------
        `subject` {subject}
            The subject to convert
        `max_len` {int}
            The maximum length of the subject, if >= max_len the subject will not be padded.
        `pad_char` {subject}
            The character to pad the subject with
        Return
        ----------
        `return` {subject}
            The subject formatted with left padding

        Example
        ----------
        leftPad("1",5,'0') // "00001"
    '''
    subject = str(subject)
    slen = len(subject)
    if slen <= max_len:
        subject = f"{subject}{pad_char * (max_len - slen)}"
    return subject

def encode_quotes(value:str)->str:
    '''
        Encodes single and double quotes within the value to &apos; or &quot; respectively.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to encode

        Return {str}
        ----------------------
        The encoded string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:15:52
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: encode_quotes
    '''
    value = value.replace("'", "&apos;")
    value = value.replace('"', "&quot;")
    return value

def decode_quotes(value:str)->str:
    '''
        Decodes single and double quotes within the value from &apos; or &quot; respectively.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to decode

        Return {str}
        ----------------------
        The decoded string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:15:52
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: encode_quotes
    '''
    value = value.replace("&apos;", "'")
    value = value.replace("&quot;", '"')
    return value



def windows_file_name(file_name:str)->str:
    '''
        Strips (window's) invalid characters from the file_name.\n
        These characters are removed:\n
        <>:"/\\|?*

        ----------

        Arguments
        -------------------------
        `file_name` {str}
            The string to be parsed.

        Return {str}
        ----------------------
            The parsed string

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 13:32:36
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: windows_file_name
    '''
    return _re.sub(r'[<>:"/\|?*]*', "", file_name)

def extension(string:_Union[str,list])->_Union[str,list]:
    '''
        Formats a file extension to have no leading period.

        ----------

        Arguments
        -------------------------
        `value` {str|list}
            The file extension(s) [separated by commas] or list of extensions to format

        Keyword Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Return {str}
        ----------------------
        The formatted file extension

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 13:33:51
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: extension
    '''
    new_ext_array = []
    if isinstance(string,(str)):
        if "," in string:
            string = string.split(",")
    if isinstance(string, list) is False:
        string = [string]

    for ext in string:
        # print(f"ext: {ext}")
        ext = ext.lower()
        ext = _re.sub(r"^\.*", '', ext)
        new_ext_array.append(ext)

    if len(new_ext_array) > 1:
        new_ext_array = list(set(new_ext_array))
    if len(new_ext_array) == 1:
        return new_ext_array[0]
    return new_ext_array
format_extension = extension

def path(value):
    if isinstance(value,(list,tuple)):
        if value[-1].startswith("."):
            file_name = f"{value[-2]}{value[-1]}"
            value = value[:-2]
            value.append(file_name)

        value = '/'.join(value)
    return PurePath(value).as_posix()


def file_path(
    value:str,
    strip_trailing_separator:bool=True,
    escape_spaces:bool=False,
    url:bool=False,
    url_encode:bool=False,
    url_decode:bool=False,
    # **kwargs
    )->str:
    '''
        Formats the path for use in windows.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The file path to format.

        [`strip_trailing_separator`=True] {bool}
            if False, the path is allowed to end with a trailing separator.

        [`escape_spaces`=False] {bool}
            if True, any segments of the path that contains a space is wrapped in quotes.

        [`url`=False] {bool}
            if True, the path seperator is set to "/" regardless of the os settings.

        [`url_encode`=False] {bool}
            If True the url is has all special characters encoded.

        [`url_decode`=False] {bool}
            If True the url is has all special characters decoded.



        Return {str}
        ----------------------
        The formatted file path.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:45:08
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: file_path
    '''
    # strip_trailing_separator = _get_kwarg(["strip_trailing_separator"], True, (bool), **kwargs)
    # treat_as_url = _get_kwarg(["url"], False, (bool), **kwargs)
    treat_as_url = url
    # escape_spaces = _get_kwarg(["escape spaces"], False, (bool), **kwargs)
    path_sep = escape_regex(_os.path.sep)
    if treat_as_url is True:
        return format_url(value, url_encode=url_encode,url_decode=url_decode,strip_trailing_separator=strip_trailing_separator)
    # print(f"path_sep: {path_sep}")

    value = PurePath(Path(value)).as_posix()
    value = _re.sub(r'(\\|\/)', path_sep, value)
    regex = _re.compile(rf'{path_sep}+')
    value = _re.sub(regex, path_sep, value)
    # only clean the path for non urls
    if len(value) > 250:
        # print(f"clean path: ",value)
        value = clean_path(value)
        # print(f"clean path: ",value)
    if escape_spaces:
        path_array = value.split(_os.path.sep)
        new_path_array = []
        for seg in path_array:
            seg_string = seg
            if " " in seg_string:
                seg_string = f'"{seg_string}"'
            new_path_array.append(seg_string)
        value = path_sep.join(new_path_array)
    if strip_trailing_separator is True:
        value = strip_end(value, path_sep)
    return value
format_file_path = file_path

def url(value:str,url_encode:bool=False,url_decode:bool=False,strip_trailing_separator:bool=True)->str:
    '''
        Formats a url string

        ----------

        Arguments
        -------------------------
        `value` {str}
            The url to format

        [`encode`=False] {bool}
            If True the url is has all special characters encoded.

        [`decode`=False] {bool}
            If True the url is has all special characters decoded.

        [`strip_trailing_separator`=True] {bool}
            if False, the path is allowed to end with a trailing separator.

        Return {str}
        ----------------------
        The formatted url

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-17-2021 14:28:23
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: url
    '''
    # strip_trailing_separator = _get_kwarg(["strip_trailing_separator"], True, (bool), **kwargs)
    strip_trailing_separator = strip_trailing_separator
    encode = url_encode
    # encode = _get_kwarg(["encode", "url_encode"], False, (bool), **kwargs)
    decode = url_decode
    # decode = _get_kwarg(["decode", "url_decode"], False, (bool), **kwargs)
    path_sep = "/"
    value = _re.sub(r'(\\|\/)', path_sep, value)
    regex = _re.compile(rf'{path_sep}+')
    value = _re.sub(regex, path_sep, value)
    if encode is True:
        value = urllib.parse.quote(value)
    if decode is True:
        value = urllib.parse.unquote(value)

    if strip_trailing_separator is True:
        value = strip_end(value, path_sep)

    return value
format_url = url


def clean_path(path):
    path = path.replace('/', _os.sep).replace('\\', _os.sep)
    path = _re.sub(r'^[\\\?]*','',path)
    if _os.sep == '\\' and '\\\\?\\' not in path:
        # fix for Windows 260 char limit
        relative_levels = len([directory for directory in path.split(_os.sep) if directory == '..'])
        cwd = [directory for directory in _os.getcwd().split(_os.sep)] if ':' not in path else []
        path = '\\\\?\\' + _os.sep.join(cwd[:len(cwd)-relative_levels] + [directory for directory in path.split(_os.sep) if directory != ''][relative_levels:])
        # path = path.replace("\\\\?\\?\\","\\\\?\\")
    path = path.replace("\\\\?\\?\\","\\\\?\\")
    return path
# \\?\?\Z:\Structure\Ra9\2021\21-0132 - EquariUI\EquariUI\EquariUI Beta\equari-beta\node_modules\equari-cryptadia-core\node_modules\preact-router\match\node_modules\.cache\.rts2_cache_cjs\rpt2_73e3afccd1fb4711c5e0a2849dd91b2323492db2\types\cache\0e26fd72fe37b4bfe0d3c7edcd1abb1561780380
# test_path = r"\\?\?\Z:\Structure\Ra9\2021\21-0132 - EquariUI\EquariUI\EquariUI Beta\equari-beta\node_modules\equari-cryptadia-core\node_modules\preact-router\match\node_modules\.cache\.rts2_cache_cjs\rpt2_73e3afccd1fb4711c5e0a2849dd91b2323492db2\types\cache\0e26fd72fe37b4bfe0d3c7edcd1abb1561780380"
# print(file_path(test_path))


def strip_empty_lines(value:str)->str:
    '''
        Strip empty lines from the value.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to strip empty lines from.

        Return {str}
        ----------------------
        The string with empty lines removed.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:42:38
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: strip_empty_lines
        * @xxx [06-03-2022 09:43:29]: documentation for strip_empty_lines
    '''


    lines = value.split("\n")
    new_lines = [x for x in lines if len(x) > 0]
    return '\n'.join(new_lines)



def array_in_string(array, value, default=False)->bool:
    '''
        iterates the array provided checking if any element exists in the value.

        ----------

        Arguments
        -------------------------
        `array` {list}
            The list of terms to search for in the value.
        `value` {str}
            The string to search within
        [`default`=False] {mixed}
            The default value to return if no match is found.

        Return {mixed}
        ----------------------
        True if a match is found, returns the default value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 13:54:36
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: array_in_string
    '''
    if len(array) == 0:
        return default
    if isinstance(value, (str)) is False:
        logger.warning('Second argument of array_in_string, must be a string.')
        logger.warning(value)
        return default
    for item in array:
        if item in value:
            return True
    return default

def array_replace_string(value,needles, new_string="", **kwargs):
    '''
        Replaces any matching substrings found in the needles list with new_string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string that will be modified.

        `needles` {list}
            A list of strings to replace in the the value

        [`new_string`=""] {str}
            What the needle will be replaced with in the value


        Keyword Arguments
        -------------------------
        `max_replace` {int}
            The maximum number of replacements to make.
            if <= 0, it will find and replace all elements in the array.

        Return {str}
        ----------------------
        The formatted string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2022 10:36:28
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: array_replace_string
    '''
    if isinstance(needles,(dict)):
        return dict_replace_string(value,needles)
    max_replace = _get_kwarg(['max','max replace'],0,(int),**kwargs)
    if len(needles) == 0:
        return value

    if isinstance(value, (str)) is False:
        logger.warning('value must be a string.')
        logger.warning(value)

    replace_count = 0
    result_string = value
    for needle in needles:
        if needle in value:
            replace_count += 1
            result_string = result_string.replace(needle,new_string)
            if max_replace > 0:
                if replace_count >= max_replace:
                    return result_string

    return result_string

def dict_replace_string(value:str,replace:dict):
    '''
        Replace all keys with their values in the value string.

        This replacement method will keep replacing until it finds no matches.
        That essentially means that if a previous replacement changes the value that matches a
        different replacement, it will then replace that value and will continue doing so until
        there are no more matches.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to replace values in.

        `replace` {dict}
            The dictionary to use for replacements.

            "find":"replace"


        Return {string|None}
        ----------------------
        The formatted value if successful, None otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-29-2022 05:15:10
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: dict_replace_string
        * @xxx [06-29-2022 05:17:05]: documentation for dict_replace_string
    '''

    if isinstance(replace,(dict)) is False:
        print("The replace argument must be a dictionary","error")
        return None

    match_found = True
    # @Mstep [LOOP] while there are matches still in the value
    while match_found is True:
        match_found = False
        # @Mstep [loop] iterate the replacements
        for k,v in replace.items():
            if v is not None:
                new_val = value.replace(k,v)
                if new_val != value:
                    value = new_val
                    match_found = True
    return value

def plural_noun(value:str):
    '''
        Convert the string (noun) to its plural equivalent.

        This uses the inflect library to perform the smart stuff..

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to convert to plural

        Return {str}
        ----------------------
        The plural equivalent of the noun.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-05-2022 07:56:17
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: plural_noun
        * @xxx [07-05-2022 07:58:44]: documentation for plural_noun
    '''

    p = inflect_engine()
    return p.plural_noun(value)

def singular_noun(value:str):
    '''
        Convert a string (noun) to its singular equivalent.

        This uses the inflect library to perform the smart stuff..

        Arguments
        -------------------------
        `value` {str}
            The string to convert to singular.

        Return {str}
        ----------------------
        The singular equivalent of the noun.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-05-2022 07:54:50
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: singular_noun
        * @xxx [07-05-2022 07:59:39]: documentation for singular_noun
    '''


    p = inflect_engine()
    return p.singular_noun(value)


def replace_end(subject,target,replace=""):
    '''
        Replace a substring from the end of the subject.
        ----------

        Arguments
        -------------------------
        `subject` {str}
            The string to perform the replacement on.
        `target` {str}
            The value to search for in the subject
        [`replace`=""] {str}
            The value to replace the target with.


        Return {str}
        ----------------------
        The subject with the target replaced if it is found.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 11-29-2022 11:02:07
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: replace_end
        * @xxx [11-29-2022 11:06:10]: documentation for replace_end
    '''
    tlen = len(target)
    # @Mstep [if] if the subject is less than the target
    if len(subject) < tlen:
        # @Mstep [RETURN] return the subject.
        return subject
    # @Mstep [] get the last n characters of the subject
    last = subject[tlen*-1:].lower()
    # @Mstep [IF] if the target ends with the last string.
    if last == target.lower():
        # @Mstep [] get the precedeing characters
        value = subject[:tlen*-1]
        # @Mstep [] concatenate the replace onto the value
        value = f"{value}{replace}"
        # @Mstep [RETURN] return the value
        return value
    # @Mstep [RETURN] return the subject.
    return subject


def convert_a_to_an(subject):
    return _re.sub(r"a\s([aeiouy])",r"an \1",subject)


