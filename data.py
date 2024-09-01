import requests
from bs4 import BeautifulSoup


def get(code, headers):
    data = [0] * len(headers)
    data[0] = code
    
    url = "https://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol="+ code + "&Type=2&PageIndex=0&PageSize=4"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tr_elements = soup.find_all('tr')

        for tr in tr_elements:
            tr_id = tr.get('id')
            if (tr_id and 
                (tr_id.startswith('rptNhomChiTieu_rptData_0_TrData_')
                 or tr_id.startswith('rptNhomChiTieu_rptData_1_TrData_'))):
                
                td_elements = tr.find_all('td')
                if (td_elements[0].text not in headers):
                    headers.append(td_elements[0].text)
                    data = data + [0]
                data[headers.index(td_elements[0].text)] = td_elements[4].text
        
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data