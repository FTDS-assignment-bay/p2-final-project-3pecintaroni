# Deploy

import streamlit as st
import pandas as pd
import numpy as np
import pickle
# import datetime
from datetime import datetime, date
from sklearn.preprocessing import MinMaxScaler

#load the files!
with open('model_scaler.pkl', 'rb') as file_1 : 
    model_scaler = pickle.load(file_1)
with open('model_pca.pkl', 'rb') as file_2 : 
    model_pca = pickle.load(file_2)
with open('model_km.pkl', 'rb') as file_3 : 
    model_km = pickle.load(file_3)
    

data_clean = pd.read_csv('cobadeploy.csv')

minmax = MinMaxScaler()

kolom =['Miscellaneous',
 'Decorations',
 'Accessories',
 'Toys',
 'Stationery',
 'Electronics',
 'Clothing',
 'Furniture',
 'Kitchenware',
 'Candles']

data_clean[kolom] = minmax.fit_transform(data_clean[kolom])
data_clean.set_index('Customer_Level',inplace=True)

def get_top_3_categories(customer_level):
    if customer_level in data_clean.index:
        top_3 = data_clean.loc[customer_level].nlargest(3)
        return top_3.index.tolist()
    
# st.dataframe(data_clean)



def run():
    with st.form('Namanya apa'):
        st.title('## Judul')

        InvoiceNo = st.slider('Your Invoice Number?', min_value=0, max_value=50000, value=500, help='Enter your invoice number')
        StockCode = st.text_input('Stock Code?', value='5000', help='Enter your stock code')
        Desc = st.text_input("Enter the item Description:", value = 'WHITE HANGING HEART T-LIGHT HOLDER').upper()
        Quantity = st.number_input('How Mant Item?', min_value=0, max_value=8000000, value=2000000, help='Quantity Item')
        # Define the minimum date value
        min_date_value = date(2010, 1, 1)
        InvoiceDate = st.date_input("Invoice Date", value='default_value_today',format="MM.DD.YYYY",min_value=min_date_value,  help = 'Your Shopping Date')
        st.write("Your birthday is:", InvoiceDate)

        UnitPrice = st.number_input('Your Item Price?', min_value=0, max_value=500, value=20, help='Enter your item price')
        
        ID = st.slider('Your Item Price?', min_value=0, max_value=30000, value=18000, help='What is your customer ID')


        country = st.selectbox('Where are you from?', options=('United Kingdom', 'France', 'Australia', 'Netherlands', 'Germany',
       'Norway', 'EIRE', 'Switzerland', 'Spain', 'Poland', 'Portugal',
       'Italy', 'Belgium', 'Lithuania', 'Japan', 'Iceland',
       'Channel Islands', 'Denmark', 'Cyprus', 'Sweden', 'Austria',
       'Israel', 'Finland', 'Bahrain', 'Greece', 'Hong Kong', 'Singapore',
       'Lebanon', 'United Arab Emirates', 'Saudi Arabia',
       'Czech Republic', 'Canada', 'Unspecified', 'Brazil', 'USA',
       'European Community', 'Malta', 'RSA'),help='Choose the country you currently live in')

        df_new = {
            "InvoiceNo" : InvoiceNo,
            "StockCode" : StockCode,
            "Description" : Desc,
            "Quantity" : Quantity,
            "InvoiceDate" :InvoiceDate,
            "UnitPrice" :UnitPrice,
            "CustomerID" :ID,
            "Country" : country}
        
        df_new = pd.DataFrame([df_new])
        submit = st.form_submit_button('Submit Form')


        df_new["InvoiceDate"] = pd.to_datetime(df_new["InvoiceDate"], format="%m/%d/%Y %H:%M")

        #Calculating the TotalPrice per order (UnitPrice and Quantity)
        df_new["TotalPrice"] = df_new["Quantity"]*df_new["UnitPrice"]

        current = pd.Timestamp(datetime(2011, 11, 28))

        RFMScore = df_new.groupby('CustomerID').agg({'InvoiceDate': lambda x: (current - x.max()).days,
                                                    'InvoiceNo': lambda x: x.count(),
                                                    'TotalPrice': lambda x: x.sum()
                                                    })

        RFMScore.rename(columns={'InvoiceDate':'Recency','InvoiceNo':'Frequency','TotalPrice':'Monetary'},inplace = True)

        def RecencyScore(x):
            if x <= (-357.0):
                return 1
            elif x <= (-323.0):
                return 2
            elif x <= (-230.0):
                return 3
            else:
                return 4

        def FreqScore(x):
            if x <= 17.00:
                return 4
            elif x <= 41.00:
                return 3
            elif x <= 99.25:
                return 2
            else:
                return 1

        def MonetScore(x):
            if x <= 291.795:
                return 4
            elif x <= 644.070:
                return 3
            elif x <= 1608.335:
                return 2
            else:
                return 1

        # Define scoring functions
        def RecencyScore(x):
            if x <= -357.0:
                return 1
            elif x <= -323.0:
                return 2
            elif x <= -230.0:
                return 3
            else:
                return 4

        def FreqScore(x):
            if x <= 17.0:
                return 4
            elif x <= 41.0:
                return 3
            elif x <= 99.25:
                return 2
            else:
                return 1

        def MonetScore(x):
            if x <= 291.795:
                return 4
            elif x <= 644.070:
                return 3
            elif x <= 1608.335:
                return 2
            else:
                return 1

        # Applying the created function on the respective columns
        # '''
        # Recency_Score(x,p,d):
        # x = value
        # p = recency, monetary_value, frequency
        # d = quartiles dict
        # '''
        RFMScore['R'] = RFMScore['Recency'].apply(RecencyScore )
        RFMScore['F'] = RFMScore['Frequency'].apply(FreqScore  )
        RFMScore['M'] = RFMScore['Monetary'].apply(MonetScore)

        #Creating a new field 'RFMValue' to split the customers into 10 segments
        RFMScore['RFMValue'] = RFMScore[['R','F','M']].sum(axis = 1)
        RFMScore['RFMGroup'] = RFMScore.R.map(str) + RFMScore.F.map(str) + RFMScore.M.map(str)
        RFMScore['RFMGroup'] = RFMScore['RFMGroup'].astype(int)

        # melakukan scaling df_new
        RFMS_scaled = model_scaler.transform(RFMScore)
        RFMS_scaled = pd.DataFrame(RFMS_scaled, columns=RFMScore.columns)
        RFMS_scaled = RFMScore.drop(['RFMValue','RFMGroup'],axis=1)

        # menggunakan model PCA
        df_inf_pca = model_pca.transform(RFMS_scaled)   



        if submit:
            st.info('Your answers have been recorded.', icon="ℹ️")  

            if submit:
                st.dataframe(RFMScore)
                pred = model_km.predict(df_inf_pca)
                st.subheader("Prediction whether you need mental health care or not!")
                if pred == 0:
                    pred = 'Platinum'
                    st.write(f'Top 3 for {pred}: {get_top_3_categories("Platinum")}')
                elif pred == 1:
                    pred = 'Diamond'
                    st.write(f'Top 3 for {pred}: {get_top_3_categories("Diamond")}')
                elif pred == 2:
                    pred = 'Gold'
                    st.write(f'Top 3 for {pred}: {get_top_3_categories("Gold")}')
                elif pred == 3:
                    pred = 'Silver'
                    st.write(f'Top 3 for {pred}: {get_top_3_categories("Silver")}')
                else:
                    st.write('Customer level not found.')



if __name__ == '__main__':
    run()           

