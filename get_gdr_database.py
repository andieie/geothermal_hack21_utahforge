

#%% 
import requests
import json
import pandas as pd 
from IPython.core.display import display, HTML

# %% 
def query_data(qfilter=''):
    """[summary]

    Args:
        qfilter (str, optional): Any string to query in the database ie: 'utah forge', 'EE0007080'. Defaults to ''.

    Returns:
        Submissions: Pandas Dataframe of submissions according to the query in qfilter
    """
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
    submissions = pd.DataFrame(json_data['result'])
    submissions.drop(['email','phone'], axis=1, inplace=True)
    return submissions


def merge_dataframes(df_submissions, baseurl='https://gdr.openei.org/files/'):
    """Gives us back a dataframe with downloadable resources. Every row is a downloadable thing. 

    Args:
        df_submissions ([type]): [description]
        baseurl (str, optional): [description]. Defaults to 'https://gdr.openei.org/files/'.
    """
    r_list = []
    id_list = []
    for i, sub in df_submissions.iterrows():
        url_id = str(sub['xdrId']) + '/'
        res = sub.resources
        for r in res:
            if 'actualName' in r.keys():
                url_aname = r['actualName']
                url_res = baseurl + url_id + url_aname 
                r_list.append(url_res)
            else:
                print(f'Does not have resource thing you can download for index {url_id}' )

    dff = pd.DataFrame(r_list, columns=['url'])
    dff['xdrId'] = dff['url'].apply(lambda x: x.split('/')[4])
    dff['xdrId'] = dff['xdrId'].astype(int)
    df_submissions['xdrId'] = df_submissions['xdrId'].astype(int)
    df = df_submissions.merge(dff, on=['xdrId'], how='outer')
    df.drop(['_id','status','loggedInUser'], axis=1, inplace=True)
    return df


def make_link(url):
    """[summary]

    Args:
        url ([type]): [description]
    """
    actual_name = url.split('/')[-1]
    return display(HTML(f"""<a href={url}>{actual_name}</a>"""))
    

def download_data(row):
    """Work in progress

    Args:
        row ([type]): [description]

    Returns:
        [type]: [description]
    """
    var = url.split('/')
    end = var[-1].split('.')
    if end[-1] == 'zip':
        path = pooch.retrieve(url=url, known_hash=None, processor=Unzip())
    else:
        path = pooch.retrieve(url=url, known_hash=None)
    print(len(path))
    return path
