# Streamlit app for correlations


import pandas as pd
import dython
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

title = st.title('Automatic Correlations')

subheader = st.caption('2022 by Taylor Brooks - Datatorii')

caption1 = st.caption('This web app will automatically perform association analysis for categorical variables in your file. Future work will expand this to work with numerical data and mixed datatypes')

caption2 = st.caption('Please select the type of analysis you want on the left sidebar')

#sidebar
sidebartitle = st.sidebar.title('Statistic Options')
sidebarheader = st.sidebar.header('Categorical')
sidebar_radio = st.sidebar.radio('Choose Statistic', options = ('Uncertainty Coefficient','Cramérs V'))


uploaded_file = st.file_uploader('Upload the fact table file as a CSV (single files only)', type= ['csv'],accept_multiple_files=False)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    df_cat = pd.DataFrame(data = df.dtypes, columns = ['a']).reset_index()
    # just categorical variables 
    cat_vars = list(df_cat['index'].loc[df_cat['a'] == 'object'])

    df_cat = df[cat_vars]

    figdim = len(df_cat.columns)
    
    if sidebar_radio is not None:
        if sidebar_radio == 'Uncertainty Coefficient':  
            association = dython.nominal.associations(df_cat, nom_nom_assoc='theil', figsize=(figdim, figdim))

        if sidebar_radio == 'Cramérs V':  
            association = dython.nominal.associations(df_cat, nom_nom_assoc='cramer', figsize=(figdim, figdim))
    
    corr = association.get('corr')
    fig, ax = plt.subplots(figsize=(figdim,figdim)) 
    mask = np.zeros_like(corr)
    mask[np.where(corr == 0)[0],np.where(corr == 0)[1]] = True
    heatmap = sns.heatmap(corr, annot=True, cbar= True, ax=ax, mask=mask, cmap='coolwarm')
    heatmap.set_facecolor('#BCBCBC')
    fig = heatmap.get_figure()
    st.pyplot(fig)

