
import pandas as pd
import requests
import streamlit as st

def get_data(num_rows: int =100) -> pd.DataFrame:
    url=f"https://bills-api.parliament.uk/api/v1/Bills?CurrentHouse=Commons&OriginatingHouse=Commons&IsDefeated=false&IsWithdrawn=false&SortOrder=DateUpdatedDescending&Take={num_rows}"

    # get data
    response = requests.get(url)

    if response.status_code == 200:
        # Get the JSON data from the response
        data = response.json()
        bills=[bill for bill in data['items']]
        df=pd.DataFrame(bills)

    else:
        print("an error occurred retrieving the data")

    # parse description field
    df['currentStage']=df['currentStage'].apply(lambda x: x['description'])

    return df

if __name__=="__main__":
    st.title("100 Last Bills downloader")
    st.markdown("Or enter a number of bills to fetch...")
    user_input = st.text_input("Number of bills to fetch")
    if user_input != '':
        df=get_data(int(user_input))
    else:
        df=get_data()
    # show data
    st.dataframe(df.head(5))
    # Add a button to download the DataFrame as CSV
    st.download_button(
        label='Download CSV',
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='current_bills.csv',
        mime='text/csv'
    )
    # Add a refresh button
    if st.button('Refresh'):
        df=get_data()

    st.markdown("Created by Maurits Westbroek")