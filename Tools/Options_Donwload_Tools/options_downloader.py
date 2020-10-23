import sys

try:
    import requests
except ImportError:
    import pip 
    pip.main(['install', 'requests'])
    import requests

try:
    import json
except ImportError:
    import pip 
    pip.main(['install', 'json'])
    import json

try:
    import pandas as pd
except ImportError:
    import pip 
    pip.main(['install', 'pandas'])
    import pandas as pd

date=sys.argv[2]
symbol = sys.argv[1]
timestamp = pd.to_datetime([date+' 00:00:00']).astype(int)[0]//1000000000


url = "https://rapidapi.p.rapidapi.com/stock/v2/get-options"


querystring = {"symbol":symbol,"date":timestamp,"region":"US"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "0da8e9b784msh9001cc4bfc4e7e7p1c6d94jsna54c1aa52dbf"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

res = response.text
res = json.loads(res)

cols=['contractSymbol','currency', 'impliedVolatility', 'expiration', 'change',  'strike', 'contractSize', 'lastPrice', 'inTheMoney', 'openInterest', 'percentChange', 'ask', 'bid','volume', 'lastTradeDate', ]


if(len(res['contracts']['calls'])>1):
	calls=[]
	for i in range(len(res['contracts']['calls'])):
	    calls.append([res['contracts']['calls'][i]["contractSymbol"],\
	    res['contracts']['calls'][i]["currency"],\
	    res['contracts']['calls'][i]["impliedVolatility"]["fmt"],\
	    res['contracts']['calls'][i]["expiration"]["fmt"],\
	    res['contracts']['calls'][i]["change"]["fmt"],\
	    res['contracts']['calls'][i]["strike"]["fmt"],\
	    res['contracts']['calls'][i]["contractSize"],\
	    res['contracts']['calls'][i]["lastPrice"]["fmt"],\
	    res['contracts']['calls'][i]["inTheMoney"],\
	    res['contracts']['calls'][i]["openInterest"]["fmt"],\
	    res['contracts']['calls'][i]["percentChange"]["fmt"],\
	    res['contracts']['calls'][i]["ask"]["fmt"],\
	    res['contracts']['calls'][i]["bid"]["fmt"],\
	    res['contracts']['calls'][i]["volume"]["fmt"],\
	    res['contracts']['calls'][i]["lastTradeDate"]["fmt"]])

	puts=[]
	for i in range(len(res['contracts']['puts'])):
	    puts.append([res['contracts']['puts'][i]["contractSymbol"],\
	    res['contracts']['puts'][i]["currency"],\
	    res['contracts']['puts'][i]["impliedVolatility"]["fmt"],\
	    res['contracts']['puts'][i]["expiration"]["fmt"],\
	    res['contracts']['puts'][i]["change"]["fmt"],\
	    res['contracts']['puts'][i]["strike"]["fmt"],\
	    res['contracts']['puts'][i]["contractSize"],\
	    res['contracts']['puts'][i]["lastPrice"]["fmt"],\
	    res['contracts']['puts'][i]["inTheMoney"],\
	    res['contracts']['puts'][i]["openInterest"]["fmt"],\
	    res['contracts']['puts'][i]["percentChange"]["fmt"],\
	    res['contracts']['puts'][i]["ask"]["fmt"],\
	    res['contracts']['puts'][i]["bid"]["fmt"],\
	    res['contracts']['puts'][i]["volume"]["fmt"],\
	    res['contracts']['puts'][i]["lastTradeDate"]["fmt"]])

	df = pd.DataFrame(calls,columns=cols)
	df.to_csv(symbol+"_"+date+"_calls.csv",index=False)

	df = pd.DataFrame(puts,columns=cols)
	df.to_csv(symbol+"_"+date+"_puts.csv",index=False)
else:
	print("Failed to download files.")