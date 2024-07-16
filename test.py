import shopping as shop
import pandas as pd

'''NextPurchase = pd.read_excel('./tacomia.xlsx',sheet_name='Sheet1',header=0)

NextPurchase.sort_values(by='Priority',inplace=True,ascending=True,ignore_index=True)

print(NextPurchase)'''

shop.purchaseUpgrades(0.5)
