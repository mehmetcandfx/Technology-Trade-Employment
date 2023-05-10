# wages.py

import pandas as pd
import os
import eurostat


def cat_describer(db):
    
    try:
        yyyy=2000+ int(ds[-5:-3])
    except:
        yyyy=2000+ int(ds[-8:-6])
    
    df=pd.DataFrame()
    for ds in db:
        dftemp = pd.DataFrame({
            'Dataset': [ds for i in eurostat.get_pars(ds)],
            'Year': [ yyyy for i in eurostat.get_pars(ds)], 
            'Category' : eurostat.get_pars(ds),
            '#ofUniques': [len(eurostat.get_par_values(ds, i)) for i in  eurostat.get_pars(ds)],
            'Uniques': [eurostat.get_par_values(ds, i) for i in  eurostat.get_pars(ds)]
            })
        df = pd.concat([df, dftemp], ignore_index=True)
        
    df.set_index(['Dataset','Year'])
    return df
