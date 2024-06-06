import streamlit as st

import FINAL_PROJECT_SEGMIFY_DEPLOY_PRED_CLUSTER_REC
import FINAL_PROJECT_SEGMIFY_RECSYS 

navigation = st.sidebar.selectbox("Select Page", 
                                  options=['Cluster Prediction', 'Recommended System'])
st.sidebar.write('# About')
st.sidebar.write('''
Segmify is an application that segments purchases using the RFM method to facilitate segment classification. 
It simplifies the process of classifying segments and periodically recommends the top 3 best products based on member level.


Halaman tersebut dibagi menjadi dua yaitu : 
- Cluster Prediction
- Recommended System
                 ''')


if navigation == 'Prediction Cluster':
    FINAL_PROJECT_SEGMIFY_DEPLOY_PRED_CLUSTER_REC.run()
else:
    FINAL_PROJECT_SEGMIFY_RECSYS.run()