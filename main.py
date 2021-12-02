import argparse
import logging
import datetime
import csv
from os import write
from requests.models import HTTPError
logging.basicConfig(level=logging.INFO)
import re
import news_page_objects as news

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from common import config

'''El modulo Logging lo que nos permite (en palabras abreviadas) es enviar mensajes por consola de manera
 automatica asignandole un nivel (level) de importancia a cada tipo de mensaje (existen DEBUG, INFO, WARNING,
  ERROR y CRITICAL. Cada uno equivale a un numero entero donde DEBUG es el mas bajo y CRITICAL es el mas alto). 
  Ya que tenemos la nocion del uso que le daremos a este modulo podemos hablar sobre la funcion basicConfig(). 
  Como su nombre lo indica, estamos dandole las configuraciones basicas o iniciales a esos mensajes que mandaremos por consola. 
  El keyword argument level=logging.INFO es solo el nivel para indicarle al logging que no muestre mensajes con nivel menor a INFO 
  (los unicos mensajes de mas bajo nivel que INFO son los de tipo DEBUG).


el metodo getLogger([module_name]) el cual retorna una instancia que nos servira para indicar que los mensajes estan siendo enviados 
desde este module name en particular. 
 
Podemos observarlo en el prompt que nos retorna al ejecutar el programa:
INFO:Beggining scraper for https://www.eluniversal.com.co
'''

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logger.info('Beggining scraper for {}'.format(host))
    logging.info('Finding links in homepage...')
    homepage = news.HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)
        #print(host + link)

        if article:
            logger.info('Artivle fetched')
            articles.append(article)
            #break
            #print(article.title)

    #print(len(articles))

    _save_articles(news_site_uid, articles)

def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid=news_site_uid,
        datetime = now)
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(out_file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(csv_headers)

def _fetch_article(news_site_uid, host, link):
    logger.info('Start fetching article at {}'.format(link))

    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article', exc_info=False)
        return None
    
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{url}'.format(host=host, url=link)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['news_sites'].keys())
    #print(news_site_choices)
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)
    #print(parser.parse_args())
    args = parser.parse_args()
    _news_scraper(args.news_site)