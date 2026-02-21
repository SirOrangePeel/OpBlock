from datetime import datetime, date, time


def parse_schedule_recurring_soonest(sched):
    if sched[:1] == "D":
        sep = sched.split(";")
        dates = []
        for stringDate in sep[1:]:
            dates.append(datetime.strptime(stringDate, '%y%m%d:%H%M'))
        dates.sort()
    else:
        currentWeekDay = datetime.today().weekday()
        sep = sched.split(";")
        dates = []
        for stringDate in sep[1:]:
            day = stringDate[0]
            if int(day) == currentWeekDay:
                dates.append(datetime.combine(datetime.today().date(), datetime.strptime(stringDate[1:], '%H%M').time()))
        dates.sort()

    if len(dates) >= 1:
        soonest = dates[0]
    else:
        soonest = None
    return(soonest)


def parse_schedule_walker(sched):
    currentWeekDay = datetime.today().weekday()
    sep = sched.split(";")
    dates = []
    for stringDate in sep:
        day = stringDate[0]
        time1 = stringDate[1:5]
        time2 = stringDate[6:]
        if int(day) == currentWeekDay:
            dates.append((datetime.combine(datetime.today().date(), datetime.strptime(time1, '%H%M').time()), datetime.combine(datetime.today().date(), datetime.strptime(time2, '%H%M').time())))
    dates = sorted(dates, key=lambda x: x[0])

    if len(dates) >= 1:
        soonest = dates[0]
    else:
        soonest = None
    return(soonest)

def walker_available(sched):
    soonest = parse_schedule_walker(sched)
    currentDate = datetime.today()
    if currentDate >= soonest[0]:
        if currentDate < soonest[1]:
            return(True)
    return(False)