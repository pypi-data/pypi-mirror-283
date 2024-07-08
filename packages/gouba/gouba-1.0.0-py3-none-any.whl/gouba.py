#By python_fucker On 2024/7/7
import mechanicalsoup
import sys
def woof(keyword=None):
  if len(sys.argv)>1:
   keyword=" ".join(sys.argv[1:])
  if not keyword:
    return {"error": "Not Have Keyword:)"}
  browser = mechanicalsoup.StatefulBrowser()
  browser.session.headers.update({'User-Agent': 'Mozilla/5.0 '})
  response = browser.open("https://sogou.com/")
  search_form = browser.select_form('#sf') 
  search_form['query'] = keyword 
  browser.submit_selected()  
  page = browser.get_current_page()
  urls = page.find_all('div', class_='r-sech')
  texts = page.find_all('h3', class_='vr-title')
  r=[]
  for url,text in zip(urls,texts):
    a = text.find('a')
    if a:
      title = a.text.strip()
      link = url.get('data-url')
      if link is not None:
       r.append({"title":title,"link":link})
  return r