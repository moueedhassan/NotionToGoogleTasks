import requests

NOTION_TOKEN = ""
DATABASE_ID = ""

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

payload = {
    "filter": {
        "and": [
            {
                "property": "Property",
                "select": {
                    "does_not_equal": "Programming"
                }
            },
            {
                "or": [
                    {
                        "property": "Status",
                        "select": {
                            "equals": "To Do"
                        }
                    },
                    {
                        "property": "Status",
                        "select": {
                            "equals": "Doing"
                        }
                    }
                ]
            }
        ]
    }
}

def notion():

    #post request to query tasks database
    response = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=headers, json=payload)

    if response.status_code == 200:
        results = response.json()
    else:
        print(f"Failed to retrieve data from Notion API. Status code: {response.status_code}")


    #filter out the results 
    dict_list = results['results']

    misc = []
    coursework = []

    for dict in dict_list:

        
        task = {}
        #Extracting name
        name = dict['properties']['Name']['title'][0]['plain_text']

        #Extracting due_date
        try: 
            due_date = dict['properties']['Due Date']['date']['end']  
    
        except:
            due_date = None
    
        task['title'] = name
        task['due'] = due_date

        if dict['properties']['Property']['select']['name'] == 'Misc':
            misc.append(task)
    
        else: 
            coursework.append(task)
    
    return misc, coursework

