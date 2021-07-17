# import used libraries
import useful_functions as uf

def main():
    while True:
        print("Hello! let's get some insights from US bikeshare data")
        city = uf.get_city()
        month, day = uf.get_time_filters()
        city_data = uf.load_data(city, month, day)
        uf.statistical_analysis(city_data, city)
        uf.display_data_sample(city_data)
        restart = uf.restart_program()
        if restart == 'yes':
            continue
        elif restart == 'no':
            break

if __name__ == '__main__':
    main()




    
