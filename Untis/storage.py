import dataclasses
import datetime#
from typing import Union
import requests
from Untis import network

class Klassen:
    classList:list

    def __init__(self:object, classList:list, school:object):
        """
        parse classList data and add additional information for easy usage
        :param classList: list from class School
        :param school: parent School instance
        """
        self.classList = classList
        self.school = School

    def find_klasse_by(self, **options) -> dict:
        """
        finds klasse by options given
        :param options: [id, name, longName, departmentId]
        :return: dict with selected klasse
        """

        for klasse in self.classList:
            for option, val in options.items():
                if not klasse[option] == val:
                    continue

            return klasse





class School:
    api:network.API

    # school data
    address:str = ""
    displayName:str = ""
    schoolID:str = ""

    masterData:dict = {}
    userData:dict = {}
    settings:dict = {}

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
    def find_klasse_by(self, **kwargs) -> list:
        """
        Find klasse by parameter given in kwargs
        if key not in klasse dict key gets ignored
        only returns klasse dict when all args matched
        :param kwargs: key=val
        :return: [] or [klasse, klasse]
        """

        returning = []

        for klasse in self.masterData["klassen"]:

            keys = klasse.keys() & kwargs.keys()
            for key in keys:
                if not klasse[key] == kwargs[key]:
                    continue

                returning.append(klasse)

        return returning






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
