from datetime import datetime, timedelta, tzinfo, timezone,  date
import time

"""
%d: Returns day of the month, from 1 to 31. In our example, it returned "15".
%m: Returns the month as a number, from 01 to 12.
%y: Returns the year in two-digit format, that is, without the century. For example, "18" instead of "2018".
%Y: Returns the year in four-digit format. In our example, it returned "2018".
%H: Returns the hour. In our example, it returned "00".
%M: Returns the minute, from 00 to 59. In our example, it returned "00".
%S: Returns the second, from 00 to 59. In our example, it returned "00".
%f: Returns microsecond from 000000 to 999999.
%Z: Returns the timezone.
%b: Returns the first three characters of the month name. In our example, it returned "Sep"
%j: Returns the number of the day in the year, from 001 to 366.
%W: Returns the week number of the year, from 00 to 53, with Monday being counted as the first day of the week.
%U: Returns the week number of the year, from 00 to 53, with Sunday counted as the first day of each week.
%a: Returns the first three characters of the weekday, e.g. Wed.
%A: Returns the full name of the weekday, e.g. Wednesday.
%B: Returns the full name of the month, e.g. September.
%w: Returns the weekday as a number, from 0 to 6, with Sunday being 0.
%p: Returns AM/PM for time.
%z: Returns UTC offset.
%c: Returns the local date and time version.
%x: Returns the local version of date.
%X: Returns the local version of time
"""
DATEFORMAT  = '%d-%m-%Y'
TIMEFORMAT = '%H:%M:%S'
DATETIMEFORMAT  = '{} {}'.format(DATEFORMAT,TIMEFORMAT)
DB_DATEFORMAT  = 'DD-MM-YYYY'
DB_TIMEFORMAT = 'HH24:MI:SS'
DB_DATETIMEFORMAT  = '{} {}'.format(DB_DATEFORMAT,DB_TIMEFORMAT)
def compileformat(p_format='DD-MM-YYYY HH24:MI:SS'):
    return p_format.replace('DD', '%d').replace(
        'MM', '%m').replace(
        'YYYY', '%Y').replace(
        'YY', '%y').replace(
        'HH24', '%H').replace(
        'HH', '%H').replace(
        'MI', '%M').replace(
        'SS', '%S')

class DateUtil():
    __formats = {'DD-MM-YY':"%d-%m-%y",
               'DD-MM-YYYY':"%d-%m-%Y",
               'YYYY-MM-DD':"%Y-%m-%d",
               'HH24:MI:SS':"%H:%M:%S",
               'DD-MM-YY HH24:MI:SS':"%d-%m-%y %H:%M:%S",
               'DD-MM-YYYY HH24:MI:SS':"%d-%m-%Y %H:%M:%S",
               'YYYY-MM-DD HH24:MI:SS':"%Y-%m-%d %H:%M:%S",
               }
    format = __formats['DD-MM-YYYY']
    dateformat = format
    datetimeformat = 'DD-MM-YYYY HH24:MI:SS'
    timeformat = 'HH24:MI:SS'
    dateobject = datetime.now()
    origdateformat = format
    origtimeformat =  'HH24:MI:SS'
    origdatetimeformat = 'DD-MM-YYYY HH24:MI:SS'
    unit_min = 60
    unit_hour = unit_min*60
    unit_day = unit_hour*24
    def __init__(self,p_dateformat='DD-MM-YYYY',
                 p_timeformat='HH24:MI:SS',
                 p_datetimeformat='DD-MM-YYYY HH24:MI:SS'):
        self.dateformat = self.get_format(p_dateformat)
        self.timeformat = self.get_format(p_timeformat)
        self.datetimeformat = self.get_format(p_datetimeformat)
        self.origdateformat = p_dateformat
        self.origtimeformat = p_timeformat
        self.origdatetimeformat = p_datetimeformat

    def get_format(self, p_key:str):
        try:
            if p_key in self.__formats.keys():
                self.format = self.__formats[p_key]
            return self.format
        except Exception as ex:
            print(ex)
            self.format = p_key
            return self.format

    def check_rettype(self,p_dateobject = datetime.now(),
                      p_format = format,
                      p_rettype = 'default',
                      p_origformat= origdateformat):
        try:
            if p_rettype == 'str':
                return p_dateobject.strftime(p_format)
            elif p_rettype == 'oracle':
                return "TO_DATE('{}','{}')".format(p_dateobject.strftime(p_format),p_origformat)
            return p_dateobject
        except Exception as ex:
            print(ex)
            raise ValueError('invalid date time format')

    def get_currentdate(self,p_rettype='default'):
        self.dateobject = datetime.now().date()
        return self.check_rettype(p_dateobject=self.dateobject,
                                  p_format=self.dateformat,
                                  p_rettype = p_rettype,
                                p_origformat = self.origdateformat)

    def get_currenttime(self,p_rettype='default'):
        self.dateobject = datetime.now().time()
        return self.check_rettype(p_dateobject=self.dateobject,
                                  p_format=self.timeformat,
                                  p_rettype = p_rettype,
                                p_origformat = self.origtimeformat)

    def get_currentdatetime(self,p_rettype='default'):
        self.dateobject = datetime.now()
        return self.check_rettype(p_dateobject=self.dateobject,
                                  p_format=self.datetimeformat,
                                  p_rettype = p_rettype,
                                p_origformat = self.origdatetimeformat)

    def get_timestamp(self, p_dateobject = datetime.now()):
        timestamp = p_dateobject.timestamp()
        return timestamp

    def age(self, p_dateobject, p_unit:int = 1):
        seconds = time.time() - self.get_timestamp(p_dateobject)
        result = round(seconds/p_unit, 3)
        return result

    def age_inminute(self,  p_dateobject = datetime.now()):
        return self.age(p_dateobject=p_dateobject, p_unit=self.unit_min )

    def age_inhour(self,  p_dateobject = datetime.now()):
        return self.age( p_dateobject=p_dateobject, p_unit=self.unit_hour)

    def age_inday(self,  p_dateobject = datetime.now()):
        return self.age(p_dateobject=p_dateobject, p_unit=self.unit_day)

    def plusminus(self,p_dateobject = datetime.now(), p_days =0,p_minutes=0,p_hours=0,p_seconds=0):
        return p_dateobject + timedelta(days=p_days, hours=p_hours, minutes=p_minutes,seconds=p_seconds)

    def stringtodate(self,p_datestring:str, p_format:str = 'DD-MM-YYYY',p_rettype='default'):
        self.format = self.get_format(p_format)
        self.dateobject = datetime.strptime(p_datestring, self.format)
        return self.check_rettype(p_dateobject=self.dateobject,
                                  p_format=self.format,
                                  p_rettype = p_rettype,
                                p_origformat = p_format.replace('%',''))

    def compileformat(self,p_format='DD-MM-YYYY HH24:MI:SS'):
        return p_format.replace('DD','%d').replace(
            'MM','%m').replace(
            'YYYY','%Y').replace(
            'YY','%y').replace(
            'HH24','%H').replace(
            'HH','%H').replace(
            'MI','%M').replace(
            'SS','%S')

    def get_date(self,yy, mm , dd):
        self.dateobject = datetime(yy,mm,dd)
        return self.dateobject

    def get_datetime(self,yy, mm , dd , hh=0, mi=0,ss=0,sss=0):
        self.dateobject = datetime(yy,mm,dd,hh,mi,ss)
        return self.dateobject

def get_oracledate(p_format:str = None):
    return DateUtil().get_currentdate(p_rettype='oracle')


def get_oracledatetime(p_format:str = None):
    return DateUtil().get_currentdatetime(p_rettype='oracle')


def dateto_oracle(p_date = datetime.now()):
    return DateUtil().check_rettype(p_dateobject=p_date,
                                    p_format=DATEFORMAT,
                                    p_origformat=DB_DATEFORMAT,
                                    p_rettype='oracle')


def datetimeto_oracle(p_date = datetime.now()):
    return DateUtil().check_rettype(p_dateobject=p_date,
                                    p_format = DATETIMEFORMAT,
                                    p_origformat=DB_DATETIMEFORMAT,
                                    p_rettype='oracle')
def sysdate(p_date = datetime.now()):
    return DateUtil().get_currentdatetime()