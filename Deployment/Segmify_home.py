# import libraries

import streamlit as st


st.set_page_config(
    page_title= 'SEGMIFY',
    layout= 'wide',
    initial_sidebar_state='expanded'
)

def run():
    # create title
    st.title('Welcome to our website!')

    st.image('LOGO.png'
             ,caption='SEGMIFY')
    
    st.markdown('---')
    
    # add description
    container = st.container(border=True)
    container.write('Welcome to the Segmify E-Commerce Clustering and Recommendation System App!')
    container.write('Our app is dedicated to improving your shopping experience by offering personalized product recommendations according to your unique preferences. By utilizing advanced machine learning clustering techniques combined with RFM (Recency, Frequency, Monetary) methods, we accurately group customers into different segments based on their purchasing behavior.')
    container.write('Once you are placed into a particular cluster, our system will provide recommendations that match your needs and interests. This sophisticated approach ensures that you always find the best selection of products that suit your tastes.')
    container.write("Whether you're an avid shopper or exploring Segmify for the first time, our app serves as your personal shopping assistant, guiding you to find products you'll love. Enjoy a seamless and enjoyable shopping journey with us.")
    container.write('Welcome to Segmify, where we make shopping smarter, easier and more fun. Happy shopping!')

if __name__ == '__main__':
    run()