"""Common Python Library time related functions.

This module provides functions to manipulate time|date objects

"""

#----- Python imports ----
import datetime
import time

def checkLeapYear(year):
    """Check for leap years
    
    Parameters
    ----------
    year : str or int
        The year to be checked <YYYY>
    
    Returns
    -------
    bool
        True: year is leap year
        False: year is no leap year
    """
    year = int(year)
    if (year % 400) == 0:
        return True
    elif (year % 100) == 0:
        return False
    elif (year % 4) == 0:
            return True
    else:
        return False

def daysInFebruary(year):
    """Get the number of days in February based on the year
    
    Parameters
    ----------
    year : str or int
        The year to be checked  <YYYY>
    
    Returns
    -------
    int
        The number of days in February (28 or 29)
    """
    if checkLeapYear(year):
        return 29
    else:
        return 28

def convertDate(inDate, inFormat='%Y-%m-%d %H:%M:%S',outFormat='%Y%m%d'):
    """Convert date from inFormat to outFormat
    
    For more information on formatting, see `official documentation <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.
    
    Parameters
    ----------
    inDate : str or int
        Input date
    inFormat: str, optional
        String representation of inDate, defaults to '%Y-%m-%d %H:%M:%S'
    outFormat: str, optional
        String representation of returned date, defaults to '%Y%m%d'
    
    Returns
    -------
    str
        Formatted inDate
    """
    try:
        date=time.strptime(str(inDate),inFormat)
    except ValueError:
        #This is probably due to receiving 'seconds since the epoch'
        #split up in components & get [year,day,month]
        timeVal = time.gmtime(inDate)[0:3]
        #convert again
        date = time.strptime('{}{:02d}{:02d}'.format(timeVal[0],
                                                     timeVal[1],
                                                     timeVal[2]),
                             '%Y%m%d')
    return time.strftime(outFormat,date)

def convert2Julian(inDate):
    """Convert a date to Julian notation
    
    Parameters
    ----------
    inDate : str or int
        Input date <YYYYMMDD>
    
    Returns
    -------
    str
        Julian notation of inDate <YYYYddd>
    """
    inDate = str(inDate)
    yyyy = int(inDate[0:4])
    mm = int(inDate[4:6])
    totalDays = int(inDate[6:8])
    for n in range(1,mm):
        totalDays += getNrDays(n, yyyy)
    return '{}{:03d}'.format(yyyy, totalDays)

def dateNextPeriod (inDate, period, inFormat='%Y%m%d',outFormat='%Y%m%d'):
    """Get the start date of the next period
    
    Returns the first day of the next period (1/10/30/366 days)
    For more information on formatting, see `official documentation <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.
    
    Parameters
    ----------
    inDate : str or int
        Input date <YYYYYMMDD>
    period : str or int
        Period should be 1, 10, 30 or 365 for day, dekad, month or year
    inFormat: str, optional
        String representation of inDate, defaults to '%Y%m%d'
    outFormat: str, optional
        String representation of returned date, defaults to '%Y%m%d'
    Returns
    -------
    str
        The start date of the next period in the desired output format
    Raises
    ------
    ValueError
        If the period is not correct
    """
    inDate = str(inDate)
    period = int(period)
    # Parse input date
    date = time.strptime(inDate,inFormat)
    yyyy = str(date[0]).zfill(2)
    mm   = str(date[1]).zfill(2)
    dd   = str(date[2]).zfill(2)
    inDate = yyyy + mm + dd

    # Get next startdate in period
    if period == 1:
        outDate = incrDate(inDate,1)
    elif period == 10:
        if dd <= '10':
            outDate = yyyy + mm + '11'
        elif dd <= '20':
            outDate = yyyy + mm + '21'
        elif dd <= '31':
            date2   = incrDate(inDate, 12)
            outDate = date2[0:4] + date2[4:6] + '01'
    elif period == 30:
        if inDate[4:6] == '12':
            yyyy2   = int(inDate[0:4]) + 1
            outDate = str(yyyy2) + '01' + '01'
        else:
            mm2     = int(inDate[4:6]) + 1
            outDate = inDate[0:4] + str(mm2).zfill(2) + '01'
    elif period == 365:
        #365 or 366 when leap year; 337 + days in February
        date2   = int(inDate[0:4]) + 1
        outDate = str(date2) + '01' + '01'
    else:
        raise ValueError('Period is not defined')
    # Formatting output
    outDate = time.strptime(outDate,"%Y%m%d")
    return time.strftime(outFormat,outDate)


def today(outFormat='%Y%m%d'):
    """Get the system date in the desired format

    Parameters
    ----------
    outFormat: str, optional
        String representation of returned date, defaults to '%Y%m%d'

    Returns
    -------
    str
        date

    """
    timestampFormat = '%Y-%m-%d %H:%M:%S.%f'
    timestamp = datetime.datetime.now().strftime(timestampFormat)
    date = time.strptime(timestamp, timestampFormat)
    return time.strftime(outFormat, date)

def datePreviousPeriod (inDate, period, inFormat='%Y%m%d',outFormat='%Y%m%d'):
    """Get the start date of the previous period
    
    Returns the first day of the previous period (1/10/30/366 days)
    For more information on formatting, see `official documentation <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.
    
    Parameters
    ----------
    inDate : str or int
        Input date <YYYYYMMDD>
    period : str or int
        Period should be 1, 10, 30 or 365 for day, dekad, month or year
    inFormat: str, optional
        String representation of inDate, defaults to '%Y%m%d'
    outFormat: str, optional
        String representation of returned date, defaults to '%Y%m%d'
    Returns
    -------
    str
        The start date of the previous period in the desired output format
    Raises
    ------
    ValueError
        If the period is not correct
    """
    inDate = str(inDate)
    period = int(period)
    # Parse input date
    date = time.strptime(inDate,inFormat)
    yyyy = '{:d}'.format(date[0])
    mm   = '{:02d}'.format(date[1])
    dd   = '{:02d}'.format(date[2])
    inDate = yyyy + mm + dd

    # Get previous startdate in period
    if period == 1:
        outDate = incrDate(inDate,-1)
    elif period == 10:
        outDate = getPrevDekStart(inDate)
    elif period == 30:
        if inDate[4:6] == '01':
            yyyy2   = int(inDate[0:4]) - 1
            outDate = str(yyyy2) + '1201'
        else:
            mm2     = int(inDate[4:6]) - 1
            outDate = '{}{:02d}01'.format(inDate[0:4], mm2)
    elif period == 365:
        yyyy2   = int(inDate[0:4]) - 1
        outDate = '{}0101'.format(yyyy2)
    else:
        raise ValueError('Period is not defined')
    # Formatting output
    outDate = time.strptime(outDate,"%Y%m%d")
    return time.strftime(outFormat,outDate)

def getDekEnd(inDate):
    """Get the last day of the dekad
    
    Parameters
    ----------
    inDate : str or int
        Input date <YYYYMMDD>
    
    Returns
    -------
    str
        End date of the dekad <YYYYMMDD>
    """
    year = str(inDate)[0:4]
    month = str(inDate)[4:6]
    day = int(str(inDate)[6:8])
    if day < 11:
        dekEndDay = '10'
    elif day < 21:
        dekEndDay = '20'
    else: 
        dekEndDay = str(getNrDaysInMonth(month, year))
    return year + month + dekEndDay

def getNrDays(this_month,this_year):
    """ Duplicate of getNrDaysInMonth.
        Kept for backwards compatibility, but redericted to 
        other function"""
    return getNrDaysInMonth(this_month,this_year)


def getDekStart(inDate):
    """Get the first day of the dekad
    
    Parameters
    ----------
    inDate : str or int
        Input date <YYYYMMDD>
    
    Returns
    -------
    str
        First date of the dekad <YYYYMMDD>
    """
    year = str(inDate)[0:4]
    month = str(inDate)[4:6]
    day = int(str(inDate)[6:8])
    if day < 11:
        dekStartDay = '01'
    elif day < 21:
        dekStartDay = '11'
    else:
        dekStartDay = '21'
    return year + month + dekStartDay

def getPrevDekStart(inDate):
    """Get the first day of the previous dekad
    
    Parameters
    ----------
    inDate : str or int
        Input date <YYYYMMDD>
    
    Returns
    -------
    str
        First date of the dekad <YYYYMMDD>
    """
    dekStartDate = getDekStart(inDate)
    prevDekEnd = incrDate(dekStartDate,days=-1)
    return getDekStart(prevDekEnd)

def getNrDaysInMonth(month, year):
    """Get the number of days in the month
    
    Parameters
    ----------
    month : str or int
        The month
    year : str or int
        The year <YYYY>
    
    Returns
    -------
    int
        The number of days
    """
    year = int(year)
    month = int(month)
    nrDaysInMonth = [31, daysInFebruary(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return nrDaysInMonth[month-1]

def getNrDekads(startDate, endDate):
    """Get the number of dekads that cover the dates
    
    Calculate the number of dekads that is needed to cover the time span
    between the start date and the end date. The dekad(s) of the start date and
    the end data is included.
    
    Parameters
    ----------
    startDate : str or int
        Start date <YYYYMMDD>
    endDate : str or int
        End date <YYYYMMDD>
    
    Returns
    -------
    int
        The number of dekads
    """
    nrDeks = 0
    startDate = int(startDate)
    endDate = int(endDate)
    loopDate = startDate
    #loop the dates to count the dekads
    while (loopDate <= endDate):
        nrDeks += 1
        loopDate = int(incrDate(getDekEnd(loopDate),1))
    return nrDeks 

def dateToDekad(date, referenceYear = 1980):
    """Calculates the dekad number where a given date is in
    
    Calculate the number of dekads since the reference year.
    Counting starts with January 1 of the reference year being dekad 1
    
    Parameters
    ----------
    date : str or int
        Date <YYYYMMDD>
    referenceYear : str or int, optional
        Reference year <YYYY>, default 1980
    
    Returns
    -------
    int
        The number of dekads since 
    """
    referenceYear = int(referenceYear)
    startOfDekad = getDekStart(date)
    year = int(startOfDekad[0:4])
    month = int(startOfDekad[4:6])
    dekadInMonth = int(startOfDekad[6])+1 # first character of day ('0','1', or '2')

    dekadWithoutDay = (year - referenceYear) * 36 + (month - 1) * 3

    return dekadWithoutDay + dekadInMonth

def incrDate (inDate, days=0, hours=0, minutes=0, seconds=0, inFormat='%Y%m%d', outFormat='%Y%m%d'):
    """Increment a date with the given step(s)
    
    Calculate a date based on the input date and the given offset steps. An 
    offset can be positive or negative.
    For more information on formatting, see `official documentation <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.
    
    Parameters
    ----------
    inDate : str or int
        Input date <YYYYMMDD>
    days : str or int, optional
        Offset days, default 0
    hours : str or int, optional
        Offset hours, default 0
    minutes : str or int, optional
        Offset minutes, default 0
    seconds : str or int, optional
        Offset seconds, default 0
    inFormat: str, optional
        String representation of inDate, defaults to '%Y%m%d'
    outFormat: str, optional
        String representation of returned date, defaults to '%Y%m%d'
    
    Returns
    -------
    str
        The incremented date 
    """
    #convert input date to datetime object
    #-create timestamp from time tuple
    inTimeStamp = time.mktime(time.strptime(str(inDate),inFormat))
    #-convert timestamp to datetime object
    date = datetime.datetime.fromtimestamp(inTimeStamp)
    
    #convert addition to time-delta object
    inter = datetime.timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    
    #add to input date
    outDate = date + inter
    
    #return time in string format
    return outDate.strftime(outFormat)

def listPeriod(startDate, endDate, period=10, first_day_only=False):
    """Create a list of start- (and end-dates)
    
    Create a list of start- (and end-dates) ([first_day, last_day]) that
    intersect with the start and end date with a step size defined by the period
    
    Examples
    --------
    listPeriod(20180102, 20180123,10)
      -> [['20180101', '20180110'], ['20180111', '20180120'], ['20180121', '20180131']]
    listPeriod(20231206, 20231208,1, first_day_only=True)
      -> ['20231206','20231207','20231208']
    
    Parameters
    ----------
    startDate : str or int
        Start date <YYYYMMDD>
    endDate : str or int
        End date <YYYYMMDD>
    period : str or int, optional
        Period should be 1, 10, 30 or 365 for day, dekad, month or year, default is 10
    
    Returns
    -------
    list of list of str OR lst of str
        A list of [first_day, last_day] pairs OR
        A list of [first_day, first_day]
    """
    startP = datePreviousPeriod(startDate,period)
    # Ensure we loop at least once
    endP   = incrDate(endDate,-1) 
    dateLst=[]
    while str(endP) < str(endDate):
        startP=dateNextPeriod(startP,period)
        endP=incrDate(dateNextPeriod(startP,period),-1)
        if first_day_only:
            dateLst.append(startP)
        else:
            dateLst.append([startP,endP])

    return dateLst

def dateInPeriod(date, startDate, endDate):
    """Check if date is in period between the start and end date    
    
    Parameters
    ----------
    date : str or int
        date to check <YYYYMMDD>
    startDate : str or int
        Start date of the period <YYYYMMDD>
    endDate : str or int
        End date of the period <YYYYMMDD>
    Returns
    -------
    bool
        True if the data is in the period, False if not
    """
    if int(date) >= int(startDate):
        if int(endDate) >= int(date):
            return True
    return False

def today(outFormat='%Y%m%d'):
    """Get the system date in the desired format
    
    Parameters
    ----------
    outFormat: str, optional
        String representation of returned date, defaults to '%Y%m%d'
    
    Returns
    -------
    str
        date
    
    """
    timestampFormat = '%Y-%m-%d %H:%M:%S.%f'
    timestamp = datetime.datetime.now().strftime(timestampFormat)
    date=time.strptime(timestamp,timestampFormat)
    return time.strftime(outFormat,date)

def countNbDays(startDate, endDate, inFormat='%Y%m%d'):
    """Count the number of days between 2 dates
    
    Parameters
    ----------
    startDate : str or int
        Start date of the period
    endDate : str or int
        End date of the period
    inFormat: str, optional
        String representation of start and end date, defaults to '%Y%m%d'
    
    Returns
    -------    
    int
        nr of days
    
    Notes
    -----
    if start date is greater then end date, the number of days will be negative
    """
    # Convert startDate and endDate in date format
    start = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(startDate), inFormat)))
    end = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(endDate), inFormat)))
    # return difference in number of days
    return (end-start).days


def building_date_lst(startdate, enddate):
    from datetime import datetime, timedelta
    #startdate in format yyyymmdd or in number of days [int] to go back from enddate
    #enddate in format yyyymmdd or 'TODAY'
    if enddate.upper() == 'TODAY':
        enddate = datetime.today().strftime('%Y%m%d')
    else:
        try:
            enddate = datetime.strptime(enddate,'%Y%m%d').strftime('%Y%m%d')
        except:
            raise Exception("Enddate should be in format YYYYMMDD but is : %s" % enddate)

    if len(startdate)<5:
        number_of_days = int(startdate)
        startdate = (datetime.strptime(enddate,'%Y%m%d') - timedelta(days=number_of_days)).strftime('%Y%m%d')
    else:
        try:
            startdate = datetime.strptime(startdate,'%Y%m%d').strftime('%Y%m%d')
        except:
            raise Exception("Startdate should be in format YYYYMMDD but is : %s" % enddate)
    return startdate, enddate

if __name__ == '__main__':
    """Demo of CPL S3 datetime"""
    today = today()
    print('Today is', convertDate(today, '%Y%m%d', '%d/%m/%y'))
    print('or julian date', convert2Julian(today))
    print('This month has', getNrDays(today[4:6],today[0:4]),'days')
    
    startOfMonth = today[0:6] + '01'
    endOfMonth = today[0:6] + str(getNrDays(today[4:6],today[0:4]))
    
    print('The dekads of this month are', listPeriod(startOfMonth, endOfMonth))
    thisDekad = listPeriod(today, today)[0]
    print('The current dekad begins with {} and ends with {}'.format(thisDekad[0], thisDekad[1]))
    