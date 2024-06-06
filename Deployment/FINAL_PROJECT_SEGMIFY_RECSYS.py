import streamlit as st
import pandas as pd
import numpy as np
import re

# Config the page
st.set_page_config(
    page_title ='BukaOnline - Cluster and Recommendation System'
)

# Load data
data = pd.read_csv('data.csv', encoding='ISO-8859-1')

# Function to categorize descriptions
def categorize_description(description):
    if not isinstance(description, str):
        return 'Miscellaneous'
    
    categories = []
    
    # Define the category keywords
    category_keywords = {
        'Candles': ['candles'],
        'Decorations': ['decoration', 'ornament', 'garland','holder','flannel','platter','balloons'],
        'Kitchenware': ['mug', 'plate', 'bowl', 'jampot','cutlery','jars','tea','bottle','container','teacup','tissues','napkins','baking'],
        'Stationery': ['notebook', 'pen', 'pencil', 'paper','sticker','pen'],
        'Toys': ['toy', 'game', 'puzzle','block','children','dolly'],
        'Furniture': ['chair', 'table', 'sofa', 'stool'],
        'Clothing': ['shirt', 'dress', 'trousers', 'sock','woolly'],
        'Electronics': ['lamp', 'light', 'clock'],
        'Accessories': ['bag', 'scarf', 'belt','charm','rucksack','backpack','earrings'],
        'Miscellaneous': ['misc', 'various']
    }
    
    # Lowercase description for case insensitive matching
    description_lower = description.lower()
    
    # Check keywords and assign categories
    for category, keywords in category_keywords.items():
        if any(re.search(r'\b' + keyword + r'\b', description_lower) for keyword in keywords):
            categories.append(category)
        if len(categories) == 2:  # Maximum of 2 categories
            break
    
    if not categories:
        categories.append('Miscellaneous')
    
    return ' '.join(categories)

# Group the data and apply the categorization
df_grouped = data.groupby('Description').agg({
    'StockCode': 'first',
    'Quantity': 'sum',
    'InvoiceDate': 'first',
    'UnitPrice': 'mean',
    'CustomerID': 'first',
    'Country': 'first'
}).reset_index()

# Apply the function to the Description column to create the Category column
df_grouped['Category'] = df_grouped['Description'].apply(categorize_description)

# Filter out rows where UnitPrice is zero
df_grouped = df_grouped[df_grouped['UnitPrice'] != 0.000000]

# Generate binary matrix for category representation
categories = ' '.join(df_grouped['Category']).split(' ')
categories = list(set(categories))

gen_desc = [[] for _ in range(len(categories))]

for dat in df_grouped['Category']:
    for i, category in enumerate(categories):
        if category in dat.split(' '):
            gen_desc[i].append(1)
        else:
            gen_desc[i].append(0)

gen_mv_dat = pd.DataFrame(np.array(gen_desc).T, columns=categories)

title_df_grouped = df_grouped[['Description']].reset_index(drop=True)
df_grouped_vector = pd.concat([title_df_grouped, gen_mv_dat], axis=1)
df_grouped_vector.set_index('Description', inplace=True)

# Define the cosine similarity function
def cosine_sim(vect1, vect2):
    norm_1 = np.linalg.norm(vect1)
    norm_2 = np.linalg.norm(vect2)

    cos_sim = (vect1 @ vect2) / (norm_1 * norm_2)
    return cos_sim

# Define the recommendation system function
def recsys(description, top_N):
    cossim = pd.Series([cosine_sim(df_grouped_vector.loc[description], x) for x in df_grouped_vector.values], index=df_grouped_vector.index).drop(index=description)
    st.write(f'You like {description}, so based on our recommender system, we recommend you to see:')
    for i, mv in enumerate(cossim.sort_values(ascending=False)[:top_N].index):
        st.write(f'{i+1}. {mv}')
    return ''

def run():
    # Create title
    st.title('RECOMENDED SYSTEM')
    st.subheader('Used to recomend item that similar to what you search')
    st.markdown('---')
    
    # # Create form
    with st.form(key='Tweets Prediction'):
        st.write("## Description Text")
        # Text input
        text = st.text_input("Enter the item Description:").upper()
        submitted = st.form_submit_button('Predict')
        
        recomend = recsys(text,3)

        if submitted:
            st.write(recomend)
            st.balloons()
            

if __name__== '__main__':
    run()
    
