import streamlit as st
import pandas as pd
import pickle

#load the model and data
@st.cache_resource
def load_data():
    frequent_itemsets = pd.read_pickle('frequent_itemsets.pkl')
    rules = pd.read_pickle('rules.pkl')
    items = pd.read_pickle('items.pkl')
    return frequent_itemsets, rules, items

frequent_itemsets, rules, items = load_data()

#function to get recommendations based on selected items
def get_recommendations(selected_items, rules):
    recommendations = set()
    for item in selected_items:
        rules_containing_item = rules[rules['antecedents'].apply(lambda x : item in x)]
        for _, row in rules_containing_item.iterrows():
            recommendations.update(row['consequents'])
    return recommendations - set(selected_items)

#streamlit app
st.title("Item Recommendation System")

#dropdown for item selection
selected_items = st.multiselect('Select items:', items)

#display recomendations:
if selected_items:
    recommendations = get_recommendations(selected_items, rules)
    if recommendations:
        st.write(f"Recommended items: {', '.join(recommendations)}")
    else:
        st.write("No recommendations available.")