# utilities.py

import pandas as pd
import os
import utilities as u
import eurostat

def plustwo(n):
    out = n + 2
    return out


def falldist(t,g=9.81):
    d = 0.5 * g * t**2
    return d

def wageget(db):
    df=pd.DataFrame()
    for ds in db:
        dftemp = pd.DataFrame({
            'Dataset': [ds for i in eurostat.get_pars(ds)],
            'Year': [ 2000+int(ds[-5:-3]) for i in eurostat.get_pars(ds)], 
            'Category' : eurostat.get_pars(ds),
            '#ofUniques': [len(eurostat.get_par_values(ds, i)) for i in  eurostat.get_pars(ds)],
            'Uniques': [eurostat.get_par_values(ds, i) for i in  eurostat.get_pars(ds)]
            })
        df = pd.concat([df, dftemp], ignore_index=True)
    
    return df
