import requests
import os
#import smtplib

with open('/home/pdg/arxiv_rss/.env','r') as fil:
    api_key = fil.read().strip()

#print(api_key)

# valid archive names are astro-ph, cond-mat, cs, econ, eess, gr-qc, hep-ex, hep-lat, hep-ph, hep-th, math, math-ph, nlin, nucl-ex, nucl-th, physics, q-bio, q-fin, quant-ph, stat

which_feed = "astro-ph"

r = requests.get('https://export.arxiv.org/rss/' + which_feed)
rss_as_rdf = r.text
rss_as_dict = xmltodict.parse(rss_as_rdf)

str_to_send = "search of arxiv RSS feed: \n\n"

for entry_dict in rss_as_dict['rdf:RDF']['item']:

    if (('keyword1'  in entry_dict['title'].lower()) and
        ('keyword2' in entry_dict['title'].lower())):
        str_to_send += ('found match for '+'keyword1 keyword2'+' in title for ' + entry_dict['link'] + "\n")

    if (('keyword1' in entry_dict['description']['#text'].lower()) and
        ('keyword2' in entry_dict['description']['#text'].lower())):
        str_to_send += ('found match for '+'keyword1 keyword2'+' in abstract for ' + entry_dict['link'] + "\n")

    list_of_authors = entry_dict['dc:creator'].replace('a>, <a','a>\n<a').split('\n')
    for author_url in list_of_authors:
        for name_tuple in [('firstname','lastname'),
                           ('anotherfirst','anotherlast')]:
            if (name_tuple[0] in author_url) and (name_tuple[1] in author_url):
                str_to_send += ('found '+name_tuple[0]+' '+name_tuple[1]+' as author for ' + entry_dict['link'] + "\n")

headers = {
#    'Authorization': 'Bearer ' + os.environ.get('SENDGRID_API_KEY'),
  'Authorization': 'Bearer ' + api_key,
  'Content-Type': 'application/json',
}
#print(headers)

if len(str_to_send)<30:
    str_to_send = "no matches to existing filters for today"
    subject = "no matches to report on "
else:
    subject = "keyword match for arxiv "+which_feed+" on "

data_dict = {"personalizations":
               [{"to": [{"email": "email1@gmail.com"}, #}]}], 
                        {"email": "email2@your.edu"}]}],
               "from": {"email": "email1@gmail.com"},
               "subject": subject + str(datetime.date.today()),
               "content": [{"type": "text/plain", "value": str_to_send}]}
# send the Email as a POST 
response = requests.post('https://api.sendgrid.com/v3/mail/send',
                         headers=headers,
                         data=json.dumps(data_dict))
# if the POST to Sendmail is successful, nothing is produced
if len(response.text)>0:
    print(response.text)
