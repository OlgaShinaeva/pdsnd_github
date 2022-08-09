import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_city():
    cities = ["chicago", "new york city", "washington"]
    while True:
        city = input("Which city would you like to see a data for?\n").lower()
        if city in cities:
            break
        else:
            print("Sorry, I don't understand. Please try again")
    return city


def get_month():
    months = ["january", "february", "march", "april", "may", "june"]
    while True:
        month = input("Which month? January, February,"
                      "March, April, May or June?\n").lower()
        if month in months:
            break
        else:
            print("Sorry, I don't understand. Please try again")
    return month


def get_day():
    while True:
        try:
            day = int(input("Which day? Please type "
                            "your response as an integer "
                            "(e.g, 0 = Monday)\n"))
            if day >= 0 and day <= 6:
                print(f"You entered: {day}")
                break
            else:
                print("Sorry, I don't understand. Please try again")
        except ValueError:
            print("Invalid input")
    return day


def get_filters():
    """
    Asks user to specify a month and day to analyze.

    Returns:
        (str) month - name of the month to filter by,
        or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
        or "all" to apply no day filter
    """
    while True:
        response = input("Would you like to filter the data by month, "
                         "day, both or not at all?\n"
                         "Type 'none' for no time filter\nType 'raw' if"
                         " you want to see the raw data\n").lower()
        if "none" in response:
            month = None
            day = None
            break
        elif "both" in response:
            month = get_month()
            day = get_day()
            break
        elif "month" in response:
            month = get_month()
            day = None
            break
        elif "day" in response:
            day = get_day()
            month = None
            break
        elif "raw" in response:
            return None
        else:
            print("Sorry, I don't understand. Please try again")
    print('-'*40)
    return month, day


def raw_data(city):
    df = pd.read_csv(CITY_DATA[city])
    n = 0
    while n < (df.shape[0] - 4):
        print(df.iloc[n:n+5])
        response = input("Would you like to see another"
                         " 5 rows of data?\n").lower()
        if "no" in response:
            break
        elif "yes" in response:
            n += 5
        else:
            print("Sorry, I don't understand. Please try again")


def load_data(city, month, day):
    """
    Loads data for the specified city and
    filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
        or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
        or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing
        city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month
    if month is not None:
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # filter by day
    if day is not None:
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    day_of_week = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    months = ["january", "february", "march", "april", "may", "june"]
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month is None and day is None:
        most_common_month = months[df['month'].mode()[0] - 1]

        print(f"The most common month of travel: {most_common_month}")

        most_common_day_of_week = day_of_week[df['day_of_week'].mode()[0]]
        print(f"The most common day of week: {most_common_day_of_week}")

        df['hour'] = df['Start Time'].dt.hour
        most_common_hour_of_day = df['hour'].mode()[0]
        print(f"The most common hour of day: {most_common_hour_of_day}")
    elif month is None and day is not None:
        most_common_month = months[df['month'].mode()[0] - 1]
        print(f"The most common month of travel: {most_common_month}")

        df['hour'] = df['Start Time'].dt.hour
        most_common_hour_of_day = df['hour'].mode()[0]
        print(f"The most common hour of day: {most_common_hour_of_day}")
    elif month is not None and day is None:
        most_common_day_of_week = day_of_week[df['day_of_week'].mode()[0]]
        print(f"The most common day of week: {most_common_day_of_week}")

        df['hour'] = df['Start Time'].dt.hour
        most_common_hour_of_day = df['hour'].mode()[0]
        print(f"The most common hour of day: {most_common_hour_of_day}")
    else:
        df['hour'] = df['Start Time'].dt.hour
        most_common_hour_of_day = df['hour'].mode()[0]
        print(f"The most common hour of day: {most_common_hour_of_day}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip"""

    print('\nCalculating The Most Popular Stations And Trip...\n')
    start_time = time.time()

    counts_start = df['Start Station'].value_counts()[df['Start Station'].mode()[0]]
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most common Start Station: {most_common_start_station},"
          " Count of trips: {counts_start}")

    counts_end = df['End Station'].value_counts()[df['End Station'].mode()[0]]
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most common End Station: {most_common_end_station},"
          " Count of trips: {counts_end}")

    counts_comb = df.value_counts(['Start Station', 'End Station']).max()
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most common Trip from Start to End: {most_common_trip},"
          " Count of trips: {counts_comb}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on trip duration"""

    print('\nCalculating The Total travel '
          'time and The Average travel time...\n')
    start_time = time.time()

    df['Trip Duration'] = df['Trip Duration'].apply(pd.to_timedelta, unit='s')
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time in hh:mm:ss : {total_travel_time}")

    average_travel_time = df['Trip Duration'].mean()
    print(f"Average Travel Time in hh:mm:ss : {average_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on user info"""

    print('\nCalculating The User information...\n')
    start_time = time.time()

    counts_user_type = df['User Type'].value_counts()
    print(f"Counts of each user type:\n{counts_user_type}")

    if city == 'washington':
        print("Gender and Birth year information"
              " is not available for this city")
    else:
        counts_gender = df['Gender'].value_counts()
        print(f"Counts of each gender:\n{counts_gender}")

        earliest_birth_year = df['Birth Year'].min()
        print(f"The earliest year of birth: {earliest_birth_year}")

        most_recent_birth_year = df['Birth Year'].max()
        print(f"The most recent year of birth: {most_recent_birth_year}")

        most_common_birth_year = df['Birth Year'].mode()[0]
        print(f"The most common year of birth: {most_common_birth_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        print('Hello! Let\'s explore some US bikeshare data!')
        city = get_city()
        if get_filters() is None:
            raw_data(city)
        else:
            month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

        restart = input("\nWould you like to restart? "
                        "Enter yes or no.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
