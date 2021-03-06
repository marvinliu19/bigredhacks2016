import datetime
import forecastio
import time


def main():
    """
    Run load_forecast() with the given lat, lng, and time arguments.
    """

    api_key = "ce9fcb652adc05193d2aa663d1a3f4ac"

    lat = 33.5734
    lng = -117.733
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
        print ('TempMin %s' % (daily_data_point.temperatureMin))
        print ('TempMax %s' % (daily_data_point.temperatureMax))
        print ('PrecProb %s' % (daily_data_point.precipProbability))
        if daily_data_point.precipProbability == 0:
            print('PrecType None')
            print('PrecIntensity None')
        else:
            print ('PrecType %s' % (daily_data_point.precipType))
            print ('PrecIntensity %s' % (daily_data_point.precipIntensity))

        tempMin = 'TempMin: ' + str(daily_data_point.temperatureMin)
        print(tempMin)


    day = 0
    fullTextMsg = '\n'

    for daily_data_point in by_day.data:
        temp = 'Temp:' + str(int(daily_data_point.temperatureMin)) + '-' + str(int(daily_data_point.temperatureMax))
        precProb = '{:.0%}'.format(daily_data_point.precipProbability)
        if daily_data_point.precipProbability == 0:
            precProb = precProb + '\n'
            text = temp
        else:
            inten = ''
            if daily_data_point.precipIntensity < .002:
                inten = 'very light '
            elif daily_data_point.precipIntensity < .017:
                inten = 'light '
            elif daily_data_point.precipIntensity < .01:
                inten = 'moderate '
            else:
                inten = 'heavy '

            precType = str(daily_data_point.precipType)
            text = temp + '\n' + precProb + " chance of " + inten + precType
            


        date  = str(datetime.date.today() + datetime.timedelta(days=day))
        date  = date[5:]
        textMsg = date + '\n'

        textMsg = textMsg + text

        fullTextMsg = fullTextMsg + textMsg + '\n'
        day = day + 1
    print (fullTextMsg)


    print (by_day.summary)

if __name__ == "__main__":
    main()





