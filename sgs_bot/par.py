

#GOOGLE API
SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/calendar']

# The ID and range of a sample spreadsheet.
#SHEETS
SAMPLE_SPREADSHEET_ID = '1R7JQG9c9OKFVb0nDidglLzfBdUg1iUdxTjxuut1UE9Q'

GAMES_RANGE = "events!A2:U"
GAMES_HEADER = "events!A1:U1"

SPIELE16_RANGE = "spiele16!A2:U"
SPIELE16_HEADER = "spiele16!A1:U1"
SPIELE07_RANGE = "spiele07!A2:U"
SPIELE07_HEADER = "spiele07!A1:U1"
TRAININGS_RANGE = "trainings!A2:U"
TRAININGS_HEADER = "trainings!A1:U1"

RANGE_LIST = [SPIELE07_RANGE,SPIELE16_RANGE,TRAININGS_RANGE]

g_maps_url = "https://www.google.com/maps/search/?api=1&query="

#SLACK
SPIELE16_ID = 'C02DDAQ75LN'
SPIELE07_ID= 'C02DL352VKM'
TRAININGS_ID = 'C02DS9EFFHA'
ALLGEMEIN_ID = 'C022KD5AH8U'
TEST_ID ='C022A67PNQ5'

channel_name_list = ["test", "spiele16", "spiele07", "trainings"]
channel_id_list = [TEST_ID, SPIELE16_ID, SPIELE07_ID, TRAININGS_ID]

#ICS grabber
URL_16 = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~1165862735024510172-T-x.ics"
URL_07 = "https://fussballoesterreich.at/netzwerk/icalendar/670725461856634215_485215725~665233077005870945-T-x.ics"

#TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
TIME_FORMAT = '%d/%m/%Y %H:%M'


def get_header(range):

    if range == SPIELE16_RANGE:
        return SPIELE16_HEADER
    elif range == SPIELE07_RANGE:
        return SPIELE07_HEADER
    elif range == TRAININGS_RANGE:
        return TRAININGS_HEADER
    else:
        print("No header found")
        return "NOHEADERFOUND"