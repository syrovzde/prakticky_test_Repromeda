import pandas as pd
from scipy.stats import chi2_contingency



def stat_test_summary(p_value:float,alpha:float=0.05)->str:
    if p_value < alpha:
        return "Null hypothesis stating indepence of groups is rejected with p-value of {p}".format(p=round(p_value, 3))
    return "Null hypothesis stating indepence of groups cannot be rejected with p-value of {p}".format(p=round(p_value, 3))

def create_table(df:pd.DataFrame,column_a:str,column_b:str,result_column:str,labels:list,bins:list):
    pd.options.mode.copy_on_write = True
    df=df.dropna(subset=[column_a,column_b])
    df.loc[:,column_a] = pd.to_numeric(df[column_a], errors='coerce')
    df.loc[:,result_column]=pd.cut(df[column_a],bins=bins,right=True,labels=labels)
    ret=df.groupby(result_column,observed=False).agg({column_b: 'mean'})
    ret.loc[:,result_column] = labels
    ret.loc[:,column_b] = 100*ret[column_b]
    return df,ret


def chisquare_test(df:pd.DataFrame,first_series_name:str,second_series_name:str) -> float:
    observed_data = pd.crosstab(df[first_series_name], df[second_series_name])
    _, p_value,_,_ = chi2_contingency(observed_data)
    return p_value

