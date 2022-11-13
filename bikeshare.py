import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': '/Users/macbookpro/Desktop/udacity/all-project-files/chicago.csv',
             'new york city': '/Users/macbookpro/Desktop/udacity/all-project-files/new_york_city.csv',
             'washington': '/Users/macbookpro/Desktop/udacity/all-project-files/washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            "\nName of the city to analyze(chicago, new york city or washington): ").lower()
        print("\nYou choose: ", city)
        if city not in ('chicago', 'new york city', 'washington'):
            print("Please enter the name of the city in strings as shown")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "\nname of the month to filter by(january, february, ... , june), or 'all' to apply no month filter: ").lower()
        print("\nYou choose: ", month)
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("\nPlease enter the name of the month in strings as shown")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nname of the day of week to filter by('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'), or 'all' to apply no day filter: ").lower()
        print("\nYou choose: ", day)
        if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print("\nPlease enter the name of the day in strings as shown")
            continue
        else:
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: ", df['month'].mode()[0])

    # display the most common day of week
    print("The most common day of week is: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # we get the maxium index of the value of the start station
    start_station = df['Start Station'].value_counts().idxmax()
    print("The most commnly used start staiton is: ", start_station)
    # display most commonly used end station
    # we get the maxium index of the value of the end station
    end_station = df['End Station'].value_counts().idxmax()
    print("The most commnly used end staiton is: ", end_station)
    # display most frequent combination of start station and end station trip
    # we count the most used indexes in both stations
    both_stations = df.groupby(['Start Station', 'End Station']).count()
    print("The most frequent combinaition of start station and end station:",
          start_station, " --And-- ", end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # this will calculate the the time in seconds
    total_travel_time = sum(df['Trip Duration'])
    print("The total time travel: ", total_travel_time,
          " in seconds and ", total_travel_time/3600, " in hours")
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: ", mean_travel_time,
          " in seconds and ", mean_travel_time/3600, " in hours")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("\nCounts of the user: ", user_type)
    # Display counts of gender
    try:  # As there's some users didn't assign thier genders so we use try and except to avoid errors
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:', gender_types)
    except KeyError:
        print("\nunfortunately, there's no data available")
    # Display earliest, most recent, and most common year of birth
    try:  # As there's some users didn't assign thier birth year so we use try and except to avoid erros
        earliest = df['Birth Year'].min()
        print('\nEarliest year of birth:', earliest)
    except KeyError:
        print("\nunfortunately, there's no data available")

    try:  # As there's some users didn't assign thier birth year so we use try and except to avoid erros
        most_recent = df['Birth Year'].max()
        print('\nMost recent year of birth:', most_recent)
    except KeyError:
        print("\nunfortunately, there's no data available")

    try:  # As there's some users didn't assign thier birth year so we use try and except to avoid erros
        most_comman_year = df['Birth Year'].value_counts().idxmax()
        print('\nMost comman year of birth:', most_comman_year)
    except KeyError:
        print("\nunfortunately, there's no data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    start_loc = 0
    while True:
        view_data = input(
            "Would you like to view 5 rows of individual trip data? Enter yes or no?: ").lower()
        if (view_data == 'yes'):
            print(df.iloc[start_loc: start_loc+5])
            start_loc += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
