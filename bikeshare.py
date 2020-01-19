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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #city = input('Please choose from the following cities: Chicago, New York City, Washington: ').lower()
    
    while True:
        city = input('Please choose from the following cities: Chicago, New York City, Washington: ').lower()
        if city in ['chicago','new york city','washington']:
            break
        else:
            print("I'm sorry that was not a valid choice. Please try again.")
            continue
        
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please choose a month from January to June or enter all to see data from all months: ').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june','all']:
            break
        else:
            print("I'm sorry that was not a valid choice. Please try again.")
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please choose a day of the week or enter all to see data from everyday: ').lower()
        if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
            break
        else:
            print("I'm sorry that was not a valid choice. Please try again.")
            continue
        
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
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


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
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most common month is {}.'.format(months[df['month'].mode()[0]-1]))
    # display the most common day of week
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    print('The most common day of the week is {}.'.format(df['day_of_week'].mode()[0]))
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour is {}.'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used starting point is {}.'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used ending point is {}.'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' TO ' + df['End Station']
    print('The most common trip (Start to End) is {}.'.format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Trip Time'] = df['End Time'] - df['Start Time']
    # display total travel time
    print('The total amount of time traveled is {}.'.format(df['Trip Time'].sum()))

    # display mean travel time
    print('The average trip length is {}.'.format(df['Trip Time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('There were {} Subscribers and {} Casual Users.\n'.format(user_types['Subscriber'],user_types['Customer']))
    
    if 'Gender' in df.columns:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        print('There were {} men and {} women.\n'.format(genders['Male'],genders['Female']))
    
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('The oldest user was born in {}.'.format(int(df['Birth Year'].min())))
        print('The youngest user was born in {}.'.format(int(df['Birth Year'].max())))
        print('The most common year of birth was {}.'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks user if they would like to view the first five rows of raw data.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    If the user answers yes: outputs the first five rows from the DataFrame.
    Asks if they would like to see the next five. If yes, outputs those.
    """

    answer = input('Would you like to see the first five lines of data? ').lower()
    if answer == 'yes':
        #definte iteration variables
        i = 0
        j = 4
        #prints the first five rows of the dataframe
        for x in range(i,j):
            print(df.loc[x])
            print()
        while True:    
            answer = input('Would you like to see the next five lines? ').lower()
            if answer != 'yes':
                break
            #If they answer yes adjust the variables of iteration and output the next five rows of data
            i = j + 1
            j += 5
            for x in range(i,j):
                print(df.loc[x])
                print()
        

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
