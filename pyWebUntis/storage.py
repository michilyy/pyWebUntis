from typing import Union

import pendulum
import requests
from pyWebUntis import network




class Stunde:
    school: object
    api: network.API

    # time
    startDateTime: pendulum.datetime
    endDateTime: pendulum.datetime

    # ids
    id: int
    lessonId: int

    # info
    homeWorks: list # TODO: research
    exam: list # TODO: research

    # attributes
    text: dict
    can: str
    ist: str

    # data

    klasse:dict
    subject:dict
    teacher:list
    raum:list



    def __init__(self, school:object, api:network.API, period):
        """"""

        self.school = school
        self.api = api

        for key in period.keys() & {"startDateTime","endDateTime","id","lessonId","homeWorks","exam","text","can","ist"}:
            setattr(self, key, period[key])

        # resolve data
        for element in period["elements"]:

            match element:
                case {"type": "CLASS"}:
                    self.klasse = self.school.find_klasses_where(id=element["id"])
                    break

                case {"type": "TEACHER"}:
                    self.teacher = self.school.find_teachers_where(id=element["id"])
                    break

                case {"type": "SUBJECT"}:
                    self.subject = self.school.find_subjects_where(id=element["id"])
                    break

                case {"type": "ROOM"}:
                    self.room = self.school.find_rooms_where(id=element["id"])
                    break




class School:
    api:network.API

    # school data
    address:str = ""
    displayName:str = ""
    schoolID:str = ""

    masterData:dict = {}
    userData:dict = {}
    settings:dict = {}

    # some additional data

    def __init__(self: object, server: str, loginName: str, username: str = "#anonymous#", password: str = "",**kwargs):
        """
        Init function for School class. Stores only Api related information specific attributes and functions
        :param server: base server url
        :param loginName: identifier name from school
        :param username: username of used default "#anonymous#"
        :param password: password of user default ""
        :param kwargs: will get ignored
        """

        self.api = network.API(server=server, loginName=loginName, username=username, password=password)

        schoolData = self.api.get_school_data()

        self.address = schoolData["address"]
        self.displayName = schoolData["displayName"]
        self.schoolID = schoolData["schoolId"]

        result = self.api.getUserData()
        self.masterData = result["masterData"]
        self.userData = result["userData"]
        self.settings = result["settings"]


    # klassen funktionen
    def find_param_where(self, parameter:str, **kwargs) -> list[dict]:
        """
        finds any key in masterData dict
        :param parameter: key which will be used in masterData for searching
        :param kwargs: arguments which to check
        :return: list of dicts
        """

        returning = []
        for param in self.masterData[parameter]:

            keys = param.keys() & kwargs.keys()
            for key in keys:
                if not param[key] == kwargs[key]:
                    continue

                returning.append(param)

        return returning




    def find_subjects_where(self, **options) -> list[dict]:
        """
        finds subject which match options
        :param options: key=val
        :return: list with dict
        :raises: KeyError
        """

        return self.find_param_where("subjects", **options)


    def find_klasses_where(self, **kwargs)  -> list[dict]:
        """
        Find klasse by parameter given in kwargs
        if key not in klasse dict key gets ignored
        only returns klasse dict when all args matched
        :param kwargs: key=val
        :return: [] or [klasse, klasse]
        """

        return self.find_param_where("klassen", **kwargs)


    def find_teachers_where(self, **kwargs)  -> list[dict]:
        """"""

        return self.find_param_where("teachers", **kwargs)

    def find_rooms_where(self, **kwargs)  -> list[dict]:
        """"""

        return self.find_param_where("rooms", **kwargs)

    def find_departments_where(self, **kwargs)  -> list[dict]:
        """"""

        return self.find_param_where("deparment", **kwargs)



    def get_timetable_week(self, ID:Union[int,str], typ:str, date:pendulum) -> dict:
        """
        get timetable from week sorted in days
        :param ID: ID of class | Student | ...
        :param typ: Type CLASS | STUDENT | ...
        :param date: any day in week
        :return:
        """

        date = pendulum.instance(date)
        args = {'ID': 5505, 'typ': 'CLASS', 'endDate': '2024-3-10', 'startDate': '2024-03-04'}
        result = self.api.getTimetable(**args)
        timetable = result["timetable"]

        #check if timetable has any data
        if not timetable["periods"]:
            return {}

        # sort timetable date
        week = {}
        for i in range(1,8):
            week[f"{pendulum.date(1,1,i):%a}"] = []

        for period in timetable["periods"]:
            day = pendulum.parse(period['startDateTime'])
            day = f"{ day:%a}"

            week[day].append(Stunde(self, self.api, period))

        return week

    def get_current_school_year(self) -> dict:
        """"""

        today = pendulum.today()
        conver = lambda date: pendulum.parse(date)

        for year in self.masterData["schoolyears"]:
            start = conver( year["startDate"] )
            end = conver( year["endDate"] )
            interval = pendulum.Interval(start, end)

            if today in interval:
                return year




    def find_next_school_week(self, ID:str, typ:str, iter:bool=False) -> dict:
        """
        finds next school week and return raw dict with timetable data
        :param ID: id
        :param typ: type
        :param iter: default False, if shoud iter until last date of year
        :return: dict
        """

        year = self.get_current_school_year()
        endDate = pendulum.parse(year["endDate"])

        for start, end in self.api.date_iter(end= endDate):
            result = self.api.getTimetable(start, end, ID=ID, typ=typ)

            if result["timetable"]["periods"]:
                data = result["timetable"]

                for i, element in enumerate(data["periods"]):
                    data["periods"][i] = Stunde(self, self.api, element)

                if iter:
                    yield result
                else:
                    return result

        if not iter:
            return {}


    def find_last_week(self, klassID:str):
        """"""
        # TODO



def search_school(query: str):
    """
    Search school with the given string.
    :param query: String with search querry
    :return: list with school objects
    """
    baseurl = "https://schoolsearch.webuntis.com/schoolquery2"
    json = {
        "id": f"blackberry",
        "jsonrpc": "2.0",
        "method": "searchSchool",
        "params": [{
            "search": f"{query}"
        }]
    }

    data = requests.post(url=baseurl, json=json)
    data = data.json()
    schools = [School(**result) for result in data["result"]["schools"]]
    return schools
