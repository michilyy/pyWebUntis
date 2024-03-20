from typing import Union



class UntisError(Exception):

    # error code | untis Definition             | Hint
    table = {
        '-8500': [ 'InvalidSchool',             ""],
        '-8502': [ 'NoSpecifiedUser',           ""],
        '-8504': [ 'InvalidPassword',           ""],
        '-8509': [ 'NoRight',                   ""],
        '-8511': [ 'LockedAccess',              ""],
        '-8520': [ 'RequiredAuthentication',    ""],
        '-8521': [ 'AuthenticationError',       ""],
        '-8523': [ 'NoPublicAccess',            ""],
        '-8524': [ 'InvalidClientTime',         ""],
        '-8525': [ 'InvalidUserStatus',         ""],
        '-8526': [ 'InvalidUserRole',           ""],
        '-7001': [ 'InvalidTimeTableType',      ""],
        '-7002': [ 'InvalidElementId',          ""],
        '-7003': [ 'InvalidPersonType',         ""],
        '-7004': [ 'InvalidDate',               ""],
        '-8998': [ 'UnspecifiedError',          ""],
        '-6003': [ 'TooManyResults',            ""],
    }


    def __init__(self, code:Union[str, int], message=None, *args) -> None:
        code = str(code)
        error = ["undefined error", f"error code {code}", "please file a bug report"]

        if code in self.table:
            error = self.table[code]



        super().__init__(*error, message, *args)