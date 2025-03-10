# pyIslam

[![Build Status](https://github.com/abougouffa/pyIslam/workflows/ci/badge.svg)](https://github.com/abougouffa/pyIslam/actions/workflows/ci.yml)

**_pyIslam_** is a Python Islamic library that provides various Islamic calculations including prayer times, qibla direction, Hijri calendar conversion, zakat calculation, and Islamic inheritance (mirath) calculation.

## Features

- [x] Prayer times calculation
- [x] Hijri/Gregorian date conversion
- [x] Qibla direction
- [x] Zakat calculation
- [x] Mirath (Islamic inheritance) calculation

## Installation

### From PyPi
```bash
pip install islam
```

**Note:** The package name on PyPi is `islam`, not `pyIslam` (which is taken by another project).

## Usage Examples

### Prayer Times
```python
from datetime import date
from pyIslam.praytimes import PrayerConf, Prayer

# Configure for your location (example: Paris, France)
conf = PrayerConf(
    longitude=2.3522,  # Paris longitude
    latitude=48.8566,  # Paris latitude
    timezone=1,        # UTC+1
    angle_ref=2,       # Calculation method
    asr_madhab=1       # 1 for Shafi'i, 2 for Hanafi
)

# Get prayer times for today
pt = Prayer(conf, date.today())
print(f"Fajr: {pt.fajr_time()}")
print(f"Sunrise: {pt.sherook_time()}")
print(f"Dhuhr: {pt.dohr_time()}")
print(f"Asr: {pt.asr_time()}")
print(f"Maghrib: {pt.maghreb_time()}")
print(f"Isha: {pt.ishaa_time()}")
```

### Qibla Direction
```python
from pyIslam.qiblah import Qiblah

# Calculate Qibla direction (example: Paris)
qibla = Qiblah(longitude=2.3522, latitude=48.8566)
direction = qibla.get_qiblah()
print(f"Qibla direction from true north: {direction:.1f}°")
```

### Hijri Date Conversion
```python
from datetime import date
from pyIslam.hijri import HijriDate

# Convert Gregorian to Hijri
today = date.today()
hijri = HijriDate.from_gregorian(today)
print(f"Today in Hijri: {hijri.day}/{hijri.month}/{hijri.year}")

# Convert Hijri to Gregorian
hijri_date = HijriDate(1444, 9, 1)  # 1 Ramadan 1444
greg = hijri_date.to_gregorian()
print(f"Gregorian date: {greg}")
```

### Zakat Calculation
```python
from pyIslam.zakat import Zakat

# Calculate Zakat on monetary wealth
wealth = Zakat(100000)  # Amount in your chosen currency
zakat_amount = wealth.calculate()
print(f"Zakat due: {zakat_amount}")
```

## Authors and Contributors

### Author
- Abdelhak Bougouffa [@abougouffa](https://github.com/abougouffa)

### Contributors
- Monsef Alahem [@monsef-alahem](https://github.com/monsef-alahem)
- Azzam S. A. [@azzamsa](https://github.com/azzamsa)

## Ports

### Rust
- **pyIslam** has been ported to Rust by Azzam S. A. [@azzamsa](https://github.com/azzamsa). The Rust version is available at [github.com/azzamsa/islam](https://github.com/azzamsa/islam) and features Prayer Times and Hijri calendar calculations.

---

**_pyIslam_** (Arabic Description)

هي مكتبة إسلامية للغة البرمجة بايثون، توفر امكانية حساب **أوقات الصلاة**، **اتجاه القبلة**، **التقويم الهجري**، **الزكاة** و**المواريث**.

حاليا، المكتبة تستطيع أن تقوم بـ:

- [x] حساب مواقيت الصلاة
- [x] التحويل بين التاريخ الهجري والميلادي
- [x] تحديد اتجاه القبلة
- [x] حساب الزكاة
- [x] حساب الميراث
