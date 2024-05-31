import time
import pandas as pd
import numpy as np

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # ser input for city
    while True:
        city = input("Choose a city to visualize (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Error! Invalid input. Please enter either chicago, new york city, or washington.")

    # User input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? (january, february, march, april, may, june, or 'all'): ").lower()
        if month in months:
            break
        else:
            print("Error! Invalid input. Please enter a month from the list or 'all'.")

    # User input for day of the week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? (monday, tuesday, wednesday, thursday, friday, saturday, sunday, or 'all'): ").lower()
        if day in days:
            break
        else:
            print("Error! Invalid input. Please enter a day from the list or 'all'.")

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['month'].str.lower() == month]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df

def display_rows(df):
    """Displays 5 rows of the dataframe at a time."""
    start_loc = 0
    while start_loc < len(df):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        if start_loc < len(df):
            if input("\nWould you like to see the next 5 rows? Enter yes or no: ").lower() != 'yes':
                break

def show_descriptive_stats(df_column):
    """Displays descriptive statistics."""
    stats = df_column.describe()
    print(stats)

def time_stats(df, original_df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Here for the most common month
    most_common_month = df['month'].mode()[0]
    print(f"The most common month is: {most_common_month}")

    # Here for the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of week is: {most_common_day}")

    # Here for the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {most_common_hour}:00")

    # Asks if user wants to see descriptive statistics
    if input("\nWould you like to see descriptive statistics for the most common start hour? Enter yes or no: ").lower() == 'yes':
        print("\nDescriptive statistics for the most common start hour:")
        original_df['hour'] = original_df['Start Time'].dt.hour
        show_descriptive_stats(original_df['hour'])
    
    # Asks if user wants to see 5 rows of the original dataframe
    if input("\nWould you like to see the first 5 rows of the original dataframe? Enter yes or no: ").lower() == 'yes':
        display_rows(original_df)

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def station_stats(df, original_df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Here for most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {most_common_start_station}")

    # Here for most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {most_common_end_station}")

    # Here for most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print(f"The most common trip is: {most_common_trip}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df, original_df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Here for total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time / 3600
    total_travel_time_days = total_travel_time_hours / 24
    print(f"The total travel time is: {total_travel_time} seconds ({total_travel_time_hours:.2f} hours or {total_travel_time_days:.2f} days)")

    # Here for mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_minutes = mean_travel_time / 60
    print(f"The average travel time is: {mean_travel_time:.2f} seconds ({mean_travel_time_minutes:.2f} minutes)")

    # Asks if user wants to see descriptive statistics
    if input("\nWould you like to see descriptive statistics for trip duration? Enter yes or no: ").lower() == 'yes':
        print("\nStatistics for trip duration:")
        show_descriptive_stats(original_df['Trip Duration'])

    # Asks if user wants to see 5 rows of the original dataframe
    if input("\nWould you like to see the first 5 rows of the original dataframe? Enter yes or no: ").lower() == 'yes':
        display_rows(original_df)

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def user_stats(df, original_df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Here for counts of user types
    print("Counts of user types:")
    print(df['User Type'].value_counts())

    # Ask if user wants to see descriptive statistics
    if input("\nWould you like to see descriptive statistics for user types? Enter yes or no: ").lower() == 'yes':
        print("\nStatistics for user types:")
        show_descriptive_stats(original_df['User Type'])

    # Ask if user wants to see 5 rows of the original dataframe
    if input("\nWould you like to see the first 5 rows of the original dataframe? Enter yes or no: ").lower() == 'yes':
        display_rows(original_df)

    # Here for the counts of gender
    if 'Gender' in df.columns:
        print("\nCounts of gender:")
        print(df['Gender'].value_counts())

        # Ask if user wants to see descriptive statistics
        if input("\nWould you like to see descriptive statistics for gender? Enter yes or no: ").lower() == 'yes':
            print("\nStatistics for gender:")
            show_descriptive_stats(original_df['Gender'])

        # Ask if user wants to see 5 rows of the original dataframe
        if input("\nWould you like to see the first 5 rows of the original dataframe? Enter yes or no: ").lower() == 'yes':
            display_rows(original_df)
    else:
        print("\nSorry! Gender data is not available for this city.")

    # Displays oldest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]

        print(f"\nEarliest year of birth: {oldest_year}")
        print(f"Most recent year of birth: {recent_year}")
        print(f"Most common year of birth: {common_year}")

        # Asks if user wants to see descriptive statistics
        if input("\nWould you like to see descriptive statistics for birth year? Enter yes or no: ").lower() == 'yes':
            print("\nStatistics for birth year:")
            show_descriptive_stats(original_df['Birth Year'])

        # Asks if user wants to see 5 rows of the original dataframe
        if input("\nWould you like to see the first 5 rows of the original dataframe? Enter yes or no: ").lower() == 'yes':
            display_rows(original_df)
    else:
        print("\nUnfortunate! For this city there is no data about users birth date.")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        original_df = df.copy()

        time_stats(df, original_df)
        station_stats(df, original_df)
        trip_duration_stats(df, original_df)
        user_stats(df, original_df)

        restart = input('\nDo you want to run another visualization? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
