

#%% 
import requests
import json
import pandas as pd 
# %% 
def query_data(qfilter=''):
    url = 'https://gdr.openei.org/api'
    headers = {
        "accept": "application/json"
    }
    data = {
        'draw': 1,
        'action': 'getSubmissionsWithPermissionsForUser',
        'format': 'json',
        's': 'all',
        'dataTableRequest': True,
        'search[value]':qfilter,
        'length': 0,
    }
    json_data = json.loads(requests.post(url, headers=headers, data=data).text)
    return pd.DataFrame(json_data['result'])

uforge = query_data('utah forge')
# %%


#Get resources from the uforge data and add column with it 
r_list = []
b_list = []
for sub in uforge.itertuples():
    url_id = str(sub.xdrId) + '/'
    url_base='https://gdr.openei.org/files/'
    res = sub.resources
    for r in res:
        if 'actualName' in r.keys():
            url_aname = r['actualName']
            url_res = url_base + url_id + url_aname 
            r_list.append(url_res)
        else:
            b_list.append(r)
            print('Does not have resource thing you can download')

# %% 
check_list = []
for i , row in uforge.iterrows():
    for r in row.resources:
        check_list.append(r)
print(len(check_list))


# %% 
#f = lambda x: x['url'].replace('https://gdr.openei.org/files/','').split('/')[0]
#dff['id']  = dff['url'].apply(f)
dff = pd.DataFrame(r_list, columns=['Url'])
#TODO 
#Merge with dff with uforge database 
dff['xdrId'] = dff['Url'].apply(lambda x: x.split('/')[4])
dff['xdrId'] = dff['xdrId'].astype(int)
uforge['xdrId'] = uforge['xdrId'].astype(int)

#merge on ID 
newdf = uforge.merge(dff, on=['xdrId'], how='outer')
newdf.head

def fetch_utah( url):
    var = url.split('/')
    end = var[-1].split('.')
    if end[-1] == 'zip':
        path = pooch.retrieve(url=url, known_hash=None, processor=Unzip())
    else:
        path = pooch.retrieve(url=url, known_hash=None)
    print(len(path))
    return path

# %%
