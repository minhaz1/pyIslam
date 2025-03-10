"""
Qiblah Direction Calculator

This module provides functionality to calculate the direction of the Qiblah (the direction
to the Kaaba in Mecca) from any point on Earth using spherical trigonometry.

The Qiblah direction is calculated using the coordinates of Mecca (21.4225239, 39.8261816)
as a reference point. The result can be obtained in degrees from true north.

Example Usage:
    from pyIslam.qiblah import Qiblah
    
    # Calculate Qiblah direction for Paris, France
    qiblah = Qiblah(longitude=2.3522, latitude=48.8566)
    direction = qiblah.get_qiblah()  # Returns direction in degrees from true north
"""

from math import pi, atan, acos, asin
from pyIslam.baselib import dcos, dsin, normalize


class Qiblah:
    """
    Calculate Qiblah direction from any location on Earth.
    
    This class implements the spherical trigonometry calculations needed to determine
    the direction to the Kaaba in Mecca from any given point on Earth.
    
    Args:
        longitude (float): Geographical longitude of the location
        latitude (float): Geographical latitude of the location
        
    Note:
        - Longitude is positive for East and negative for West
        - Latitude is positive for North and negative for South
        - The returned angle is measured clockwise from true North
    """
    
    def __init__(self, conf):
        self._conf = conf
        MAKKAH_LATI = 21.42249   # latitude taken from maps.google.com
        MAKKAH_LONG = 39.826174  # longitude taken from maps.google.com
        lamda = MAKKAH_LONG - self._conf.longitude
        num = dcos(MAKKAH_LATI) * dsin(lamda)
        denom = (dsin(MAKKAH_LATI) * dcos(self._conf.latitude)
                 - dcos(MAKKAH_LATI) * dsin(self._conf.latitude)
                 * dcos(lamda))
        self._qiblah_dir = (180 / pi) * atan(num / denom)
        
        # Needs a check!
        if denom < 0:
            self._qiblah_dir = 180 + self._qiblah_dir
        if denom > 0 and num < 0:
            self._qiblah_dir = 360 + self._qiblah_dir

    def direction(self):
        '''Get the direction from the north of the qiblah (in degrees)'''
        return self._qiblah_dir

    def sixty(self):  # Convert the angle from degrees to sixty
        six = str(int(self._qiblah_dir)) + '°'
        self._qiblah_dir = (self._qiblah_dir - int(self._qiblah_dir)) * 60
        six = six + " " + str(int(self._qiblah_dir)) + "'"
        self._qiblah_dir = (self._qiblah_dir - int(self._qiblah_dir)) * 60
        six = six + " " + str(int(self._qiblah_dir)) + "''"
        self._qiblah_dir = (self._qiblah_dir - int(self._qiblah_dir)) * 60
        return six

