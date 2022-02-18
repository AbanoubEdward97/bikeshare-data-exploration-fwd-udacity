import calendar
from cmath import nan
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
    global days_of_the_week
    days_of_the_week=[calendar.day_name[i].title() for i in range(7)];days_of_the_week.append("All")
    global months
    months=[calendar.month_name[i] for i in range(1,7)];months.append("All")
    global city
    city,month,day="","",""
    while city not in CITY_DATA:
        city=input("What city would you like to see data for [Chicago, New york, Washington]:\n").lower()
        if city not in CITY_DATA:
            print("Invalid input , please enter the name of city correctly !!")
    # get user input for month (all, january, february, ... , june)
    while month not in months:
        month=input("Enter the month you want to analyse or enter 'all' to analyse all months (e.g:June or june): ").title()
        if month not in months:
            print("Invalid input , please enter the name of the month correctly")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days_of_the_week:
        day=input("Enter the week day you want to analyse or enter 'all' to analyse all days (e.g:Saturday or saturday): ").title()
        if day not in days_of_the_week:
            print("Invalid input , please enter the name of the day correctly")
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
    city_data=pd.read_csv(f"./{CITY_DATA[city]}")
    city_data["Start Time"],city_data["End Time"]=pd.to_datetime(city_data["Start Time"]),pd.to_datetime(city_data["End Time"])
    if month != "All":
        city_month_data=city_data[city_data["Start Time"].dt.month == months.index(month)+1] 
    else:
        city_month_data =city_data
    if day != "All":
        city_month_data=city_month_data[city_data["Start Time"].dt.weekday == days_of_the_week.index(day)]
    # displaying consequent five rows from the data to be analysed based on user requries
    display_rows=""
    while display_rows not in ["yes","no"]:
        display_rows=input("Would you like to display some of the data: (yes or no): ").lower()
        if display_rows not in ["yes" , "no"]:
            print("Invalid Input !! , please enter (yes or no)")
        elif display_rows =="yes":
            i=0
            while display_rows == "yes":
                try:
                    n_rows=int(input("enter the number of rows you want to display: "))
                    print(city_month_data.iloc[i:i+n_rows,:])
                    i+= n_rows
                except ValueError:
                    print("number of rows must be positive integers !!")
                display_rows=input("Would you like to display next some rows again:(yes or no): ").lower()
                while display_rows not in ["yes" , "no"]:
                    display_rows=input("Invalid Input !! , please enter (yes or no): ").lower()
    return(city_month_data)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df["months"]=df["Start Time"].dt.month
    df["days"]=df["Start Time"].dt.weekday
    df["start_hour"]=df["Start Time"].dt.hour
    # display the most common month
    print(f" the most common month is: {months[(df['months'].mode()[0])-1]}")
    # display the most common day of week
    print(f" the most common day of week is: {days_of_the_week[df['days'].mode()[0]]} , count:{max(df['days'].value_counts())}")
    # # display the most common start hour
    print(f" the most common start hour is: {df['start_hour'].mode()[0]} , count:{max(df['start_hour'].value_counts())}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most commonly used start station : {df['Start Station'].mode()[0]} with counts: {df['Start Station'].value_counts()[0]}")

    # display most commonly used end station
    print(f"The most commonly used end station : {df['End Station'].mode()[0]} with counts: {df['End Station'].value_counts()[0]}")


    # display most frequent combination of start station and end station trip
    df["combination"]=df["Start Station"]+","+df["End Station"]
    combination=df["combination"].mode()[0].split(",")
    print(f"The combination of stations are: start :{combination[0]} , end:{combination[1]}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total=sum(df["Trip Duration"])
    mean=df["Trip Duration"].mean()
    print(f"total travel time duration: {total//(3600*24)} Days, {(total%(3600*24))//(3600)} Hours, {((total%(3600*24))%(3600))//60} Minutes, {((total%(3600*24))%(3600))%60} Seconds")
    # display mean travel time
    print(f"Mean travel time duration: {mean//3600} hours {(mean%3600)//60} minutes {round((mean % 3600)%60,2)} seconds")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for i in range(len(df["User Type"].value_counts())):
        print(f"user type: {df['User Type'].value_counts().index[i]} , counts: {df['User Type'].value_counts()[i]}")
    # solution for washington dataset (doesn't contain gender and birth year)
    if city != "washington":
        # Display counts of gender
        print(f"counts of gender:\n{df['Gender'].value_counts()}")
        # Display earliest, most recent, and most common year of birth
        most_common =df["Birth Year"].mode()[0]
        birth_date=df["Birth Year"]
        birth_date.dropna(axis=0,inplace=True)
        most_recent=max(birth_date)
        most_early=min(birth_date)
        print(f"The earliest year of birth is: {most_early}\n,most recent: {most_recent}\n, most common: {most_common}")
    else:
        print("Sorry , The information on Gender and Birth Year for Washington city is not available")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters() # done
        df = load_data(city, month, day) #done
        time_stats(df) #done 
        station_stats(df) #1 required 
        trip_duration_stats(df) #done 
        user_stats(df) 

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
    main()
