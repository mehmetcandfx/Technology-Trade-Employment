import pandas as pd
import os
import eurostat

db=["EARN_SES_AGT14","EARN_SES06_14"]#,"EARN_SES10_14","EARN_SES14_14","EARN_SES18_14"]



df=pd.DataFrame()
for ds in db:

    print(ds[-5:-2])
    if ds[-5:-2] == "AGT": 
        yyyy=2000+ int(ds[-8:-6])
    else:
        yyyy=2000+ int(ds[-5:-3])

    dftemp = pd.DataFrame({
        'Dataset': [ds for i in eurostat.get_pars(ds)],
        'Year': [ yyyy for i in eurostat.get_pars(ds)], 
        'Category' : eurostat.get_pars(ds),
        '#ofUniques': [len(eurostat.get_par_values(ds, i)) for i in  eurostat.get_pars(ds)],
        'Uniques': [eurostat.get_par_values(ds, i) for i in  eurostat.get_pars(ds)]
        })
    df = pd.concat([df, dftemp], ignore_index=True)
    

print(df)

