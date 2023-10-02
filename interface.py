import streamlit as st
import pandas as pd
import psycopg2 as p 
import pickle
import datetime
load_model=pickle.load(open('AQI_calc.pk1','rb'))
def get_personalized_recommendation(aqi_value="570", user_profile="", location="South Delhi"):
    aqi_value=int(aqi_value)
    recommendations = []

    thresholds = [
        (0, 50, "Good: No significant health risks; outdoor activities are safe."),
        (51, 100, "Moderate: Sensitive individuals should consider reducing prolonged outdoor exertion."),
        (101, 150, "Unhealthy for Sensitive Groups: Avoid prolonged outdoor exertion."),
        (151, 200, "Unhealthy: Avoid prolonged outdoor exertion for everyone."),
        (201, 300, "Very Unhealthy: Avoid outdoor activity."),
        (301, float('inf'), "Hazardous: Health alert! Stay indoors; avoid any outdoor activity.")
    ]


    for low, high, recommendation in thresholds:
        if low <= aqi_value & aqi_value<= high:
            recommendations.append(recommendation)
            break

        if user_profile == "asthma":
            recommendations.append("If you have asthma, use a mask or consider staying indoors.")
        elif user_profile == "elderly":
            recommendations.append("If you are elderly, avoid outdoor activities during poor air quality.")
        elif user_profile == "child":
            recommendations.append("For children, limit outdoor playtime during poor air quality.")
        elif user_profile == "heart_condition":
            recommendations.append("If you have a heart condition, reduce outdoor exertion.")
        elif user_profile == "pregnant":
            recommendations.append("If pregnant, avoid outdoor activities during poor air quality.")
        elif user_profile == "allergies":
            recommendations.append("If you have allergies, take allergy medication as needed during high pollen days.")
        elif user_profile == "immunocompromised":
            recommendations.append("If immunocompromised, take extra precautions during poor air quality.")
        elif user_profile == "athlete":
            recommendations.append("Athletes should adjust their outdoor training schedule based on AQI levels.")
        elif user_profile == "smoker":
            recommendations.append("If you are a smoker, consider quitting to protect your respiratory health.")
        elif user_profile == "diabetes":
            recommendations.append("Diabetics should monitor blood sugar closely during poor air quality.")
        elif user_profile == "elderly":
            recommendations.append("Elderly individuals should stay hydrated during hot and humid conditions.")
        elif user_profile == "obesity":
            recommendations.append("Obese individuals should manage their weight to reduce health risks.")  
            
        if location == "South Delhi":
            recommendations.append("In South Delhi, consider visiting parks with better air quality.")
        elif location == "Central Delhi":
            recommendations.append("In Central Delhi, use masks or stay indoors during high pollution days.")
        elif location == "East Delhi":
            recommendations.append("In East Delhi, avoid outdoor activities when AQI is high.")
        elif location == "North Delhi":
            recommendations.append("In North Delhi, use air purifiers indoors during poor air quality days.")
        elif location == "West Delhi":
            recommendations.append("In West Delhi, keep windows closed on high-pollution days.")
        elif location == "New Delhi":
            recommendations.append("In New Delhi, monitor air quality and take precautions accordingly.")
        elif location == "Noida":
            recommendations.append("In Noida, stay indoors when AQI levels are very high.")
        elif location == "Gurgaon":
            recommendations.append("In Gurgaon, use air purifiers to improve indoor air quality.")
        elif location == "Faridabad":
            recommendations.append("In Faridabad, limit outdoor activities during poor air quality days.")
        elif location == "Ghaziabad":
            recommendations.append("In Ghaziabad, avoid outdoor exercise when AQI is unhealthy.")
        elif location == "Dwarka":
            recommendations.append("In Dwarka, monitor local air quality for accurate recommendations.")
        elif location == "Lajpat Nagar":
            recommendations.append("In Lajpat Nagar, stay updated on local air quality conditions.")
        elif location == "Rohini":
            recommendations.append("In Rohini, follow local advisories during poor air quality days.")
        elif location == "Karol Bagh":
            recommendations.append("In Karol Bagh, use masks when AQI levels are high.")
        elif location == "Connaught Place":
            recommendations.append("In Connaught Place, choose indoor activities during poor air quality days.")
            
        return recommendations

# Create a dictionary to store user information (in-memory, not secure)
users ={}

# Page title
st.markdown("""
    <style>
        .centered-title {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="centered-title">AIR QUALITY INDEX</h1>', unsafe_allow_html=True)



# Create a container to hold the home page content
home_page_container = st.empty()


# Create a sidebar for navigation
page = st.sidebar.radio("Select a Page", ["Home", "AQI Prediction", "Indian Map and Live Sensors", "Previous AQI Data", "System Alerts", "Previous Environmental Conditions"])

# Define the content for each page
if page == "Home":
    home_page_container.header("Welcome to our website!")
    home_page_container.write("Please select a page from the sidebar.")
else:
    home_page_container.empty()  # Clear the home page content when navigating to other pages

if page == "AQI Prediction":
    today=datetime.datetime.today()
    user_input = st.date_input("Enter date: ")
    value=datetime.date(today.year,today.month,today.day)
    #dif=(value-today).days
    if user_input:
        st.header("AQI Prediction")
        pred=load_model.predict(n_periods=1,return_conf_int=True)
        forecast=pd.DataFrame(pred[0])
        st.write(forecast.iloc[0])
        
    
    
    # Add content for AQI Prediction here

elif page == "Indian Map and Live Sensors":
    st.header("Indian Map and Live Sensors")
    latitudes = [
    28.5284,  # South Delhi
    28.6139,  # Central Delhi (and New Delhi)
    28.6280,  # East Delhi
    28.7041,  # North Delhi
    28.6139,  # West Delhi
    28.5355,  # Noida
    28.4595,  # Gurgaon
    28.4089,  # Faridabad
    28.6692,  # Ghaziabad
    28.5656,  # Lajpat Nagar
    28.7181,  # Rohini
    28.6519,  # Karol Bagh
    28.6304   # Connaught Place
    ]

    longitudes = [
        77.2283,  # South Delhi
        77.2090,  # Central Delhi (and New Delhi)
        77.2850,  # East Delhi
        77.1025,  # North Delhi
        77.2090,  # West Delhi
        77.3910,  # Noida
        77.0266,  # Gurgaon
        77.3178,  # Faridabad
        77.4538,  # Ghaziabad
        77.2433,  # Lajpat Nagar
        77.1025,  # Rohini
        77.1890,  # Karol Bagh
        77.2177   # Connaught Place
    ]

    data = {
        "lat": latitudes,
        "lon": longitudes
}

    st.map(data)

elif page == "Previous AQI Data":
    st.header("Previous AQI Data")
    
    df = pd.read_csv(r"C:\Users\srikruthi neriyanuri\Desktop\PYTHON\dt.csv")

    @st.experimental_memo
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)

    st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )

elif page == "System Alerts":
    st.header("System Alerts")
    st.write(''' 🚨 System Alert: Important Notice 🚨
             
            Dear valued user,
            We apologize for the inconvenience, but our website is currently undergoing scheduled maintenance to 
            improve your experience.During this time, you may experience temporary unavailability of our system 
            updates / alerts. Rest assured, our team is working diligently to minimize any disruptions, and we 
            expect to be back up and running shortly.
            We appreciate your patience and understanding as we strive to provide you with a better and more reliable 
            service.
            Thank you for choosing Zenith.
            
            Best regards,
            The Zenith Team''')

elif page == "Previous Environmental Conditions":
    st.header("Recommendations")
    
    aqi_value = st.text_input("Entr AQI number: ")
    user_profile = st.text_input("Enter problem:(are u dead?)")
    location = st.text_input("entr location:")
    st.write(get_personalized_recommendation(aqi_value,user_profile,location))



    # Example usage
    aqi_value = 160  
    user_profile = "asthma" 
    user_location = "South Delhi"
    recommendations = get_personalized_recommendation(aqi_value, user_profile, user_location)

    for recommendation in recommendations:
        print(recommendation)
