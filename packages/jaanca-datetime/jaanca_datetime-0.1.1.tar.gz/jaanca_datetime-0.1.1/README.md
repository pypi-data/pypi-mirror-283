<p align="center">
    <em>jaanca public libraries</em>
</p>

<p align="center">
<a href="https://pypi.org/project/jaanca-datetime" target="_blank">
    <img src="https://img.shields.io/pypi/v/jaanca-datetime?color=blue&label=PyPI%20Package" alt="Package version">
</a>
<a href="(https://www.python.org" target="_blank">
    <img src="https://img.shields.io/badge/Python-%5B%3E%3D3.8%2C%3C%3D3.11%5D-blue" alt="Python">
</a>
</p>


---

#  A tool library created by jaanca

* **Python library**: A tool library created by jaanca with help functions for date and time management and moving dates between time days by UTC.

[Source code](https://github.com/jaanca/python-libraries/tree/main/jaanca-datetime)
| [Package (PyPI)](https://pypi.org/project/jaanca-datetime/)
| [Samples](https://github.com/jaanca/python-libraries/tree/main/jaanca-datetime/samples)

---

# library installation
```console
pip install jaanca-datetime --upgrade
```

---
# Example of use

```python
from jaanca_datetime import DateTimeHelper, App,TimeZonesPytz

if __name__=="__main__":
    # DateTimeHelper.print_console_timezones_pytz()
    print(f"date now: {DateTimeHelper.get_datetime_now(App.Time.POSTGRESQL_FORMAT_DATE,is_format_string=False)}")
    print(f"date timezone convert UTC to Bogotá: {DateTimeHelper.get_datetime_now_to_another_location(App.Time.STANDARD_FORMAT_DATE,TimeZonesPytz.US.AZURE_DEFAULT,TimeZonesPytz.America.BOGOTA)}")

    datetime_data="2024-08-22 14:02:02"
    datetime_format=App.Time.STANDARD_FORMAT_DATE
    is_valid_format=DateTimeHelper.is_valid_datetime_format(datetime_data,datetime_format)
    print(f"datetime_data[{datetime_format}]:[{datetime_data}]: is_valid_format={is_valid_format}")

    datetime_data="2024-08-22"
    datetime_format="%Y-%m-%d"
    is_valid_format=DateTimeHelper.is_valid_datetime_format(datetime_data,datetime_format)
    print(f"datetime_data[{datetime_format}]:[{datetime_data}]: is_valid_format={is_valid_format}")

    datetime_data="2024-08-22"
    datetime_format=App.Time.STANDARD_FORMAT_DATE
    is_valid_format=DateTimeHelper.is_valid_datetime_format(datetime_data,datetime_format)
    print(f"datetime_data[{datetime_format}]:[{datetime_data}]: is_valid_format={is_valid_format}")

# output
# date now: 2024-07-09 12:31:29.366428
# date timezone convert UTC to Bogotá: 2024-07-09 07:31:29
# datetime_data[%Y-%m-%d %H:%M:%S]:[2024-08-22 14:02:02]: is_valid_format=True
# datetime_data[%Y-%m-%d]:[2024-08-22]: is_valid_format=True
# datetime_data[%Y-%m-%d %H:%M:%S]:[2024-08-22]: is_valid_format=False
 
```

---

# Semantic Versioning

jaanca-datetime < MAJOR >.< MINOR >.< PATCH >

* **MAJOR**: version when you make incompatible API changes
* **MINOR**: version when you add functionality in a backwards compatible manner
* **PATCH**: version when you make backwards compatible bug fixes

## Definitions for releasing versions
* https://peps.python.org/pep-0440/

    - X.YaN (Alpha release): Identify and fix early-stage bugs. Not suitable for production use.
    - X.YbN (Beta release): Stabilize and refine features. Address reported bugs. Prepare for official release.
    - X.YrcN (Release candidate): Final version before official release. Assumes all major features are complete and stable. Recommended for testing in non-critical environments.
    - X.Y (Final release/Stable/Production): Completed, stable version ready for use in production. Full release for public use.
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

## [0.0.1rcX] - 2024-05-24
### Added
- First tests using pypi.org in develop environment.

## [0.1.0] - 2024-05-24
### Added
- Completion of testing and launch into production.

## [0.1.1] - 2024-05-24
### Added
- Add feature is_valid_datetime_format.

