import requests
import bs4

#url = "https://www.elpais.com/america"
url = "https://elpais.com/internacional/2021-11-30/emma-coronel-esposa-de-el-chapo-guzman-condenada-a-tres-anos-de-carcel.html"

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text, 'html.parser')
news = soup.select('h2 > a')
article = soup.select('h1')
body = soup.select('p')

#print(url+news[0]['href'])
print(body)

#print(news[0].text)

#for item in news:
   #print(f"Noticia:{item.text} | Link: {url}{item['href']}")