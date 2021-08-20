from . import jalali


def jalali_converter(time):
    timeToStr = "{},{},{}".format(time.year, time.month, time.day)
    output = jalali.Gregorian(timeToStr).persian_tuple()
    return output


def jalaliConvertToGregorian(time):
    output = jalali.Persian((time[0], time[1], time[2])).gregorian_tuple()
    return output
