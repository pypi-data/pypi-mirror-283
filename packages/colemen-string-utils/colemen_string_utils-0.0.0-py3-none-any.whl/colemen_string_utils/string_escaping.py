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
from datetime import datetime
import logging as _logging
import re
from sre_compile import isstring
# from typing import Union as _Union
# import re as _re
# import os as _os
# import urllib.parse

# import colemen_utilities.dict_utils as _obj
from colemen_string_utils.support import get_kwarg as _get_kwarg,_rand,_rand_number
# import colemen_utilities.string_utils as _csu
from colemen_string_utils.string_parsing import get_quoted_substrings as _get_quoted_substrings

# import colemen_utilities.random_utils as _ran
from pyparsing import QuotedString
# from pyparsing import And, Suppress,Dict, Word, Literal, Group, Optional, ZeroOrMore, OneOrMore, Regex, restOfLine, alphanums,nums, printables, string, CaselessKeyword,nestedExpr,ParseException,quotedString,removeQuotes,originalTextFor,delimitedList,QuotedString

# from colemen_utilities.dict_utils.dict_utils import get_kwarg as _get_kwarg

logger = _logging.getLogger(__name__)

_numeric_char_codes = {
    "symbols":{
        ";":"&#59;",
        "#":"&#35;",
        "&":"&#38;",
        "!":"&#33;",
        "\"":"&#34;",
        "$":"&#36;",
        "%":"&#37;",
        "'":"&#39;",
        "(":"&#40;",
        ")":"&#41;",
        "*":"&#42;",
        "+":"&#43;",
        ",":"&#44;",
        "-":"&#45;",
        ".":"&#46;",
        "/":"&#47;",
        ":":"&#58;",
        "<":"&#60;",
        "=":"&#61;",
        ">":"&#62;",
        "?":"&#63;",
        "@":"&#64;",
        "[":"&#91;",
        "\\":"&#92;",
        "]":"&#93;",
        "^":"&#94;",
        "_":"&#95;",
        "`":"&#96;",
        "{":"&#123;",
        "|":"&#124;",
        "}":"&#125;",
        "~":"&#126;"
    },
    "numeric":{
        "0":"&#48;",
        "1":"&#49;",
        "2":"&#50;",
        "3":"&#51;",
        "4":"&#52;",
        "5":"&#53;",
        "6":"&#54;",
        "7":"&#55;",
        "8":"&#56;",
        "9":"&#57;"
    },
    "upper_case":{
        "A":"&#65;",
        "B":"&#66;",
        "C":"&#67;",
        "D":"&#68;",
        "E":"&#69;",
        "F":"&#70;",
        "G":"&#71;",
        "H":"&#72;",
        "I":"&#73;",
        "J":"&#74;",
        "K":"&#75;",
        "L":"&#76;",
        "M":"&#77;",
        "N":"&#78;",
        "O":"&#79;",
        "P":"&#80;",
        "Q":"&#81;",
        "R":"&#82;",
        "S":"&#83;",
        "T":"&#84;",
        "U":"&#85;",
        "V":"&#86;",
        "W":"&#87;",
        "X":"&#88;",
        "Y":"&#89;",
        "Z":"&#90;"
    },
    "lower_case":{

        "a":"&#97;",
        "b":"&#98;",
        "c":"&#99;",
        "d":"&#100;",
        "e":"&#101;",
        "f":"&#102;",
        "g":"&#103;",
        "h":"&#104;",
        "i":"&#105;",
        "j":"&#106;",
        "k":"&#107;",
        "l":"&#108;",
        "m":"&#109;",
        "n":"&#110;",
        "o":"&#111;",
        "p":"&#112;",
        "q":"&#113;",
        "r":"&#114;",
        "s":"&#115;",
        "t":"&#116;",
        "u":"&#117;",
        "v":"&#118;",
        "w":"&#119;",
        "x":"&#120;",
        "y":"&#121;",
        "z":"&#122;"
    }
}



def regex(value:str)->str:
    '''
        Escapes regex special characters.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to escape.

        Return {str}
        ----------------------
        The formatted string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:46:32
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: escape_regex
    '''
    regex_chars = ["\\", "^", "$", "{", "}", "[", "]", "(", ")", ".", "*", "+", "?", "<", ">", "-", "&"]
    for char in regex_chars:
        value = value.replace(char, f"\\{char}")
    return value
escape_regex = regex

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

        Example
        ----------------------
        hey/there's/you/"sexy" beast

        result:
        hey/there&apos;s/you/&quot;sexy&quot; beast

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

def reverse_sanitize_quotes(string):
    orig_list = False
    if isinstance(string, (list)):
        orig_list = True
    if isinstance(string, (str)):
        string = [string]

    new_list = []
    for item in string:
        item = item.replace("&apos_", "'")
        item = item.replace("&quot_", '"')
        new_list.append(item)

    if len(new_list) == 1 and orig_list is False:
        return new_list[0]

    return new_list

def sanitize_quotes(value):
    orig_list = False
    if isinstance(value,(int,float,bool)) is True:
        return value
    if value is None:
        return value

    if isinstance(value, (list)):
        orig_list = True
    if isinstance(value, (str)):
        value = [value]

    new_list = []

    if isinstance(value,datetime):
        return value
    for item in value:
        if isinstance(item, (str)):
            item = item.replace("'", "&apos_")
            item = item.replace('"', "&quot_")
        new_list.append(item)

    if len(new_list) == 1 and orig_list is False:
        return new_list[0]

    return new_list

def _get_numeric_charcode(char):
    for _,v in _numeric_char_codes.items():
        for c,code in v.items():
            if c == char:
                return code
    return None

def _get_numeric_charcode_chars(cat:str)->list:
    output = []
    if cat in _numeric_char_codes:
        for k,_ in _numeric_char_codes[cat].items():
            output.append(k)
    return output

def escape_charcode(value:str,reverse=False,**kwargs)->str:
    '''
        Escape character in a string with their character codes.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to escape.

        [`reverse`=False] {bool}
            If True, it will unescape the charcoded characters.

        Keyword Arguments
        -------------------------
        [`chars`=None] {list|str}
            A list or string of characters to escape.

        [`quote`=None] {str}
            If a quote character is provided, it will only escape characters that are quoted with this char.

        [`symbols`=True] {bool}
            If True, all symbols will be escaped.

        [`numeric`=False] {bool}
            If True, all numeric will be escaped.

        [`upper_case`=False] {bool}
            If True, all upper_case will be escaped.

        [`lower_case`=False] {bool}
            If True, all lower_case will be escaped.

        Return {str}
        ----------------------
        The escaped string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 09:36:42
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: escape_charcode
        * @xxx [06-04-2022 09:38:48]: documentation for escape_charcode
    '''

    if reverse is True:
        return charcode_unescape(value)

    quote_char = _get_kwarg(["quote","quote char"], None, (str), **kwargs)
    chars = _get_kwarg(["chars"], None, (list,str), **kwargs)
    symbols = _get_kwarg(["symbols"], True, (bool), **kwargs)
    numeric = _get_kwarg(["numeric"], False, (bool), **kwargs)
    upper_case = _get_kwarg(["upper_case"], False, (bool), **kwargs)
    lower_case = _get_kwarg(["lower_case"], False, (bool), **kwargs)

    if quote_char is not None and len(quote_char) == 1:
        quotes = _get_quoted_substrings(value,quote_char)
        if quotes is None:
            return value
        if len(quotes) > 0:
            for q in quotes:
                quote_value = escape_charcode(
                    q,
                    reverse,
                    chars=chars,
                    symbols=symbols,
                    numeric=numeric,
                    upper_case=upper_case,
                    lower_case=lower_case
                    )
                value = value.replace(q,quote_value)
            return value


    if chars is not None:
        if isinstance(chars,(str)):
            chars = chars.split()
        for c in chars:
            code = _get_numeric_charcode(c)
            value = value.replace(c,code)
        return value

    chars = []

    if symbols is True:
        chars = chars + _get_numeric_charcode_chars('symbols')
    if numeric is True:
        chars = chars + _get_numeric_charcode_chars('numeric')
    if upper_case is True:
        chars = chars + _get_numeric_charcode_chars('upper_case')
    if lower_case is True:
        chars = chars + _get_numeric_charcode_chars('lower_case')

    for c in chars:
        code = _get_numeric_charcode(c)
        value = value.replace(c,code)

    return value
charcode = escape_charcode

def charcode_unescape(value:str)->str:
    '''
        Unescape the character codes from escape_charcode.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to unescape.

        Return {str}
        ----------------------
        The unescaped string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 09:39:02
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: charcode_unescape
        * @xxx [06-04-2022 09:39:50]: documentation for charcode_unescape
    '''

    for _,v in _numeric_char_codes.items():
        for c,code in v.items():
            value = value.replace(code,c)
    return value

def quoted_commas(value,escape_value="__ESCAPED_COMMA__",reverse=False):
    '''
        Escape commas that are located within quotes.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to search within
        [`escape_value`='__ESCAPED_COMMA__] {str}
            The value to replace commas with.
        `reverse` {bool}
            if True it will replace the escaped commas with actual commas.

        Return {str}
        ----------------------
        The string with escaped commas.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 06:54:48
        `memberOf`: parse_sql
        `version`: 1.0
        `method_name`: escape_quoted_commas
        @xxx [06-01-2022 06:57:45]: documentation for escape_quoted_commas
    '''

    if reverse is True:
        return value.replace(escape_value,",")

    sql_qs = QuotedString("'", esc_quote="''")
    quote = sql_qs.search_string(value)
    if len(quote) > 0:
        quote = quote.asList()
        for q in quote:
            if len(q) == 1:
                q = q[0]
            esc = q.replace(",",escape_value)
            value = value.replace(q,esc)

    return value
escape_quoted_commas = quoted_commas



def compress(string):
    index = 0
    compressed = ""
    len_str = len(string)
    while index != len_str:
        char = string[index]
        count = 1
        while (index < len_str-1) and (char == string[index+1]):
            count = count + 1
            index = index + 1
        if count == 1:
            compressed += str(char)
        elif count == 2:
            compressed += str(char) + str(char)
        else:
            compressed += str(char) + str(count)
        index = index + 1
    return compressed

def decompress(value:str):
    if isinstance(value,(str)) is False:
        value = str(value)
    match = re.findall(r'([A-Z]{1})([0-9]+)',value)
    if len(match) > 0:
        for m in match:
            val = m[0] * int(m[1])
            value = value.replace(f"{m[0]}{m[1]}",val)
    return value

numerals = [
    ["0","Z"],
    ["1","R"],
    ["2","I"],
    ["3","P"],
    ["4","F"],
    ["5","B"],
    ["6","M"],
    ["7","C"],
    ["8","Q"],
    ["9","G"],
]
num_codes = [x[1] for x in numerals]

def string_encode_int(value,min_len=12)->str:
    '''
        Encode the integer value into string of uppercase characters with the length specified.
        ----------

        Arguments
        -------------------------
        `value` {int}
            The value to encode

        [`min_len`=12] {int}
            How many characters the string must be.
            This has no effect if the value's length is greater than the minimum (it will not trim)

        Return {str}
        ----------------------
        The value encoded to letters.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-20-2023 12:34:25
        `memberOf`: DeleteMe_hashID_test
        `version`: 1.0
        `method_name`: string_encode_int
        * @xxx [02-20-2023 12:36:47]: documentation for string_encode_int
    '''
    value = str(value)
    # @Mstep [] remove all non-numeric characters from the value.
    value = re.sub(r'[^0-9]','',value)
    # @Mstep [LOOP] iterate the numerals list.
    for num in numerals:
        # @Mstep [] replace each number with its corresponding letter.
        value = value.replace(num[0],num[1])
    # @Mstep [] compress the value
    value = compress(value)

    # @Mstep [IF] if the value is shorter than the minimum length
    if len(value) < min_len:
        # @Mstep [] generate the num_codes list.
        # num_codes = [x[1] for x in numerals]
        # @Mstep [] calculate how many pad characters are needed.
        delta = min_len - len(value)



        # @Mstep [loop] iterate the num_code_characters
        # This groups the characters by adding a comma before each letter
        # doing so forces the padding to place random characters around letters followed by numbers.
        # RIMQNGQ4ISYQ = Q,N,G,Q4,I,S
        for k in num_codes:
            # @Mstep [] replace all num_code chars with prefixed comma
            value = value.replace(k,f",{k}")
        vlist = value.split(",")

        # @Mstep [LOOP] range loop the delta characters
        for _ in range(delta):
            # @Mstep [] randomly select a position to place the new character.
            pos = _rand_number(0,len(vlist))
            # @Mstep [] randomly select a padding character that is not num_code
            pad = _rand(1,lower_case=False,digits=False,exclude=num_codes)
            # @Mstep [] insert the padding character
            vlist.insert(pos,pad)

        # @Mstep [] compile the character list into a string.
        value = ''.join(vlist)

    # @Mstep [RETURN] return the encoded string.
    return value

def string_decode_int(value:str)->int:
    '''
        Decode a string encoded by string_encode_int
        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to decode

        Return {int}
        ----------------------
        The decoded integer value.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-20-2023 12:36:56
        `memberOf`: DeleteMe_hashID_test
        `version`: 1.0
        `method_name`: string_decode_int
        * @xxx [02-20-2023 12:37:51]: documentation for string_decode_int
    '''
    # pad_chars = ['A', 'D', 'E', 'H', 'J', 'K', 'L', 'N', 'O', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    # @Mstep [] decompress the string.
    value = decompress(value)


    # num_codes = [x[1] for x in numerals]
    # @Mstep [] remove all padding characters from the value.
    new_val = []
    # @Mstep [LOOP] iterate the characters in the value.
    for char in list(value):
        # @Mstep [IF] if the character is a num_code
        if char in num_codes:
            # @Mstep [] append the character to the new_val list.
            new_val.append(char)
    # @Mstep [] join the new_val list into a string.
    value = ''.join(new_val)

    for num in numerals:
        value = value.replace(num[1],num[0])

    num = value
    value = re.sub(r'[^0-9]','',value,re.IGNORECASE)
    if len(value) == 0:
        return None
    num = int(value)
    return num




# def quoted_chars_adv(value,**kwargs):


#     reverse = _get_kwarg(["reverse"], False, (bool), **kwargs)
#     quote_char = _get_kwarg(["quote char","quote"], None, (str), **kwargs)
#     chars = _get_kwarg(["chars"], None, (list,str), **kwargs)
#     symbols = _get_kwarg(["symbols"], True, (bool), **kwargs)
#     numeric = _get_kwarg(["numeric"], False, (bool), **kwargs)
#     upper_case = _get_kwarg(["upper_case"], False, (bool), **kwargs)
#     lower_case = _get_kwarg(["lower_case"], False, (bool), **kwargs)

#     if chars is not None:
#         if isinstance(chars,(str)):
#             chars = chars.split()
#         for c in chars:
#             code = _get_numeric_charcode(c)
#             value = value.replace(c,code)
#         return value

#     if reverse is True:
#         for e in escapes:
#             value = value.replace(e[1],e[0])
#         return value

#     for e in escapes:
#         sql_qs = QuotedString("'", esc_quote="''")
#         quote = sql_qs.search_string(value)
#         if len(quote) > 0:
#             quote = quote.asList()
#             # print(f"quote: {quote}")
#             for q in quote:
#                 if len(q) == 1:
#                     q = q[0]
#                 esc = q.replace(e[0],e[1])
#                 value = value.replace(q,esc)
#     # print(sql_qs.search_string(value))
#     return value



def unicode_to_html(value:str,**kwargs)->str:
    '''
        Convert unicode characters to HTML encoded characters.

        ----------

        Arguments
        -------------------------
        `value` {str,dict}
            The string to format.

        Keyword Arguments.
        -------------------------
        [`semicolon`=false] {bool}
            Replace the semicolon character with __SEMI_COLON__.
            This is useful for sql related stuff, so you can replace the semicolons used in HTML.


        Return {str}
        ----------------------
        The string with unicode chars replaced with HTML encoded chars.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 08:10:2022 11:48:42
        `version`: 0.0.1
        `method_name`: unicode_to_html
        * @TODO []: documentation for unicode_to_html
    '''

    if value is None:
        return value

    if isinstance(value,(bool,int,float)):
        return value

    if isinstance(value,(list)):
        output = []
        for v in value:
            output.append(unicode_to_html(v))
        return output

    if isinstance(value,(dict)):
        output = {}
        for k,v in value.items():
            output[k] = unicode_to_html(v)
        return output

    if isinstance(value,(str)):
        semicolon = _get_kwarg(["semicolon"],False,(bool),**kwargs)
        value = value.encode('ascii', 'xmlcharrefreplace').decode()
        if semicolon is True:
            value = value.replace(";","__SEMI_COLON__")
        return value




def quoted_chars(value,reverse=False):
    '''
        Escape characters that can effect parsing which are located within quotes.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to search within

        `reverse` {bool}
            if True it will reverse the escaped chars with their actual chars.

        Return {str}
        ----------------------
        The string with escaped chars.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 06:54:48
        `memberOf`: parse_sql
        `version`: 1.0
        `method_name`: escape_quoted_chars
        @xxx [06-01-2022 06:57:45]: documentation for escape_quoted_chars
    '''

    #we dont fuck with these sneaky hobbitses
    if isinstance(value,(bool,int,float)):
        return value

    if isinstance(value,(dict)):
        output = {}
        for k,v in value.items():
            output[quoted_chars(k)] = quoted_chars(v)
        return output


    if isinstance(value,(list)):
        output = []
        for v in value:
            output.append(quoted_chars(v))
        return output

    if isinstance(value,(str)):

        escapes = [
            [",","__&#44__"],
            [";","__&#59__"],
            ["(","__&#40__"],
            [")","__&#41__"],
            ["`","__&#96__"],
            ['"',"__&#34__"],
            ["'","__&#39__"],
        ]


        if reverse is True:
            for e in escapes:
                value = value.replace(e[1],e[0])
            return value

        for e in escapes:
            sql_qs = QuotedString("'", esc_quote="''")
            quote = sql_qs.search_string(value)
            if len(quote) > 0:
                quote = quote.asList()
                # print(f"quote: {quote}")
                for q in quote:
                    if len(q) == 1:
                        q = q[0]
                    esc = q.replace(e[0],e[1])
                    # print(f"valuevalue: {value}")
                    value = value.replace(q,esc)
        # print(sql_qs.search_string(value))
        return value
escape_quoted_chars = quoted_chars












