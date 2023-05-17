library(dplyr)
library(haven)

OWW3 <- read_dta('/Users/memoc/Downloads/oww3.dta')
class(OWW3)
dim(OWW3)
head(OWW3)
typeof(OWW3)

dataNl <- filter(select(OWW3,y0,y1,country_code,country_name,y3,isic88,y4,isco88), 
                  country_code == "NLD" 
                  )#&y0>1990)

unique(dataNl$y0)

newdata <- summarize(dataNl)

