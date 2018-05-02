import pandas as pd
import numpy as np

def tsv_to_dataframe(file_tsv):
    '''
    this function transforms Eurostat tsv file in pandas dataframe
    file_tsv: file name. It's work with tsv and compressed file "tsv.gz"
    '''
    
    def clean_cells(x):
        '''This function transforms Eurostat Missing Values ": " in numpy missing values.
        Then clean Eurostat annotation "b, u, .."'''
        try:
            return float(x)
        except:
            try:
                return float(x.split(" ")[0])
            except:
                return np.nan
    # open the Eurostat TSV file 

    data = pd.read_csv(file_tsv, sep="\t")

    
    
    
    # Create a dataframe for values data
    data_clean = data
    # Clean data values with clean_cells function
    data_clean = data_clean.applymap(lambda x: clean_cells(x))
    # Drop column with variable name like "age,isced11,unit,sex,geo\time". It is the first column. we have a 
    # dataframe with only data values 
    data_clean.drop(data_clean.columns[0], axis = 1, inplace = True)
    # transform column with variable in multiple-columns  
    variabili = data[data.columns[0]].apply(lambda x: pd.Series(x.split(",")))
    variabili.columns = data.columns[0].split(",")
    # return cleaned dataframe in pandas dataframe
    return pd.concat([variabili, data_clean], axis = 1)



#example 
if __name__ == "__main__":
    import urllib.request
    import gzip

    eurostat_link = "http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/AppLinkServices?lang=en&appId=bulkdownload&appUrl=http%3A%2F%2Fec.europa.eu%2Feurostat%2Festat-navtree-portlet-prod%2FBulkDownloadListing%3Ffile%3Ddata%2Frd_e_gerdtot.tsv.gz"
    urllib.request.urlretrieve(eurostat_link , "file.tsv.gz")
    result = tsv_to_dataframe("file.tsv.gz")
    result



