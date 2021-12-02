import bs4
import requests

response = requests.get('https://www.pira.com.co')
soup = bs4.BeautifulSoup(response.text, 'html.parser')

response2 = requests.get('https://www.platzi.com')
soup2 = bs4.BeautifulSoup(response2.text, 'html.parser')

print(soup.title.text)

#soup nos regresa listas 

#links de Pira

links_pag = soup.select('.dslc-button')

links = [course.a['href'] for course in links_pag]

for i in links:
    print(i)

#links de platzi

school_links = soup2.select('.SchoolsList-school')

#primer texto dentro de href
print(school_links[0]['href'])

#todos los elementos dentro de href
schools = [school['href'] for school in school_links]

for school in schools:
    print(school)