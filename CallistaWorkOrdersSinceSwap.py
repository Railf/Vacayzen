import streamlit as st
import pandas as pd
import numpy as np

wo   = pd.read_csv('/Users/workhorse/Downloads/wo.csv')
swap = pd.read_csv('/Users/workhorse/Downloads/swap.csv')

wo                   = wo.dropna()
wo['DATE SUBMITTED'] = pd.to_datetime(wo['DATE SUBMITTED'])
swap['SWAPPED']      = pd.to_datetime(swap['SWAPPED'])

result = pd.DataFrame()

def GetWorkOrdersForUnitAfterDate(row):
    global result
    wos = wo[
        (wo['PROPERTY ID'] == row['CODE']) &
        (wo['DATE SUBMITTED'] > row['SWAPPED']) &
        (wo['STATUS'] == 'COMPLETED')
        ]
    result = pd.concat([result,wos])

swap.apply(lambda row: GetWorkOrdersForUnitAfterDate(row), axis=1)

result = result.drop('DESCRIPTION', axis=1)
st.write(result)
st.download_button('Download Result',result.to_csv(index=False),'result.csv',use_container_width=True)