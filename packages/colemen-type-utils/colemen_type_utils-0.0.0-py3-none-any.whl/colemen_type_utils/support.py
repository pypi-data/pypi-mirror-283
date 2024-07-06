'''
Methods that do not directly serve a purpose in this library but help get shit done.
'''



from ctypes import Union
import re




def is_integer(value:Union[str,int],negatives=True):
    '''
        Determine if the value provided is an integer.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.

        Return {bool}
        ----------------------
        True if the value is an integer or string containing an integer, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:38:36
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_integer
        * @xxx [01-06-2023 09:39:49]: documentation for is_integer
    '''

    if isinstance(value,(int)):
        if negatives is False:
            if value < 0:
                return False
        return True

    # @Mstep [] determine the appropriate regex to use.
    reg = r'^[0-9]*$'

    if negatives is True:
        reg = r'^[0-9-]*$'


    # @Mstep [IF] if the value is a string.
    if isinstance(value,(str)):
        # @Mstep [] strip leading and trailing spaces.
        value = strip(value,[" "])
        return False if re.match(reg,value) is None else True

def is_float(value:Union[str,float],negatives=True):
    '''
        Determine if the value provided is a float.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.

        Return {bool}
        ----------------------
        True if the value is an float or string containing an float, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:38:36
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_float
        * @xxx [01-06-2023 09:39:49]: documentation for is_float
    '''

    if isinstance(value,(int)):
        if negatives is False:
            if value < 0:
                return False
        return True

    if isinstance(value,(str)):

        # @Mstep [] determine the appropriate regex to use.
        reg = r'^[0-9]*\.[0-9]*$'

        if negatives is True:
            reg = r'^[0-9-]*\.[0-9]*$'

        # @Mstep [] strip leading and trailing spaces.
        value = strip(value,[" "])
        return False if re.match(reg,value) is None else True
    return isinstance(value,(int))

def strip(value:str,chars:list,side='both'):
    '''
        Strips characters/strings from the beginning,end or both sides of a string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The value to be formatted

        `chars` {list}
            A list of strings to be stripped from the value

        [`side`='both'] {str}
            Can be "left", "right", "both"

        Return {str}
        ----------------------
        The formatted value.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-04-2022 10:25:04
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: strip_any
    '''
    new_value = value
    cycle = True
    if side in ["both","left"]:
        cycle = True
        while cycle is True:
            matchFound = False
            for char in chars:
                if new_value.startswith(char):
                    new_value = new_value[len(char):]
                    matchFound = True
                else:
                    continue
            if matchFound is False:
                cycle = False
    if side in ["both","right"]:
        cycle = True
        while cycle is True:
            matchFound = False
            for char in chars:
                if new_value.endswith(char):
                    new_value = new_value[:-len(char)]
                    matchFound = True
                else:
                    continue
            if matchFound is False:
                cycle = False
    return new_value
