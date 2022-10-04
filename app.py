from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data#panel', headers={'User-Agent':'Popular browser\'s user-agent',})
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
table.find_all('th', attrs={'class':'font-semibold text-center'})[:5]

row = table.find_all('th', attrs={'class':'font-semibold text-center'})
row_length = len(row)


temp = [] #initiating a list 
temp = []

for i in range(1, row_length):

    Date = table.find_all('th', attrs={'class':'font-semibold text-center'})[i].text
        
    Volume = table.find_all('td', attrs={'class':'text-center'})[i].text
    Volume = Volume.strip()   

    temp.append((Date, Volume))
    
temp 

date = []
market_cap = []
volume = []
open = []
close = []

for i in range(0, row_length):
    Date = table.find_all('th', attrs={'class':'font-semibold text-center'})[i].text
    date.append(Date)

for j in range(0, row_length2,4):
    MC = table.find_all('td', attrs={'class':'text-center'})[j].text
    MC = Market_Cap.strip()
    market_cap.append(MC)
    
for j in range(1, row_length2,4):
    vol = table.find_all('td', attrs={'class':'text-center'})[j].text
    vol = volumee.strip()
    volume.append(vol)
    
for j in range(2, row_length2,4):
    Opn = table.find_all('td', attrs={'class':'text-center'})[j].text
    Opn = Openn.strip()
    open.append(Opn)
    
for j in range(3, row_length2,4):
    cls = table.find_all('td', attrs={'class':'text-center'})[j].text
    cls = Openn.strip()
    close.append(cls)

#change into dataframe

import pandas as pd

df = pd.DataFrame(temp, columns = ('Date','Volume'))
df.head()

#insert data wrangling here

import pandas as pd

df = pd.DataFrame({
    columns[0] : date,
    columns[2] : volume,
})

df['Date']=df['Date'].astype('datetime64[ns]')

def delete_dollar(x):
 for i in x:
        xx = i.split('$')
        return int(xx[1].replace(',',''))

def delete_dollar_2(x):
  for i in x:
        if i == 'N/A':
           return 'N/A'
        else:
         xx = i.split('$')
         return float(xx[1].replace(',',''))

df['Volume'] = df[['Volume']].apply(delete_dollar,axis=1)
        
        

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)