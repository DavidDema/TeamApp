

#GOOGLE API
SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/calendar']

# The ID and range of a sample spreadsheet.
#SHEETS
SAMPLE_SPREADSHEET_ID = '1BsbelcuvmYAZsBWTr1-BfuxXHK_zPws6QIpdNmk_7hE'
ADMIN_RANGE = "admin!A1:U"
EVENTS_RANGE = "events!A2:U"
EVENTS_HEADER = "events!A1:U1"
ADD_HEADER = "events2add!A1:U1"
ADD_RANGE = "events2add!A2:U"
#GAMES_RANGE = "games!A2:U"
#TRAININGS_RANGE = "trainings!A2:U"

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

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

def get_channel_id(channel_name=""):
    ch_id = ""
    for n in channel_name_list:
        i = 0
        if n == channel_name:
            ch_id = channel_id_list[i]
            i += 1
    return ch_id