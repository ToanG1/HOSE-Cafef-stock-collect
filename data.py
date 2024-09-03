import requests
from bs4 import BeautifulSoup
from stockCode import find
import unidecode

def get(code, headers):
    data = [0] * len(headers)
    # Code
    data[0] = code
    serp = getSerpByCode(code)
    # Market Capitalization
    try:
        data[1] = getMarketCapitalization(serp)
    except:
        data[1] = 0
    # State Capital
    try:
        blockHoder = getBlockHolder(code)
    except:
        try:
            blockHoder = getBlockHolderBySerp(serp)
        except:
            blockHoder = ['-', '-']
    data[2] = blockHoder[0]
    data[3] = blockHoder[1]
        
    # Other
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

def getSerpByCode(code):
    baseUrl = 'https://s.cafef.vn/hose/'
    
    response = requests.get(baseUrl + getURL(code))
    if (response.status_code == 200):
        return BeautifulSoup(response.content, 'html.parser')
        
def getURL(code):
    name = find(code)

    lower_str = name.lower()

    normalized_str = unidecode.unidecode(lower_str).replace("&", '')

    hyphenated_str = normalized_str.replace(" ", "-").replace(" - ", "-").replace("-", "-")

    return f"{code.lower()}-{hyphenated_str}.chn"

            
def getMarketCapitalization(serp):
    elements = serp.find_all('div', attrs={'class': 'dltl-other'})
    for element in elements:
        li = element.find_all('li')
        if (len(li) < 3): continue
        label = li[3].find('b').text  
        if (label == 'Vốn hóa thị trường'): 
            return li[3].find('div', attrs={'class': 'r'}).text.strip()
        
def getBlockHolder(code):
    url = 'https://s.cafef.vn/Ajax/CongTy/BanLanhDao.aspx?sym='
    serp = BeautifulSoup(requests.get(url + code).content, 'html.parser')
    d_sh = serp.find(id='divViewCoDongLon')
    tr_elements = d_sh.find_all('tr')
    td_elements = tr_elements[4].find_all('td')
    return [td_elements[0].text.strip(), td_elements[2].text.strip() + '%']

def getBlockHolderBySerp(serp):
    d_sh = serp.find(id='dvSH')
    tr_elements = d_sh.find_all('tr')
    td_elements = tr_elements[1].find_all('td')
    return [td_elements[0].text.strip(), td_elements[1].text.strip()]
