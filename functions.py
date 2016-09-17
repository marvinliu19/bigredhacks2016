import datetime
import forecastio

def sevenDayForecast(lat, lng):
    api_key = "ce9fcb652adc05193d2aa663d1a3f4ac"

    forecast = forecastio.load_forecast(api_key, lat, lng)

    by_day = forecast.daily()

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
    return (fullTextMsg)

if __name__ == "__sevenDayForecast__":
    sevenDayForcast(33, -117)
