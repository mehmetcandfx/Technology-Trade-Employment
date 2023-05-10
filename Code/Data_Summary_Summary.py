import pandas as pd
import os
import eurostat

db=["EARN_SES_AGT14"]#,"EARN_SES06_14"]#,"EARN_SES10_14","EARN_SES14_14","EARN_SES18_14"]
pars=['age']

df=pd.DataFrame()

for ds in db:
    
    try:
        yyyy=2000+ int(ds[-5:-3])
    except:
        yyyy=2002

    for par in pars:
        print(type(par))    
        try:
            eurostat.get_dic(ds,par, full=False)
        except:
            pass
        else:
            dftemp = pd.DataFrame({
                'Dataset': [ds for i in eurostat.get_dic(ds,par, full=False)],
                'Year': [ yyyy for i in eurostat.get_dic(ds,par, full=False)], 
                'Category' : [par for i in eurostat.get_dic(ds,par, full=False)],
                'Descriptions': eurostat.get_dic(ds,par, full=False)
            })
            
            df = pd.concat([df, dftemp], ignore_index=True)
        

df.set_index(['Dataset','Year'])


