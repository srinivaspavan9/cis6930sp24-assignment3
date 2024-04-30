import pytest
from datetime import datetime

def get_day_of_week(date_time_str):
    date_time = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")
    # Adjust so 1 is Sunday and 7 is Saturday
    return (date_time.weekday() + 1) % 7 + 1

def test_get_day_of_week():
    # Test case: Known date where 04/03/2022 is a Sunday
    assert get_day_of_week("04/03/2022 00:00") == 1  # Now expecting 1 for Sunday
    # Test case: Another known date
    assert get_day_of_week("04/04/2022 00:00") == 2  # Now expecting 2 for Monday, if Sunday is 1

    print("All tests passed for get_day_of_week.")
