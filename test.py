import pandas as pd
url = 'https://www.google.com/finance/historical'
params = {'q': 'ASX:BBG'}
r = requests.get(url=url, params=params)

pd.read_html(r.content)[2]

