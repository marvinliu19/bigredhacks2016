import datetime
import forecastio


def main():
    """
    Run load_forecast() with the given lat, lng, and time arguments.
    """

    api_key = "ce9fcb652adc05193d2aa663d1a3f4ac"

    lat = 40.7128
    lng = -74.0059
    time = datetime.datetime(2016, 2, 27, 6, 0, 0)

    forecast = forecastio.load_forecast(api_key, lat, lng)

    print "===========Currently Data========="
    print forecast.currently()

    print "===========Hourly Data========="
    by_hour = forecast.hourly()
    print "Hourly Summary: %s" % (by_hour.summary)


    min = 500
    high = 0
    for hourly_data_point in by_hour.data:
        print hourly_data_point
        if hourly_data_point.temperature < min:
            min = hourly_data_point.temperature 
        if hourly_data_point.temperature >high:
            high = hourly_data_point.temperature 
    print min
    print high
    
        


    print "===========Daily Data========="
    by_day = forecast.daily()
    print "Daily Summary: %s" % (by_day.summary)

    for daily_data_point in by_day.data:
        print daily_data_point

    print ('asdf')
    print (by_day.summary)


if __name__ == "__main__":
    main()