import urllib.request

# API keys for reading and writing
API_KEY_READ = 'LZIJ17H3NMAT172L'
API_KEY_WRITE = 'UKOEUS8UIZOU0XAJ'

# fields to upload
channels = {'field1': 'bpm', 'field2': 'rmssd', 'field3': 'sdnn', 'field4': 'pNNx'}
baseurl = 'http://api.thingspeak.com/update?api_key=' + API_KEY_WRITE

# update the thingspeak channel with the results for each field
def update_channel(results):
    data_to_update = ''
    for channel in channels:
        data_to_update += ('&' + str(channel) + '=' + str(results[channels[channel]]))
    f = urllib.request.urlopen(baseurl+str(data_to_update))
    f.read()
    f.close()