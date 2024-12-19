import streamlit as st
import requests

# Azure Function URL (replace with your actual function URL)
azure_function_url = "https://p10recommandations.azurewebsites.net/api/recommandationv5?code=1w8titnAB6QvVSd9JU6oEBKCkmV6lm4bBdmIMWN10HtpAzFuzhsq4g%3D%3D"
                      
# Streamlit UI
st.title("Send user_id to Azure Function")
user_id = st.selectbox("Select a User ID:", [5, 8, 10, 11, 12])
print(user_id)
if st.button("Send"):
    if user_id:
        # Send a request to the Azure Function
        try:
            response = requests.get(azure_function_url, params={"user_id": user_id})
            if response.status_code == 200:
                result = response.json()
                st.success("Response received from Azure Function:")
                st.json(result)
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a User ID before sending.")