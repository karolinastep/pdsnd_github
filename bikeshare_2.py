import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_name = CITY_DATA.keys()
    months_all = ['all','january', 'february', 'march', 'april', 'may', 'june']
    days_all = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington? \n').lower()
        if city not in city_name:
            print('\nPlease provide valid city name.\n')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to filter the data by month?\nIf yes, please type January, February, March, April, May or June.\n If not, please type all.\n').lower()
        if month not in months_all:
            print('\nPlease provide valid month.\n')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    'Would you like to filter the data by day?'
    while True:
        day = input('Would you like to filter the data by day?\nIf yes, please type day from Monday to Sunday.\n If not, please type all.\n').lower()
        if day not in days_all:
            print('\nPlease provide valid day.\n')
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
    # load data file into a dataframe
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
    months = ['january', 'february', 'march', 'april', 'may', 'june']    
    popular_month_index = df['month'].mode()[0]
    popular_month = months[popular_month_index-1].title()
    print('Most popular month is: ', popular_month)
    
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day of week is: ', popular_day)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour is: ', popular_hour)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_sstation = df['Start Station'].mode()[0]
    print('Most popular start station is: ', popular_sstation)

    # display most commonly used end station
    popular_estation = df['End Station'].mode()[0]
    print('Most popular end station is: ', popular_estation)

    # display most frequent combination of start station and end station trip
    df['station_comb'] = df['Start Station'] + '///' + df['End Station']
    popular_station_comb = df['station_comb'].mode()[0].split('///')    
    print('Most popular trip is from {} to {}.'.format(popular_station_comb[0],popular_station_comb[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = np.sum(df['Trip Duration'])
    print('Total travel time is: {} seconds.'.format(total_travel))

    # display mean travel time
    avg_travel = np.mean(df['Trip Duration'])
    print('Average travel time is: {} seconds.'.format(avg_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users if the data was provided."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(pd.DataFrame(user_types))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(pd.DataFrame(gender))
    else:
        print('Gender not provided.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = np.nanmin(df['Birth Year'])
        recent = np.nanmax(df['Birth Year'])
        common = df['Birth Year'].mode()[0]
        print('The oldest customer was born in {}. The youngest customer was born in {}. The most common year of birth is {}.'.format(int(earliest), int(recent), int(common)))
    else:
        print('Birth Year not provided')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 rows of raw data based on request."""
    
    j = 0
    while True:
        k = j+5
        raw_d = input('Would you like to see raw data? Enter yes or no.\n').lower()
        if raw_d != 'yes':
            break
        for i in range(j,k,1):
            print(df.iloc[i])
        j += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
