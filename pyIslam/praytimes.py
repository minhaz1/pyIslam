# -*- coding: utf-8 -*-

from math import pi, atan, sqrt, tan, floor
from datetime import time, datetime
from pyIslam.hijri import HijriDate
from pyIslam.baselib import dcos, dsin, equation_of_time, gregorian_to_julian
from math import *


class FixedTime():
    """
    Represents fixed prayer time adjustments for both regular days and Ramadan.
    
    This class is used to store prayer time adjustments that are applied
    throughout the year and special adjustments for Ramadan.
    
    Args:
        all_year_time_min (float): Time adjustment in minutes for regular days
        ramadan_time_min (float): Time adjustment in minutes for Ramadan days
    """

    def __init__(self, all_year_time_min, ramadan_time_min):
        self._all_year_time = all_year_time_min
        self._ramadan_time = ramadan_time_min

    @property
    def ramadan_time_hr(self):
        return self._ramadan_time / 60.0

    @property
    def all_year_time_hr(self):
        return self._all_year_time / 60.0


class MethodInfo:
    """
    Defines a prayer time calculation method used by various Islamic organizations.
    
    This class stores the parameters used for calculating prayer times according to
    different recognized Islamic authorities and their geographical applicability.
    
    Args:
        method_id (int): Unique identifier for the calculation method
        organizations (str or list): Organization(s) using this method
        fajr_angle (float): Angle for Fajr prayer calculation
        ishaa_angle (float): Angle for Isha prayer calculation
        applicability (tuple): Regions/countries where this method is applicable
    """

    def __init__(self, method_id, organizations, fajr_angle, ishaa_angle, applicability=()):
        self._id = method_id
        self._organizations = organizations if type(
            organizations) in (list, tuple) else (organizations,)
        self._fajr_angle = fajr_angle
        self._ishaa_angle = ishaa_angle
        self._applicability = applicability if type(
            applicability) in (list, tuple) else (applicability,)

    @property
    def id(self):
        return self._id

    @property
    def organizations(self):
        return self._organizations

    @property
    def fajr_angle(self):
        return self._fajr_angle

    @property
    def ishaa_angle(self):
        return self._ishaa_angle

    @property
    def applicability(self):
        return self._applicability


LIST_FAJR_ISHA_METHODS = (
    MethodInfo(1, ("University of Islamic Sciences, Karachi (UISK)",
                   "Ministry of Religious Affaires, Tunisia",
                   "Grande Mosquée de Paris, France"),
               18.0, 18.0, ()),

    MethodInfo(2, ("Muslim World League (MWL)",
                   "Ministry of Religious Affaires and Awqaf, Algeria",
                   "Presidency of Religious Affairs, Turkey"),
               18.0, 17.0, ()),

    MethodInfo(3, "Egyptian General Authority of Survey (EGAS)",
               19.5, 17.5, ()),

    MethodInfo(4, "Umm al-Qura University, Makkah (UMU)",
               18.5, FixedTime(90, 120), ()),

    MethodInfo(5, ("Islamic Society of North America (ISNA)",
                   "France - Angle 15°"),
               15.0, 15.0, ()),

    MethodInfo(6, "French Muslims (ex-UOIF)",
               12.0, 12.0, ()),

    MethodInfo(7, ("Islamic Religious Council of Signapore (MUIS)",
                   "Department of Islamic Advancements of Malaysia (JAKIM)",
                   "Ministry of Religious Affairs of Indonesia (KEMENAG)"),
               20.0, 18.0, ()),

    MethodInfo(8, "Spiritual Administration of Muslims of Russia",
               16.0, 15.0, ()),

    MethodInfo(9, "Fixed Ishaa Time Interval, 90min",
               19.5, FixedTime(90, 90), ()),

)


class PrayerConf:
    """
    Configuration for prayer time calculations.
    
    This class holds the geographical and methodological parameters needed
    to calculate prayer times for a specific location.
    
    Args:
        longitude (float): Geographical longitude of the location
        latitude (float): Geographical latitude of the location
        timezone (int): Timezone offset from UTC
        angle_ref (int, optional): Reference method for Fajr/Isha angles. Defaults to 2
        asr_madhab (int, optional): Asr shadow calculation method (1=Shafi'i, 2=Hanafi). Defaults to 1
        enable_summer_time (bool, optional): Whether to adjust for daylight saving. Defaults to False
    """

    def __init__(self, longitude, latitude, timezone, angle_ref=2,
                 asr_madhab=1, enable_summer_time=False):
        '''Initialize the PrayerConf object
        @param longitude: geographical longitude of the given location
        @param latitude: geographical latitude of the given location
        @param timezone: the time zone GMT(+/-timezone)
        @param angle_ref: The reference method for Fajr and Ishaa angles, you can pass a MethodInfo object or the ID of the method (for backward compatibility), a list of predefined MethodInfos can be found in LIST_FAJR_ISHA_METHODS, default option for angle_ref is 2
        @param asr_madhab: integer value
        1 = Jomhor (Shafii, Maliki & Hambali) (default option)
        2 = Hanafi
        @param: enable_summer_time: True if summer time is used in the place,
        False (default) if not'''

        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone
        self.sherook_angle = 90.83333  # Constants
        self.maghreb_angle = 90.83333

        # 1 = Jomhor (Shafii, Maliki & Hambali), 2 = Hanafi
        self.asr_madhab = asr_madhab if asr_madhab == 2 else 1

        self.middle_longitude = self.timezone * 15
        self.longitude_difference = (
            self.middle_longitude - self.longitude) / 15

        self.summer_time = enable_summer_time

        global LIST_FAJR_ISHA_METHODS

        if isinstance(angle_ref, int):
            method = LIST_FAJR_ISHA_METHODS[angle_ref -
                                            1 if angle_ref <= len(LIST_FAJR_ISHA_METHODS) else 2]
        elif isinstance(angle_ref, MethodInfo):
            method = angle_ref
        else:
            raise TypeError(
                "angle_ref must be an instance form type int or MethodInfo")

        self.fajr_angle = (method.fajr_angle +
                           90.0) if type(method.fajr_angle) is not FixedTime else method.fajr_angle
        self.ishaa_angle = (method.ishaa_angle +
                            90.0) if type(method.ishaa_angle) is not FixedTime else method.ishaa_angle


class Prayer:
    """
    Main class for calculating Islamic prayer times.
    
    This class performs the actual calculations of prayer times based on
    the provided configuration and date.
    
    Args:
        conf (PrayerConf): Configuration object with location and calculation parameters
        dat (date): Date for which to calculate prayer times
        correction_val (float, optional): Optional correction value in minutes. Defaults to 0
    
    Methods:
        fajr_time(): Get Fajr prayer time
        sherook_time(): Get sunrise time
        dohr_time(): Get Dhuhr prayer time
        asr_time(): Get Asr prayer time
        maghreb_time(): Get Maghrib prayer time
        ishaa_time(): Get Isha prayer time
        midnight(): Get Islamic midnight time
        last_third_of_night(): Get the beginning of the last third of night
    """

    def __init__(self, conf, dat, correction_val=0):
        self._conf = conf
        self._date = dat
        self._jd = gregorian_to_julian(dat)

        if not (correction_val in range(-2, 3)):
            raise Exception('Correction value exception')
        else:
            self._correction_val = correction_val

        # Dohr time MUST BE calculated at first, every other time depends on it!
        self._dohr_time = self._get_dohr_time()

        self._fajr_time = self._get_fajr_time()
        self._sherook_time = self._get_sherook_time()
        self._asr_time = self._get_asr_time()
        self._maghreb_time = self._get_maghreb_time()
        self._ishaa_time = self._get_ishaa_time()

        # These HAVE TO BE called AFTER Ishaa, since they depends on it
        self._midnight = self._get_midnight()
        self._second_third_of_night = self._get_second_third_of_night()
        self._last_third_of_night = self._get_last_third_of_night()

    def _get_asr_angle(self):
        '''Get the angle angle for asr (according to choosed asr fiqh)'''
        delta = self._sun_declination()
        x = (dsin(self._conf.latitude) * dsin(delta)
             + dcos(self._conf.latitude) * dcos(delta))
        a = atan(x / sqrt(-x * x + 1))
        x = self._conf.asr_madhab + (1 / tan(a))
        return 90 - (180 / pi) * (atan(x) + 2 * atan(1))

    def _sun_declination(self):
        '''Get sun declination'''
        n = self._jd - 2451544.5
        epsilon = 23.44 - 0.0000004 * n
        l = 280.466 + 0.9856474 * n
        g = 357.528 + 0.9856003 * n
        lamda = l + 1.915 * dsin(g) + 0.02 * dsin(2 * g)
        x = dsin(epsilon) * dsin(lamda)
        return (180 / (4 * atan(1))) * atan(x / sqrt(-x * x + 1))

    def _get_time_for_angle(self, angle):
        '''Get Times for "Fajr, Sherook, Asr, Maghreb, ishaa"'''
        delta = self._sun_declination()
        s = ((dcos(angle)
              - dsin(self._conf.latitude) * dsin(delta))
             / (dcos(self._conf.latitude) * dcos(delta)))
        return (180 / pi * (atan(-s / sqrt(-s * s + 1)) + pi / 2)) / 15

    def _hours_to_time(self, val, shift):
        '''
        Convert a decimal value (in hours) to time object,
        @param val: hours value
        @param shift: time shift (in seconds) from the actual `val` time, used to add or subtract time from the prayer time
        @param summer_time: True id summer time is used, False else
        '''
        if not (isinstance(shift, float) or isinstance(shift, int)):
            raise ValueError("shift's value must be an int or a float")

        st = 1 if self._conf.summer_time else 0

        hours = val + shift / 3600
        minutes = (hours - floor(hours)) * 60
        seconds = (minutes - floor(minutes)) * 60

        hours = floor(hours + st) % 24

        return time(hours, floor(minutes), floor(seconds))

    def fajr_time(self, shift=0.0):
        '''
        Get the Fajr time
        @param shift: time shift (in seconds) from the actual `val` time, used to add or subtract time from the prayer time
        '''
        return self._hours_to_time(self._fajr_time, shift)

    def _get_fajr_time(self):
        return self._dohr_time - self._get_time_for_angle(self._conf.fajr_angle)

    def sherook_time(self, shift=0.0):
        '''
        Get the Sunrise (Sherook) time
        @param shift: time shift (in seconds) from the actual `val` time, used to add or subtract time from the prayer time
        '''
        return self._hours_to_time(self._sherook_time, shift)

    def _get_sherook_time(self):
        return self._dohr_time - self._get_time_for_angle(self._conf.sherook_angle)

    def dohr_time(self, shift=0.0):
        '''
        Get the Dohr (Zenith) time
        @param shift: time shift (in seconds) from the actual `val` time, used to add or subtract time from the prayer time
        '''
        return self._hours_to_time(self._dohr_time, shift)

    def _get_dohr_time(self):
        '''
        # Dohr time for internal use, return number of hours, not time object
        '''
        ld = self._conf.longitude_difference
        time_eq = equation_of_time(self._jd)
        duhr_t = 12 + ld + time_eq / 60
        return duhr_t

    def asr_time(self, shift=0.0):
        '''
        Get the Asr time
        @param shift: time shift (in seconds) from the actual `val` time, used to add or subtract time from the prayer time
        '''
        return self._hours_to_time(self._asr_time, shift)

    def _get_asr_time(self):
        return self._dohr_time + self._get_time_for_angle(self._get_asr_angle())

    def maghreb_time(self, shift=0.0):
        '''
        Get the Maghreb time
        @param shift: time shift (in seconds) from the actual `val` time, used to add or subtract time from the prayer time
        '''
        return self._hours_to_time(self._maghreb_time, shift)

    def _get_maghreb_time(self):
        return self._dohr_time + self._get_time_for_angle(self._conf.maghreb_angle)

    def ishaa_time(self, shift=0.0):
        '''
        Get the Ishaa time
        @param shift: time shift (in seconds) from the actual `val` time, used to add or subtract time from the prayer time
        '''
        return self._hours_to_time(self._ishaa_time, shift)

    def _get_ishaa_time(self):
        if (type(self._conf.ishaa_angle) is FixedTime):
            is_ramadan = HijriDate.get_hijri(
                self._date, self._correction_val).month == 9

            time_after_maghreb = self._conf.ishaa_angle.ramadan_time_hr if is_ramadan else self._conf.ishaa_angle.all_year_time_hr

            ishaa_t = (time_after_maghreb + self._dohr_time +
                       self._get_time_for_angle(self._conf.maghreb_angle))
        else:
            ishaa_t = self._dohr_time + \
                self._get_time_for_angle(self._conf.ishaa_angle)
        return ishaa_t

    def midnight(self, shift=0.0):
        '''
        Midnight is the exact time between sunrise (Shorook) and sunset (Maghreb),
        It defines usually the end of Ishaa time
        '''
        return self._hours_to_time(self._midnight, shift)

    def _get_midnight(self):
        return self._maghreb_time + ((24.0 - (self._maghreb_time - self._fajr_time)) / 2.0)

    def second_third_of_night(self, shift=0.0):
        return self._hours_to_time(self._second_third_of_night, shift)

    def _get_second_third_of_night(self):
        return self._maghreb_time + ((24.0 - (self._maghreb_time - self._fajr_time)) / 3.0)

    def last_third_of_night(self, shift=0.0):
        '''
        Qiyam time starts after Ishaa directly, however, the best time for Qiyam is the last third of night
        '''
        return self._hours_to_time(self._last_third_of_night, shift)

    def _get_last_third_of_night(self):
        # The last third of night,
        return self._maghreb_time + (2 * (24.0 - (self._maghreb_time - self._fajr_time)) / 3.0)
