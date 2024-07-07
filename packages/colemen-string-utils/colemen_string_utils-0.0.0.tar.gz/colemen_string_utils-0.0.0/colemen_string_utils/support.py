




from typing import Union
import string as _string
import random as _random


def keys_to_lower(dictionary):
    '''
        Converts all keys in a dictionary to lowercase.
    '''
    return {k.lower(): v for k, v in dictionary.items()}




def get_kwarg(key_name:Union[list,str], default_val=False, value_type=None, **kwargs):
    '''
        Get a kwarg argument that optionally matches a type check or
        return the default value.

        ----------

        Arguments
        -------------------------
        `key_name` {list|string}
            The key name or a list of key names to search kwargs for.

        [`default_val`=False] {any}
            The default value to return if the key is not found or fails
            the type check (if provided.)

        [`value_type`=None] {any}
            The type or tuple of types.
            The kwarg value must match at least one of these.
            Leave as None to ignore type checking.
        `kwargs` {dict}
            The kwargs dictionary to search within.

        Return {any}
        ----------------------
        The value of the kwarg key if it is found.
        The default value if the key is not found or its value fails type checking.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 08:33:36
        `memberOf`: objectUtils
        `version`: 1.0
        `method_name`: get_kwarg
        * @xxx [06-03-2022 08:38:33]: documentation for get_kwarg
    '''

    kwargs = keys_to_lower(kwargs)
    if isinstance(key_name, list) is False:
        key_name = [key_name]

    for name in key_name:
        if name in kwargs:
            if value_type is not None:
                if isinstance(kwargs[name], value_type) is True:
                    return kwargs[name]
            else:
                return kwargs[name]
    return default_val


def rand(length=12, **kwargs):
    '''
        Generates a cryptographically secure random _string.


        ----------
        Arguments
        -----------------
        `length`=12 {int}
            The number of characters that the string should contain.

        Keyword Arguments
        -----------------
        `upper_case`=True {bool}
            If True, uppercase letters are included.
            ABCDEFGHIJKLMNOPQRSTUVWXYZ

        `lower_case`=True {bool}
            If True, lowercase letters are included.
            abcdefghijklmnopqrstuvwxyz

        `digits`=True {bool}
            If True, digits are included.
            0123456789

        `symbols`=False {bool}
            If True, symbols are included.
            !"#$%&'()*+,-./:;<=>?@[]^_`{|}~

        `exclude`=[] {string|list}
            Characters to exclude from the random _string.

        Return
        ----------
        `return` {str}
            A random string of N length.
    '''

    uppercase = get_kwarg(['upper case', 'upper'], True, bool, **kwargs)
    lowercase = get_kwarg(['lower case', 'lower'], True, bool, **kwargs)
    digits = get_kwarg(['digits', 'numbers', 'numeric', 'number'], True, bool, **kwargs)
    symbols = get_kwarg(['symbols', 'punctuation'], False, bool, **kwargs)
    exclude = get_kwarg(['exclude'], [], (list, str), **kwargs)

    choices = ''
    if uppercase is True:
        choices += _string.ascii_uppercase
    if lowercase is True:
        choices += _string.ascii_lowercase
    if digits is True:
        choices += _string.digits
    if symbols is True:
        choices += _string.punctuation

    if len(exclude) > 0:
        if isinstance(exclude, str):
            exclude = list(exclude)
        for exd in exclude:
            choices = choices.replace(exd, '')

    return ''.join(_random.SystemRandom().choice(choices) for _ in range(length))

def number(minimum=1,maximum=100):
    if minimum > maximum:
        maximum = minimum + maximum
    return _random.randint(minimum,maximum)
integer = number


def remove_keys(data:dict,keys:Union[list,str],reverse:bool=False,comp_values:bool=False)->dict:
    '''
        Remove matching keys from a dictionary or keep only the matching keys.

        ----------

        Arguments
        -------------------------
        `data` {dict}
            The dictionary to filter.

        `keys` {list|str}
            A key or list of keys that will be removed from the dictionary.

        [`reverse`=False] {bool}
            If True, all keys except the ones provided will be removed.

        [`comp_values`=False] {bool}
            If True, remove keys based on their values


        Return {dict}
        ----------------------
        The dict with keys filtered.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 10:15:45
        `memberOf`: dict_utils
        `version`: 1.0
        `method_name`: remove_keys
        * @xxx [06-04-2022 10:23:17]: documentation for remove_keys
    '''
    # reverse = get_kwarg(['reverse'], False, (bool), **kwargs)
    # comp_values = get_kwarg(['comp_values'], False, (bool), **kwargs)
    keys = force_list(keys)


    output = {}
    for k,v in data.items():
        if comp_values is False:
            if reverse is True:
                if k in keys:
                    output[k] = v
            else:
                if k not in keys:
                    output[k] = v
        else:
            if reverse is True:
                if v in keys:
                    output[k] = v
            else:
                if v not in keys:
                    output[k] = v

    return output


def force_list(value,allow_nulls=True)->list:
    '''
        Confirm that the value is a list, if not wrap it in a list.

        ----------

        Arguments
        -------------------------
        `value` {any}
            The value to test.

        [`allow_nulls`=True] {bool}
            If False and the value is null, the list will be empty.

        Return {list}
        ----------------------
        The value as a list

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:13:57
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: force_list
        * @xxx [06-03-2022 09:14:52]: documentation for force_list
    '''
    if value is None and allow_nulls is False:
        return []

    if isinstance(value,(tuple)) is True:
        return list(value)
    if isinstance(value,(list)) is False:
        return [value]
    return value



def option(options:list,count:int=1,allow_repeats:bool=False,default=None)->any:
    '''
        Select a random option from a list.

        ----------

        Arguments
        -------------------------
        `options` {list}
            The list or dictionary to select from.

        [`count`=1] {int}
            How many random options to select.

        [`allow_repeats`=False] {bool}
            If True, the result can contain the same option multiple times.

        [`default`=None] {any}
            This is the value returned if options is an empty list.

        Return {any}
        ----------------------
        The random option or a list of random options if `count` is greater than one.\n
        returns `default` if there are no options.


        Examples
        ----------------------

        options = ["kitties","and","titties"]\n

        _obj.rand_option(options)\n
        // 'titties'\n

        _obj.rand_option(options,count=2)\n
        // ['kitties', 'and']\n

        _obj.rand_option(options,count=8)\n
        // ['kitties', 'and', 'titties']\n

        _obj.rand_option(options,count=6,repeats=True)\n
        // ['titties', 'kitties', 'titties', 'and', 'kitties', 'and']\n

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 08:01:13
        `memberOf`: _objectUtils
        `version`: 1.0
        `method_name`: rand_option
        * @xxx [06-03-2022 08:33:02]: documentation for rand_option
    '''

    # count = _obj.get_kwarg(['count'], 1, (int), **kwargs)
    # allow_repeats = _obj.get_kwarg(['allow repeats','repeats'], False, (bool), **kwargs)
    # default = _obj.get_kwarg(['default'], None, None, **kwargs)
    # keys = _obj.get_kwarg(['keys','return keys'], False, (bool), **kwargs)

    # TODO []: add support for dictionaries
    # if isinstance(options,(dict)):
    #     is_dict = True
    #     return options[random_key(options)]


    olen = len(options)

    # @Mstep [IF] if there are no options.
    if olen == 0:
        # @Mstep [RETURN] return None.
        return default

    # @Mstep [IF] if the option length is less than or equal to the selection count.
    if olen <= count:
        # @Mstep [if] if repeats are not allowed.
        if allow_repeats is False:
            # @Mstep [] set the selection count to the number of options.
            count = olen

    # @Mstep [IF] if the count is equal to the options length
    if count == olen:
        # @Mstep [IF] if the selection count is one
        if count == 1:
            # @Mstep [return] return the only available option.
            return options[0]
        return options

    selection = []

    while len(selection) != count:
        select = options[_random.randint(0, olen-1)]
        if allow_repeats is False and select not in selection:
            selection.append(select)
        elif allow_repeats is True:
            selection.append(select)


    if len(selection) == 1:
        return selection[0]
    return selection

