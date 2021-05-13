

#%% 
import requests
import json

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

#TODO 
#Merge with dff with uforge database 
dff['id'] = dff['url'].apply(lambda x: x.split('/')[4])




# %%
