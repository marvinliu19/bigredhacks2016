import datetime
import forecastio

def sevenDayForcast():
    api_key = "ce9fcb652adc05193d2aa663d1a3f4ac"

    lat = 40.7128
    lng = -74.0059

    forecast = forecastio.load_forecast(api_key, lat, lng)

    by_day = forecast.daily()

    day = 1
    fullTextMsg = ''

    for daily_data_point in by_day.data:
        tempMin = 'TempMin: ' + str(daily_data_point.temperatureMin)
        tempMax = 'TempMax: ' + str(daily_data_point.temperatureMax)
        precProb = 'PrecProb: ' + str(daily_data_point.precipProbability)
        if daily_data_point.precipProbability == 0:
            precType = 'PrecType: None'
            precInten = 'precInten: 0'
        else:
        	precType = 'PrecType: ' + str(daily_data_point.precipType)
        	precInten = 'precInten: ' + str(daily_data_point.precipIntensity)

        textMsg = 'Day' + str(day)

        textMsg = textMsg + '\n' + tempMin + '\n' + tempMax + '\n' + precProb
        if daily_data_point.precipProbability != 0:
        	textMsg = textMsg + '\n' + precType + '\n' + precInten

        fullTextMsg = fullTextMsg + textMsg + '\n'
        day = day + 1
    return (fullTextMsg)





if __name__ == "__sevenDayForecast__":
    sevenDayForcast()