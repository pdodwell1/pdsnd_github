import time
import pandas as pd
import numpy as np
import math

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_dict = { 'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6 }
days_dict = { 'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6 }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs

    while 1:
        city = input("\nPlease select a city from the following..."
                    "\nChicago, New York City, or Washington: ").lower()
        if city not in CITY_DATA:
            print("\nInvalid input.")
            continue
        city = CITY_DATA[city]
        break

    while 1:
        month_day_filter = input("\nWould you like to filter the data?"
                                "\n'Yes' gives you the option to filter by month and/or day of week"
                                "\n'No' displays all data: ").lower()
        if month_day_filter == 'yes':
            month_day_filter = True
        elif month_day_filter == 'no':
            month_day_filter = False
        else:
            print('\nInvalid input.')
            continue
        break

    # get user input for month (all, january, february, ... , june)


    # get user input for day of week (all, monday, tuesday, ... sunday)

    while 1:
        if month_day_filter:
            filter = input('\nPlease select one of the following: month, day, or month and day: ').lower()
            if filter == 'month':
                month = input("\nPlease select a month from the following... "
                            "\nJanuary, February, March, April, May, or June: ").lower()
                if month not in months_dict:
                    print('\nInvalid input.')
                    continue
                month = months_dict[month]
                day='all'
            elif filter=='day':
                day = input("\nPlease enter a day of the week... "
                            "\nSunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday: ").lower()
                if day not in days_dict:
                    print('\nInvalid input.')
                    continue
                day = days_dict[day]
                month='all'
            elif filter=='month and day':
                month = input("\nPlease select a month from the following... "
                            "\nJanuary, February, March, April, May, or June: ").lower()
                if month not in months_dict:
                    print('\nInvalid input.')
                    continue
                month = months_dict[month]
                day = input("\nPlease enter a day of the week... "
                            "\nSunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday: ").lower()
                if day not in days_dict:
                    print('\nInvalid input.')
                    continue
                day = days_dict[day]
            else:
                print('\nInvalid input.')
                continue
            break
        else:
            month='all'
            day='all'
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract fields from Start Time to create columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']

   # filter by day and/or month if applicable
    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: {}".format(str(df['month'].mode().values[0])))

    # display the most common day of week
    print("The most common day of the week is: {}".format(str(df['day_of_week'].mode().values[0])))

    # display the most common start hour
    print("The most common hour is: {}".format(str(df['hour'].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {}".format(str(df['Start Station'].mode().values[0])))

    # display most commonly used end station
    print("The most common end station is: {}".format(str(df['End Station'].mode().values[0])))

    # display most frequent combination of start station and end station trip
    print("The most common trip is: {}".format(str(df['trip'].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is: {}".format(str(df['Trip Duration'].sum())))

    # display mean travel time
    print("The average travel time is: {}".format(str(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("Number of user types:\n",user_type,"\n")

    # Display counts of gender

    if 'Gender' in df:

        gender = df['Gender'].value_counts()
        print("Gender:\n",gender,"\n")

    # Display earliest, most recent, and most common year of birth
        print("Earliest birth year: {}".format(str(int(df['Birth Year'].min()))))
        print("Most recent birth year: {}".format(str(int(df['Birth Year'].max()))))
        print("Most common birth year: {}".format(str(int(df['Birth Year'].mode().values[0]))))
    else:
        print("There is no gender or birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):

    # show raw data
    start_line = 0
    end_line = 5

    show_data = input("Would you to see the raw data, yes or no: ").lower()

    if show_data == 'yes':
        while end_line <= df.shape[0] - 1:

            print(df.iloc[start_line:end_line,:])
            start_line += 5
            end_line += 5

            show_data_end = input("Would you like to see more data?: ").lower()
            if show_data_end == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nStart again, yes or no: ').lower()
        print()
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
