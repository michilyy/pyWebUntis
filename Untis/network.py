import datetime
import time
import regex
from typing import Union
import requests
import base64
import Untis.error






class API:
    # requests data
    session = requests.Session()
    session.headers = {
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.11.0"
    }

    server: str = None
    untisID = "untis-mobile-blackberry-2.7.4"

    # auth data default anonymous
    username: str
    password: str


    def __init__(self: object, server: str , loginName:str, username:str="#anonymous#", password:str="", **kwargs):
        """
        Init function for School class. Stores only Api related information specific attributes and functions
        :param server: base server url
        :param loginName: identifier name from school
        :param username: username of used default "#anonymous#"
        :param password: password of user default ""
        :param kwargs: will get ignored
        """

        self.server = server
        self.loginName = loginName

        self.username = username
        self.password = password


    # helper functions
    def get_school_data(self):
        """
        Search school with the given string.
        :return: list with school objects
        """
        baseurl = "https://schoolsearch.webuntis.com/schoolquery2"
        json = {
            "id": f"{self.untisID}",
            "jsonrpc": "2.0",
            "method": "searchSchool",
            "params": [{
                "search": f"{self.loginName}"
            }]
        }

        data = self.session.post(url=baseurl, json=json).json()
        return data["result"]["schools"][0]

    def auth(self) -> dict:
        """
        helper function creates auth dict
        :return: dict
        """

        # TODO do some research how calculate otp for non anonymous user
        auth = {
            "clientTime": int(time.time() * 1000),
            "otp": 0,
            "user": f"{self.username}"
        }

        return auth

    def _getMoSofromDate(self, date: datetime.datetime) -> list[datetime.date, datetime.date]:
        """
        Gets date of Monday and Sunday of week
        :param date: the given date to calculate monday and sunday
        :return: list with monday and sunday date
        """

        # get datetime.date from given object
        # calculate monday
        # calculate friday

        date = date.date() if isinstance(date, datetime.datetime) else date

        mon = date - datetime.timedelta(days=date.weekday())
        son = date + datetime.timedelta(days=6 - date.weekday())

        return [mon, son]

    def _date_iter(self,
                   end: datetime.date, start: datetime.date = datetime.date.today(),
                   delta: datetime.timedelta = datetime.timedelta(days=7)
                   ) -> list[datetime.date, datetime.date]:
        """
        Iter dates from start
        :param end: datetime.date object beginning the iteration
        :param args: start:datetime.date, steps=datetime.timedelta
        :param kwargs: end:datetime.date, steps=datetime.timedelta
        :return: list with monday and sunday dates
        """

        current = start
        while current < end:
            result = self._getMoSofromDate(current)
            yield result
            current = current + delta



    ## API functions
    # default requests function
    def _requests(self, method: str, params: dict = None, auth:bool=True) -> dict:
        """
        Creates default requests for untis server
        :param method: method which get used
        :param params: params for request
        :param auth: default True only false for login
        :return: dict
        :raise UntisError when requests return error
        """

        url = f"https://{self.server}/WebUntis/jsonrpc_intern.do"
        url_params = {
            "school": f"{self.loginName}",
            "m": f"{method}",
            "a": "true",  # TODO: Why?
            "s": f"{self.server}",
            "v": "i5.12.3"
        }

        values = []
        if auth:
            values = [{
                "auth": self.auth()
            }]

        params and values[0].update(params)


        data = {
            "id": self.untisID,
            "jsonrpc": "2.0",
            "method": f"{method}",
            "params": values
        }

        result = self.session.post(url=url, params=url_params, json=data)
        result = result.json()

        if "error" in result:
            error = result["error"]
            raise Untis.error.UntisError(code=error["code"], message=error["message"])

        return result["result"]


    def createImmediateAbsence(self):
        """"""
        """ params
        val periodId: Int,
		val studentId: Int,
		val startTime: UntisTime,
		val endTime: UntisTime,
		"""
        
        # TODO
        result = self._requests(method="createImmediateAbsence2017")
        return result


    def deleteAbsence(self):
        """"""
        """ params
        val absenceId: Int,
        """

        #TODO
        result = self._requests(method="deleteAbsence2017")
        return result


    def getStudentAbsences(self):
        """"""
        """ params
        val startDate: UntisDate,
		val endDate: UntisDate,
		val includeExcused: Boolean,
		val includeUnExcused: Boolean,
		"""
        #TODO
        result = self._requests(method="getStudentAbsences2017")
        return result


    def submitAbsencesChecked(self):
        """"""
        
        """ params
        val ttIds: List<Int>
        """
        
        #TODO
        result = self._requests(method="submitAbsencesChecked2017")
        return result


    def getLessonTopic(self):
        """"""
        # TODO: Params
        #TODO
        result = self._requests(method="getLessonTopic2017")
        return result


    def submitLessonTopic(self):
        """"""

        """ params
        val lessonTopic: String,
		val ttId: Int,
		"""

        #TODO
        result = self._requests(method="submitLessonTopic")
        return result


    def getOfficeHours(self):
        """"""
        """ params
        val klasseId: Int,
		val startDate: UntisDate
        """
        #TODO
        result = self._requests(method="getOfficeHours2017")
        return result


    def getPeriodData(self):
        """"""
        """ params
        val ttIds: List<Int>,
        """

        #TODO
        result = self._requests(method="getPeriodData2017")
        return result


    def getAppInfo(self):
        """"""
        #TODO

        result = self._requests(method="getAppInfo", auth=False)
        return result

    def getVersion(self):
        """"""
        #TODO

        result = self._requests(method="getVersion", auth=False)
        return result


    def getAppSharedSecret(self, username:str="", password:str="#anonymous#"):
        """
        Get APP Shared Secrets
        :param username: username, default ""
        :param password: password, default "#anonymous#"
        :return: appSharedSecrets data
        """

        params = {
            "username": username,
            "password": password
        }

        result = self._requests(method="getAppSharedSecret", params=params, auth=False)
        return result


    def getUserData(self, elementID: int= 0) -> dict:
        """"""
        """ params
		"""
        params = {
            "deviceOs": "AND",
            "deviceOsVersion": "Android13 API 33",
            "elementId": 0 # what should be here? # can be any number?
        }

        result = self._requests(method="getUserData2017", params=params)
        return result



    def getColors(self) -> dict:
        """
        get colors of school
        :return: dict {key : {foreColor, backColor}}
        """
        result = self._requests(method="getColors2017")
        result = result["appcolors"]

        colors = {}
        for entry in result:
            colors[entry["type"]] = {key:val for key, val in entry.items() if not key=="type"}

        return colors


    def getMessagesOfDay(self, date: datetime.date = datetime.date.today()):
        """"""
        # TODO
        """ params
        val date: UntisDate,
        """
        params = {
            "date": f"{date:%Y-%m-%d}"
        }

        result = self._requests(method="getMessagesOfDay2017", params=params)
        return result


    def getExams(self, startDate: Union[datetime.datetime, str], endDate: Union[datetime.datetime, str],
            Id: str, typ: str ):
        """
        Get Exams in timerange
        :param startDate: The start date can be acquired through class startDate
        :param endDate: The end date can be acquired tho class endDate
        :param Id: The ID of class | student ... TODO need research
        :param typ: type of ID possible: CLASS | STUDENT | ... TODO: need research
        :return:
        """
        # TODO: IDEA: could obtain Information from Class | Student Group/Class/Object
        # get exams for given school year or for time range?
        isinstance(startDate, datetime) and (startDate := f"{startDate:%Y-%m-%d}")
        isinstance(endDate, datetime) and (endDate := f"{endDate:%Y-%m-%d}")

        params = {
            "startDate": startDate,
            "endDate": endDate,
            "id": f"{Id}",
            "type": f"{typ}"  # only seen in usage of CLASS
        }

        result = self._requests(method="getExams2017", params=params)
        # TODO: Empty result
        return result


    def getHomeWork(self, startDate: Union[datetime.datetime, str], endDate: Union[datetime.datetime, str],
                         ID: str, Type: str):
        """"""

        # TODO: IDEA: could obtain Information from Class | Student Group/Class/Object
        # TODO: See getExams2017
        startDate, endDate = f"{startDate:%Y-%m-%d}", f"{endDate:%Y-%m-%d}"
        params = {
            "startDate": startDate,
            "endDate": endDate,
            "id": f"{ID}",
            "type": f"{Type}"
        }

        """ params
        val id: Int,
		val type: String,
		val startDate: UntisDate,
		val endDate: UntisDate,
		"""

        result = self._requests(method="getHomeWork2017", params=params)
        return result


    def getTimetable(self):
        """"""

        params = {
            "startDate",
            "endDate",
            "id",
            "masterDataTimestamp",
            "timetableTimestamp",
            "timetableTimestamps",
            "type"
        }
        """ params
        val id: Int,
		val type: String,
		val startDate: UntisDate,
		val endDate: UntisDate,
		val masterDataTimestamp: Long, // TODO: Try how the response behaves depending on changes to this value
		val timetableTimestamp: Long,
		val timetableTimestamps: List<Long>,
		"""

        result = self._requests(method="getTimetable2017", params=params)
        return result

    # some special api functions?
    def _get_request(self, path):
        """"""
        headers = {
            "anonymous-school-base64": base64.b64encode(bytes(self.loginName,"UTF8")),
            "user-agent": "android"
        }
        url = f"https://{self.server}{path}?school={self.loginName}"
        result = requests.get(url=url, headers=headers)
        return result.json()


    def todo_1(self):
        path = "/WebUntis/api/rest/view/v1/mobile/data"
        return self._get_request(path)

    def todo_2(self):
        path = "/WebUntis/api/rest/view/v1/trigger/startup"
        return self._get_request(path)

    def todo_3(self):
        path = "/WebUntis/api/rest/view/v2/home"
        return self._get_request(path)

