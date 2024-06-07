import home, PROJECT_SEGMIFY_DEPLOY_PRED_REC, PROJECT_SIGMIFY_RECSYS
import streamlit as st


navigation = st.sidebar.selectbox('Navigation',['Home Page','Clustering customer and Recommend category','Recommendation System Item'])

st.sidebar.markdown('# About Aplication')
st.sidebar.write("Segmify is an application that groups customers based on their shopping behavior, including purchase frequency, spending amount, and recency of purchases. It uses the RFM method to facilitate segment classification, making it easier to classify segments and periodically recommend the top 3 best products based on member level.")

if navigation == 'Clustering customer and Recommend category':
    PROJECT_SEGMIFY_DEPLOY_PRED_REC.run()
elif navigation == 'Recommendation System Item':
    PROJECT_SIGMIFY_RECSYS.run()
else:
    home.run()
