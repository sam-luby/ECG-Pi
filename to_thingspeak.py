import urllib.request

API_KEY_READ = '9VSOE6M365ZBTHTU'

API_KEY_WRITE = 'QVN6DOKQAI2WK4MR'
channels = {'field1': 'bpm', 'field2': 'rmssd', 'field3': 'sdnn', 'field4': 'pNNx'}
baseurl = 'http://api.thingspeak.com/update?api_key=' + API_KEY_WRITE

def update_channel(results):
    data_to_update = ''
    for channel in channels:
        data_to_update += ('&' + str(channel) + '=' + str(results[channels[channel]]))
    f = urllib.request.urlopen(baseurl+str(data_to_update))
    f.read()
    f.close()