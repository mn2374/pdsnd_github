import numpy as np
import pandas as pd
import time

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITIES = ["chicago", "new york city", "washington"]
MONTHS = ["all", "january", "febuary", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAYS = ["all", "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]


def get_input(prompt, corpus):
    while True:
        try:
            corpus_text = ", ".join(corpus)
            data = input(f"{prompt} ({corpus_text}): ").lower()
            assert data in corpus, f"invalid input please select one of {corpus_text}"
            return data.lower()
        except Exception as e:
            print(e)


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
    city = get_input("select city", CITIES)

    # get user input for month (all, january, february, ... , june)
    month = get_input("select month", MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_input("select day", DAYS)
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["Month"] = df["Start Time"].apply(lambda x: x.month)
    if month != "all":
        df = df.where(df["Month"] ==
                      MONTHS.index(month))
    df["Day"] = df["Start Time"].apply(lambda x: x.weekday())
    if day != "all":
        df = df.where(df["Day"] ==
                      DAYS.index(day))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("most common month", MONTHS[int(df.Month.value_counts().idxmax())])

    # display the most common day of week
    print("most common day", DAYS[int(df.Day.value_counts().idxmax())])

    # display the most common start hour
    print("most common hour", df["Start Time"].apply(
        lambda x: x.hour).value_counts().idxmax()+1)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most common start station",
          df["Start Station"].value_counts().idxmax())

    # display most commonly used end station
    print("most common end station",
          df["End Station"].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print("most common station pair ",
          df.groupby(["Start Station", "End Station"]).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("total travel time", (df["End Time"] - df["Start Time"]).sum())

    # display mean travel time
    print("mean travel time", (df["End Time"] -
                               df["Start Time"]).mean().total_seconds() / 60, "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User type counts")
    print(df["User Type"].value_counts())

    if "Gender" in df:
        # Display counts of gender
        print("User gender Counts")
        print(df["Gender"].value_counts())
    
    if "Birth Year" in df:

        # Display earliest, most recent, and most common year of birth
        birth_year = df["Birth Year"]
        print("oldest user year")
        print(int(birth_year.min()))
        print()

        print("youngest user year")
        print(int(birth_year.max()))
        print()

        print("most common user birth year")
        print(int(birth_year.value_counts().idxmax()))
        print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    offset = 0
    while input("\nWould you like to see 5 rows of raw data? Enter yes or no.\n").lower() == "yes":
        print(df.iloc[offset:offset+5])
        offset += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
