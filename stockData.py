import requests
import data

url = "https://www.hsx.vn/Modules/Listed/Web/SymbolList?pageFieldName1=Code&pageFieldValue1=&pageFieldOperator1=eq&pageFieldName2=Sectors&pageFieldValue2=&pageFieldOperator2=&pageFieldName3=Sector&pageFieldValue3=00000000-0000-0000-0000-000000000000&pageFieldOperator3=&pageFieldName4=StartWith&pageFieldValue4=&pageFieldOperator4=&pageCriteriaLength=4&_search=false&nd=1725165564829&rows=10000&page=1&sidx=id&sord=desc"

def collect(sheet, headers):
    response = requests.get(url)
    
    if response.status_code == 200:
        for item in response.json()["rows"]:
            code = item.get("cell")[1]
            sheet.append(data.get(code, headers))
    else:
        print(f"Request failed with status code: {response.status_code}")
