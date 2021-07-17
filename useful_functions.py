import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city():
    '''Get the city to perform data analysis on it.'''
    city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()
    while city not in CITY_DATA:
        print("\nPlease choose a city from the given cities")
        city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()    
    return city

def filtering_features():
    '''Get filering method from user.'''
    time_filters = ['month', 'day', 'both', 'none']    
    time_filter = input("Would you like to filter data by month, day, both, or not at all? Type none for no time filter. ").lower()
    while time_filter not in time_filters:
        print("Please enter a correct time filter")
        time_filter = input("Would you like to filter data by month, day, both, or not at all? Type none for no time filter. ").lower()
    return time_filter

def get_month():
    '''Get specific month from user to filter data based on it.'''
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input("\nWhich month? January, February, March, April, May, or June ").lower()
    while month not in months:
        print("]nPlease enter a correct month from the given months")
        month = input("Which month? January, February, March, April, May, or June ").lower()  
    return month

def get_day():
    '''Get specific day from user to filter data based on it.'''
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday ").lower()
    while day not in days:
        print("\nPlease enter a correct day from the given days")
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday ").lower()
    return day

def get_time_filters():
    '''Return month and day to filter data using them'''
    time_filter = filtering_features()
        
    if time_filter == 'month':
        month = get_month()
        day = 'all'
    
    elif time_filter == 'day':
        day = get_day()
        month = 'all'
   
    elif time_filter == 'both':
        month = get_month()       
        day = get_day()
   
    elif time_filter == 'none':
        month = 'all'
        day = 'all'
    
    return month, day
    
def load_data(city, month, day):
    '''
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day 
    '''
    city_data = pd.read_csv(CITY_DATA[city])

    city_data['Start Time'] = pd.to_datetime(city_data['Start Time'])
    city_data['day_of_week'] = city_data['Start Time'].dt.day_name()
    city_data['day_of_week'] = city_data['day_of_week'].apply(lambda day:day.lower())
    city_data['month'] = city_data['Start Time'].dt.month
    city_data['hour'] = city_data['Start Time'].dt.hour
    city_data['trip_stations'] = city_data['Start Station'] + "->" +city_data['End Station']

    if month != 'all':
        month = month.lower() 
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        months_map = pd.DataFrame(data = np.arange(1,7).reshape(1,6), columns= months)
        month = months_map[month].values[0]
        city_data = city_data[city_data['month'] == month]
    
    if day !='all':
        day = day.lower()
        city_data = city_data[city_data['day_of_week'] == day]        
    
    return city_data

def time_statistical_analysis(city_data):
    '''
    Calculate time based statistical analysis on a pandas Data frame containing filtered city data .
    
    Args:
        (Pandas DataFrame) city_data - data frame of the data to do analysis on it 
    '''
    popular_month = city_data['month'].mode()[0]
    popular_day = city_data['day_of_week'].mode()[0]
    popular_hour = city_data['hour'].mode()[0]
    print("\nThe most common bikeshare month: {}".format(popular_month))
    print("The most common bikeshare day of weak: {}".format(popular_day))
    print("The most common bikeshare hour of day: {}\n".format(popular_hour))

def stations_statistical_analysis(city_data):
    '''
    Calculate place based statistical analysis on a pandas Data frame containing filtered city data .
    
    Args:
        (Pandas DataFrame) city_data - data frame of the data to do analysis on it 
    '''    
    popular_start_station = city_data['Start Station'].mode()[0]
    popular_end_station = city_data['End Station'].mode()[0]
    print("\nThe most common bikeshare start station: {}".format(popular_start_station))
    print("The most common bikeshare end station: {}\n".format(popular_end_station))

def trip_statistical_analysis(city_data):
    '''
    Calculate statistical analysis on trips of a pandas Data frame containing filtered city data .
    
    Args:
        (Pandas DataFrame) city_data - data frame of the data to do analysis on it 
    '''  
    popular_trip = city_data['trip_stations'].mode()[0]
    trip_travel_time = city_data['Trip Duration'].sum()
    trip_average_time = city_data['Trip Duration'].mean()
    print("\nThe most common bikeshare trip from {} to {}".format(popular_trip.split("->")[0],popular_trip.split("->")[1]))
    print("Trip total travel time: {}".format(trip_travel_time))
    print("Trip average travel time: {}\n".format(trip_average_time))

def user_info(city_data, city):
    '''
    Calculate statistical analysis on the users using bikeshare system.
    
    Args:
        (Pandas DataFrame) city_data - data frame of the data to do analysis on it 
        (str) city - name of the city to analyze 
    '''  
    user_types = city_data['User Type'].value_counts()
    print ("\nUser types:\n{}".format(user_types))
    if city != "washington":    
        gender_type = city_data['Gender'].value_counts()
        earliest_year_of_birth = city_data['Birth Year'].min()
        most_recent_year_of_birth = city_data['Birth Year'].max()
        most_common_year_of_birth = city_data['Birth Year'].mode()[0]
        print ("\nGender types:\n{}\n".format(gender_type))
        print ("The earliest year of birth: {}".format(int(earliest_year_of_birth)))
        print ("The most recent year of birth: {}".format(int(most_recent_year_of_birth)))
        print ("The most common year of birth: {}\n".format(int(most_common_year_of_birth)))
        
def statistical_analysis(city_data, city):
    '''
    Calculate statistical analysis on the filtered data of a given city.
    
    Args:
        (Pandas DataFrame) city_data - data frame of the data to do analysis on it 
        (str) city - name of the city to analyze        
    '''
    time_statistical_analysis(city_data)
    stations_statistical_analysis(city_data)
    trip_statistical_analysis(city_data)
    user_info(city_data, city)

def display_data_sample(city_data):
    '''Display data samples of a given data frame'''
    i = 0
    while True:
        try:
            display_Sample_data = input('\nWould you want to see the raw data? Type Yes or No ').lower()
        except:
            print("\nYou should enter Yes or No")
            continue
        if display_Sample_data == 'yes':
            print("Data samples:\n")
            for data_sample in np.arange(i,i+5):
                print(city_data.iloc[data_sample])
                print("\n")
            i += 5
        elif display_Sample_data == 'no':
            i = 0
            break
    
def restart_program():
    '''
    Restart the program based on the user input
        
    Return:
        yes : user wants to restart the program
        No : user does not want to restart the program
    '''
    restart = input("\nWould you like to restart? Type Yes or No ").lower()
    while restart not in ['yes','no']:
        print("\nyou should enter Yes or No")
        restart = input("Would you like to restart? Type Yes or No\n").lower()
    return restart