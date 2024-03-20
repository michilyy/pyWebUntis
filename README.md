# Begin idk

This Projekt ist more or less just a bunch of code snippeds for working with the WebUntis api.
Most of this code is inspired by the betterUntis codebase


Two Instances
With find school you can find a school which you want.
Then you can give the selected school ID to the class and it finds itself all things
or asks for login if nessesary

## TODO:

- Add functions in school class
- parse output in usable format
-

# what do i want

# what i know

untis provides a domain for searching schools
get a list back where all schools with api endpoints are listed

- schools can require credentials but dont have to
- wenn login muss schlüssel generiert werden der in der anfrage immer mitgeschickt wird
- Schule has lehrer, schüler, räume, klassen, fächer, Tabele only with Zeiten,
- timetable is always asked in daterange from monday to sunday
- timetable send redundant data with ?

TODO UNTIS API:
 - [ Method Defined ] [ needed Args defined ] [ Working function ]
 - Constant
 - [X] [ ] [ ] const val DEFAULT_WEBUNTIS_HOST = "mobile.webuntis.com"
 - [ ] [ ] [ ] cst val DEFAULT_WEBUNTIS_PATH = "/ms/app/"
 - [X] [ ] [ ] cst val SCHOOL_SEARCH_URL = "https://schoolsearch.webuntis.com/schoolquery2"
 - Methods
 - [X] [ ] [ ] cst val METHOD_CREATE_IMMEDIATE_ABSENCE = "createImmediateAbsence2017"
 - [X] [ ] [ ] cst val METHOD_DELETE_ABSENCE = "deleteAbsence2017"
 - [X] [ ] [ ] cst val METHOD_GET_ABSENCES = "getStudentAbsences2017"
 - [X] [ ] [ ] cst val METHOD_GET_APP_SHARED_SECRET = "getAppSharedSecret"
 - [X] [ ] [ ] cst val METHOD_GET_EXAMS = "getExams2017"
 - [X] [ ] [ ] cst val METHOD_GET_HOMEWORKS = "getHomeWork2017"
 - [X] [ ] [ ] cst val METHOD_GET_MESSAGES = "getMessagesOfDay2017"
 - [X] [ ] [ ] cst val METHOD_GET_OFFICEHOURS = "getOfficeHours2017"
 - [X] [ ] [ ] cst val METHOD_GET_PERIOD_DATA = "getPeriodData2017"
 - [X] [ ] [ ] cst val METHOD_GET_TIMETABLE = "getTimetable2017"
 - [X] [ ] [ ] cst val METHOD_GET_USER_DATA = "getUserData2017"
 - [ ] [ ] [ ] cst val METHOD_SEARCH_SCHOOLS = "searchSchool"
 - [X] [ ] [ ] cst val METHOD_SUBMIT_ABSENCES_CHECKED = "submitAbsencesChecked2017"
 - [X] [ ] [ ] cst val METHOD_GET_LESSON_TOPIC = "getLessonTopic2017"
 - [X] [ ] [ ] cst val METHOD_SUBMIT_LESSON_TOPIC = "submitLessonTopic"
 - ACCESS
 - [ ] [ ] [ ] cst val CAN_READ_STUDENT_ABSENCE = "READ_STUD_ABSENCE"
 - [ ] [ ] [ ] cst val CAN_WRITE_STUDENT_ABSENCE = "WRITE_STUD_ABSENCE"
 - [ ] [ ] [ ] cst val CAN_READ_LESSON_TOPIC = "READ_LESSONTOPIC"
 - [ ] [ ] [ ] cst val CAN_WRITE_LESSON_TOPIC = "WRITE_LESSONTOPIC"
 - [ ] [ ] [ ] cst val CAN_READ_HOMEWORK = "READ_HOMEWORK"
 - [ ] [ ] [ ] cst val CAN_WRITE_HOMEWORK = "WRITE_HOMEWORK"
 - [ ] [ ] [ ] cst val CAN_READ_CLASSREG_EVENT = "READ_CLASSREGEVENT"
 - [ ] [ ] [ ] cst val CAN_WRITE_CLASSREG_EVENT = "WRITE_CLASSREGEVENT"
 - [ ] [ ] [ ] cst val CAN_DELETE_CLASSREG_EVENT = "DELETE_CLASSREGEVENT"
 - [ ] [ ] [ ] cst val CAN_READ_CLASS_ROLE = "READ_CLASSROLE"
 - [ ] [ ] [ ] cst val CAN_READ_PERIOD_INFO = "READ_PERIODINFO"
 - [ ] [ ] [ ] cst val CAN_WRITE_PERIOD_INFO = "WRITE_PERIODINFO"
 - [ ] [ ] [ ] cst val CAN_ACTION_CHANGE_ROOM = "ACTION_CHANGE_ROOM"
 - RIGHTS
 - [ ] [ ] [ ] cst val RIGHT_OFFICEHOURS = "R_OFFICEHOURS"
 - [ ] [ ] [ ] cst val RIGHT_ABSENCES = "R_MY_ABSENCES"
 - [ ] [ ] [ ] cst val RIGHT_CLASSREGISTER = "CLASSREGISTER"