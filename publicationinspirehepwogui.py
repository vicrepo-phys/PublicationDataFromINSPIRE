# -*- coding: utf-8 -*-
"""PublicationInspireHepWoGUI.ipynb

# This is the latest version of Publication info crawlled from INSPIRE Website, We are also writing the publication information a file named "PublicationInfo.txt".
Date: 8 June, 2023 , Victor Roy, NISER.
"""

import pandas as pd
import urllib.request, json
import requests

# Open the INSPIRE-HEP profile
#inspirehep_profile = 'https://inspirehep.net/api/literature?sort=mostrecent&size=1000&q=a%20' + BAI
# Ask the user for AuthorIdentifier input
user_input = input("Enter the AuthorIdentifier (Press Enter to use the default value): ")

# Check if user provided an input
if user_input:
    AuthorIdentifier = user_input
else:
    AuthorIdentifier = 'V.Roy.2'

inspirehep_profile = 'https://inspirehep.net/api/literature?sort=mostrecent&size=1000&q=a%20' + AuthorIdentifier



# What needs to be printed ?
options={"PSno":"yes",
         "PTitle": "yes",
         "PAuthorList": "yes",
         "Pjournal": "yes",
         "PAbstract":"no",
         "Pcitation":"yes"}

print(options)
print(AuthorIdentifier)

# Load the data
json_text = requests.get(inspirehep_profile).json()
layer1=json_text['hits'] # this is a dictionary
#type(layer1)
layer2=layer1['hits'] # this is a list

#type(layer2)

# Here we arrive at the individual publication data
layer3=[]
for text in layer2:
    layer3.append(text)
    #print(text)

type(layer3[1])

# Number of listed publications in INSPIRES HEP
npub=len(layer3)

from datetime import date

today = date.today()

print('We found total ', npub, ' publications in INSPIRE database as on', today)

# Original Working
import pandas as pd

df_data = []
countJ=0
f=open("PublicationInfo.txt","w")
for i in range(npub):
    # Accessing all keys of the dictionary
    #print(layer3[i].keys())
    idData=layer3[i]['id']
    updatStat=layer3[i]['updated']
    #print(updatStat)
    metadata_l=layer3[i]['metadata']  # Dictionary
    # metadata_l contains all the relevant information
    """ with the following keys:  dict_keys(['citation_count_without_self_citations',
    'citation_count', 'authors', 'publication_info', 'citeable', '$schema', 'keywords',
    'references', 'number_of_pages', 'referenced_authors_bais', 'inspire_categories',
    'author_count', 'first_author', 'control_number', 'dois', 'earliest_date',
    'document_type', 'texkeys', 'abstracts', 'refereed', 'titles', 'facet_author_name',
    'core', 'imprints', 'curated', 'journal_title_variants'])
    """
    #print(metadata_l.keys())
    titles_l=metadata_l['titles']
    authors_l= metadata_l['authors']
    cCountD=metadata_l['citation_count']
    #pubInfo=metadata_l['publication_info'][0] # this is a Dictionary
    #print(pubInfo.keys())
    """
    dict_keys(['journal_volume', 'page_end', 'conference_record', 'year', 'parent_isbn',
    'journal_record', 'page_start', 'journal_title', 'cnum'])
    """


    titleP= metadata_l['titles'][0]['title']
    if options["PSno"]=="yes":
      print(str(i+1)+")",titleP)
      f.write("["+str(i+1)+"]")
      f.write(titleP+'\n')
    else:
      if options["PTitle"]=="yes":
        print(titleP)
        f.write(titleP+'\n')

    #pdf.cell(w=10, h = 0, txt = titleP, border = 0, ln = 0,
          #align = '', fill = False, link = '')
    #imprintD=metadata_l['imprints']
    #coreD=metadata_l['core']
    #print('core',coreD)

    # Number of co-authors
    nauth=metadata_l['author_count']
    authors = []
    for author in layer3[i]['metadata']['authors']:
      try:
        fname = author['first_name']
      except Exception:
        fname = ''
      try:
        lname = author['last_name']
      except Exception:
        lname = ''
      authors.append(' '.join([fname,lname]) )
       # Now setting critiria that if number of co-authors exceed 10 then put et.al.
      if len(authors)<10:
        auth = ', '.join(authors)
      else:
        auth = authors[:8]
        auth.append(' et al.')
        auth = ', '.join(auth)
    if options["PAuthorList"]=="yes":
      print(auth)
      f.write(auth + '\n')
    if 'refereed' in metadata_l:
      countJ=countJ+1
      pubInfo=metadata_l['publication_info'][0]
      #print(pubInfo)
      page_start = pubInfo.get('page_start', '')
      page_end = pubInfo.get('page_end', '')
      articleId= pubInfo.get('artid', '')
      if options["Pjournal"]=="yes":
        if page_start and page_end:
          print('Published in', pubInfo['journal_title']+' '+pubInfo['journal_volume']
            +',',page_start,'-',page_end,',', pubInfo['year'],'.' )
        elif page_start:
          print('Published in', pubInfo['journal_title']+' '+pubInfo['journal_volume']
            +',',page_start,',', pubInfo['year'],'.' )
        elif articleId:
          print('Published in', pubInfo['journal_title']+' '+pubInfo['journal_volume']
            +',',articleId,',', pubInfo['year'],'.' )


        f.write("{},{},{},{}\n".format('Published in', pubInfo['journal_title']+' '+pubInfo['journal_volume']
            +',',pubInfo['year'],'.' ))
      if options["PAbstract"]=="yes":
        print('ABSTRACT')
        print(metadata_l['abstracts'][0]['value'])
        f.write('ABSTRACT\n')
        f.write(metadata_l['abstracts'][0]['value']+'\n')

      if options["Pcitation"]=="yes":
        print("Total citation count:  ",cCountD)
        f.write("{}{}\n".format('Total citation count:',cCountD))

      page_start = pubInfo.get('page_start', '')
      page_end = pubInfo.get('page_end', '')
      if articleId:
        pagess=articleId
      else:
        pagess=page_start+'-'+page_end



      # Store the data in a dictionary for use as a dataframe
      df_data.append({
        'S No.':countJ,
        'Title': titleP,
        'Authors': auth,
        'Journal': pubInfo['journal_title'] if options["Pjournal"] == "yes" else '',
        'Volume': pubInfo['journal_volume'] if options["Pjournal"] == "yes" else '',
        'Pages': pagess,
        'Year': pubInfo['year'] if options["Pjournal"] == "yes" else '',
        'Abstract': metadata_l['abstracts'][0]['value'] if options["PAbstract"] == "yes" else '',
        'Citation Count': cCountD if options["Pcitation"] == "yes" else ''
        })





    #print('Total citation:', cCountD)
    print('─' * 55)
    f.write('─' * 55 + '\n')

df = pd.DataFrame(df_data)
print('We found total ', npub, ' publications in INSPIRE database as on', today)
print('Out of which', countJ, ' paper(s) is(are) published in peer reviewed journals')
f.close()

"""### Now we try to generate out put in tabular format so that it could be readily copied to google doc, I followed chatgpt's suggestion here."""

outputFile="Publication"+AuthorIdentifier+".xlsx"
df.to_excel(outputFile)
#df.to_excel("Publications.xlsx")
