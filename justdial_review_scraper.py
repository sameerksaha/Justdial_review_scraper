from bs4 import BeautifulSoup
import requests, lxml


def get_name(body):
    return body.find("span", {'class': 'rName'})


def get_body(body):
    return body.find('div', {"class": 'vew_opn'})


def rating(body):
    count = 0
    text = body.find_all('span', {'class': 'ms10'})
    for i in text:
        if 'ms10' in str(i):
            count = count + 1
    return count


def get_date(body):
    return body.find('span', {'class': "dtyr ratx pull-right"})

u = "https://www.justdial.com/Delhi/S-K-Premium-Par-Hari-Nagar/011PXX11-XX11-131128122154-B8G6_BZDET"
page_number = 1
while True:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"})

    if '?' in u:
        url = u.replace(u[u.index('?'):], '') + '/reviews/page-' + str(page_number)
    else:
        url = u + '/reviews/page-' + str(page_number)
    # paste the link here before -%s
    response = session.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    service = soup.find_all("div", {'class': "allratR"})
    try:
        if page_number > int(soup.find('span', {'class': "act"}).text):
            break
    except AttributeError:
        break
    img_soup = soup.find_all("img", {'id': 'rwimg0'})
    for service_html in range(len(service)):
        name = get_name(service[service_html])
        print(f'Name- {name.text}')
        body_text = get_body(service[service_html])
        print(f'Review Body- {body_text.text}')
        rating_star = rating(service[service_html])
        print(f"Rating- {rating_star}")
        date = get_date(service[service_html])
        print(f'Post Date- {date.text}')
        img_link = img_soup[0].get('src')
        print(f"Profile Image- {img_link}")
        print()

        
    page_number = page_number + 1
