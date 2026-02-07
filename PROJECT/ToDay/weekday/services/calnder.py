Year={
    '2001':'A','2002':'B','2003':'C','2004':'K',
    '2005':'F','2006':'G','2007':'A','2008':'I',
    '2009':'D','2010':'I','2011':'F','2012':'N',
    '2013':'B','2014':'C','2015':'D','2016':'L',
    '2017':'G','2018':'A','2019':'B','2020':'J','2021':'E',
    '2022':'F','2023':'G','2024':'H','2025':'C','2026':'D',
    '2027':'E','2028':'M','2029':'A','2030':'B','2031':'C',
    '2032':'K','2033':'F','2034':'G','2035':'A','2036':'I',
    '2037':'D','2038':'I','2039':'F','2040':'N','2041':'B',
    '2042':'C','2043':'D','2044':'L','2045':'G','2046':'A',
    '2047':'B','2048':'J','2049':'E','2050':'F','2051':'G',
    '2052':'H','2053':'C','2054':'D','2055':'E','2056':'M',
    '2057':'A','2058':'B','2059':'C','2060':'K','2061':'F',
    '2062':'G','2063':'A','2064':'I','2065':'D','2066':'E',
    '2067':'F','2068':'N','2069':'B','2070':'C','2071':'D',
    '2072':'L','2073':'G','2074':'A','2075':'B','2076':'J',
    '2077':'E','2078':'F','2079':'G','2080':'H','2081':'C',
    '2082':'D','2083':'E','2084':'M','2085':'A','2086':'B',
    '2087':'C','2088':'K','2089':'F','2090':'G','2091':'A',
    '2092':'I','2093':'D','2094':'I','2095':'F','2096':'N',
    '2097':'B','2098':'C','2099':'D','2100':'E',
    
}


def months(mon): #take input as 01...12 op=jan jun etc
    num=str(mon)
    month={
        '01':'JAN',
        '02':'FEB',
        '03':'MAR',
        '04':'APR',
        '05':'MAY',
        '06':'JUN',
        '07':'JUL',
        '08':'AUG',
        '09':'SEP',
        '10':'AUG',
        '11':'NOV',
        '12':'DEC',
        }
    #print(month[num])
    return month[num]
#add month + key genrater hare
def Month_key(num,kay): # input month + Key from year
    mon=months(num)
    DATA = {
    'A': {'JAN':1,'FEB':4,'MAR':4,'APR':7,'MAY':2,'JUN':5,'JUL':7,'AUG':3,'SEP':6,'OCT':1,'NOV':4,'DEC':6},
    'B': {'JAN':2,'FEB':5,'MAR':5,'APR':1,'MAY':3,'JUN':6,'JUL':1,'AUG':4,'SEP':7,'OCT':2,'NOV':5,'DEC':7},
    'C': {'JAN':3,'FEB':6,'MAR':6,'APR':2,'MAY':4,'JUN':7,'JUL':2,'AUG':5,'SEP':1,'OCT':3,'NOV':6,'DEC':1},
    'D': {'JAN':4,'FEB':7,'MAR':7,'APR':3,'MAY':5,'JUN':1,'JUL':3,'AUG':6,'SEP':2,'OCT':4,'NOV':7,'DEC':2},
    'E': {'JAN':5,'FEB':1,'MAR':1,'APR':4,'MAY':6,'JUN':2,'JUL':4,'AUG':7,'SEP':3,'OCT':5,'NOV':1,'DEC':3},
    'F': {'JAN':6,'FEB':2,'MAR':2,'APR':5,'MAY':7,'JUN':3,'JUL':5,'AUG':1,'SEP':4,'OCT':6,'NOV':2,'DEC':4},
    'G': {'JAN':7,'FEB':3,'MAR':3,'APR':6,'MAY':1,'JUN':4,'JUL':6,'AUG':2,'SEP':5,'OCT':7,'NOV':3,'DEC':5},
    'H': {'JAN':1,'FEB':4,'MAR':5,'APR':1,'MAY':3,'JUN':6,'JUL':1,'AUG':4,'SEP':7,'OCT':2,'NOV':5,'DEC':7},
    'I': {'JAN':2,'FEB':5,'MAR':6,'APR':2,'MAY':4,'JUN':7,'JUL':2,'AUG':5,'SEP':1,'OCT':3,'NOV':6,'DEC':1},
    'J': {'JAN':3,'FEB':6,'MAR':7,'APR':3,'MAY':5,'JUN':1,'JUL':3,'AUG':6,'SEP':2,'OCT':4,'NOV':7,'DEC':2},
    'K': {'JAN':4,'FEB':7,'MAR':1,'APR':4,'MAY':6,'JUN':2,'JUL':4,'AUG':7,'SEP':3,'OCT':5,'NOV':1,'DEC':3},
    'L': {'JAN':5,'FEB':1,'MAR':2,'APR':5,'MAY':7,'JUN':3,'JUL':5,'AUG':1,'SEP':4,'OCT':6,'NOV':2,'DEC':4},
    'M': {'JAN':6,'FEB':2,'MAR':3,'APR':6,'MAY':1,'JUN':4,'JUL':6,'AUG':2,'SEP':5,'OCT':7,'NOV':3,'DEC':5},
    'N': {'JAN':7,'FEB':3,'MAR':4,'APR':7,'MAY':2,'JUN':5,'JUL':7,'AUG':3,'SEP':6,'OCT':1,'NOV':4,'DEC':6},
    }
    # print(DATA[kay][mon])
    return(DATA[kay][mon])

#Month_key('01','A')
#input month num + key from year
def calend(date, key):
    index = (date + key - 1) % 7 + 1

    days = {
        2: 'MONDAY',
        3: 'TUESDAY',
        4: 'WEDNESDAY',
        5: 'THURSDAY',
        6: 'FRIDAY',
        7: 'SATURDAY',
        1: 'SUNDAY',
    }

    return days[index]




def fullday(yea,mon,daye): #yea,mon,daye 
    # print("enter year as full ex.2020")
    # yea=input()
    # print("enter month as ex.jan=01 (01 - only)" )
    # mon=input()
    # print("enter day date as ex.01,..31 etc")
    # daye=input()
    year=str(yea)
    dayd=int(daye)
    years_kay=Year[year]
    month_key=Month_key(mon,years_kay)
    #monss=months(mon)
    days=calend(dayd,month_key)
    print(f"Date={daye} {yea} WeekDay Is : {days}")
    return days



fullday('2026','02','07') #give input as sting not number 0 not inital work