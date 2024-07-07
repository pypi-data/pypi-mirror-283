
'''
The master control settings for colemen_string_utils
'''




from colemen_string_utils.settings.types import _inflect_engine_type


INFLECT_ENGINE = None
'''The singleton instance of the inflect engine'''



def inflect_engine()->_inflect_engine_type:
    '''
        Create a singleton instance of the inflect engine.

        ----------

        Return {type}
        ----------------------
        The instance of the inflect engine.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 07-05-2022 08:42:21
        `memberOf`: colemen_config
        `version`: 1.0
        `method_name`: inflect_engine
        * @xxx [07-05-2022 08:44:27]: documentation for inflect_engine
    '''
    global INFLECT_ENGINE

    if INFLECT_ENGINE is None:
        import inflect
        INFLECT_ENGINE = inflect.engine()

    return INFLECT_ENGINE

