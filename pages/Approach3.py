import streamlit as st
import pandas as pd
import plotly.express as px
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.title("Third approach")

st.header("1. Data Pre-processing steps:")

st.subheader("Importing the raw csv files of our datasets (after finding some other significant datasets):")
code = '''crime_dataset = pd.read_csv("./datasets folder/dstrIPC_1.csv")
census_dataset = pd.read_csv("./datasets folder/census data.csv")
gdp_dataset = pd.read_csv("./datasets folder/INDIA_STATE_WISE_GDP_2001_2011.csv")
education_dataset = pd.read_csv("./datasets folder/Educational_standard_of_inmates.csv")
literacy_dataset = pd.read_csv("./datasets folder/LITERACY_RATE.csv")'''
st.code(code, language = "python")
crime_dataset = pd.read_csv("./datasets folder/dstrIPC_1.csv")
census_dataset = pd.read_csv("./datasets folder/census data.csv")
gdp_dataset = pd.read_csv("./datasets folder/INDIA_STATE_WISE_GDP_2001_2011.csv")
education_dataset = pd.read_csv("./datasets folder/Educational_standard_of_inmates.csv")
literacy_dataset = pd.read_csv("./datasets folder/LITERACY_RATE.csv")

st.write('''While performing EDA (Exploratory data analysis), I found out that the names of some of the 
Indian states were represented differently in different datasets. Therefore, I need to do some data 
preprocessing steps, in order to bring the required uniformity, before starting to build the respective plots. 
Firstly, I extract the correct names for all states and try to map them accordingly onto all datasets.''')

st.subheader("Defining a function to return a dictionary, whose keys are the wrong state names and the respective values are the correct versions:")
def map_correct_to_wrong_states(
        correct_names: list,
        wrong_names: list):
    state_mapping = {}
    if len(correct_names) != len(wrong_names):
        print("Check names something is wrong in the wrong_name list")
    for i in range(len(correct_names)):
        state_mapping[wrong_names[i]] = correct_names[i]
    return state_mapping
code = '''def map_correct_to_wrong_states(
        correct_names: list,
        wrong_names: list):
    state_mapping = {}
    if len(correct_names) != len(wrong_names):
        print("Check names something is wrong in the wrong_name list")
    for i in range(len(correct_names)):
        state_mapping[wrong_names[i]] = correct_names[i]
    return state_mapping'''
st.code(code, language="python")

st.subheader("Calling the above function using the state names from crime and census datasets:")
correct_state_list = sorted(census_dataset['State/Union Territory'].values)
crime_dataset_states = sorted(crime_dataset['STATE/UT'].unique())
state_mapping = map_correct_to_wrong_states(correct_state_list, crime_dataset_states)
code = '''correct_state_list = sorted(census_dataset['State/Union Territory'].values)
crime_dataset_states = sorted(crime_dataset['STATE/UT'].unique())
state_mapping = map_correct_to_wrong_states(correct_state_list, crime_dataset_states)
'''
st.code(code, language="python")
st.write(state_mapping)
st.write('''There are certain Indian states missing in some of the datasets. Their names are Dhadra and Nagar Haveli, Lakshwadeep and lastly, Damen and Diu. They represent very minor and small states/islands, therefore can be ignored.''')

st.subheader("Dropping the above states from the crime, education, literacy and census datasets:")
crime_dataset = crime_dataset.replace({'STATE/UT':state_mapping})
crime_dataset = crime_dataset[crime_dataset['STATE/UT'] != 'Dadra and Nagar Haveli']
crime_dataset = crime_dataset[crime_dataset['STATE/UT'] != 'Daman and Diu']
crime_dataset = crime_dataset[crime_dataset['STATE/UT'] != 'Lakshadweep']
correct_state_list = sorted(crime_dataset['STATE/UT'].unique())
crime_dataset = crime_dataset.replace({'STATE/UT':state_mapping})

education_dataset = education_dataset[education_dataset['STATE/UT'] != 'D & N HAVELI']
education_dataset = education_dataset[education_dataset['STATE/UT'] != 'DAMAN & DIU']
education_dataset = education_dataset[education_dataset['STATE/UT'] != 'LAKSHADWEEP']

literacy_dataset = literacy_dataset[literacy_dataset['State/UT'] != 'Dadra and Nagar Haveli']
literacy_dataset = literacy_dataset[literacy_dataset['State/UT'] != 'Daman and Diu']
literacy_dataset = literacy_dataset[literacy_dataset['State/UT'] != 'Lakshadweep']

census_dataset = census_dataset[census_dataset['State/Union Territory'] != 'Dadra and Nagar Haveli']
census_dataset = census_dataset[census_dataset['State/Union Territory'] != 'Daman and Diu']
census_dataset = census_dataset[census_dataset['State/Union Territory'] != 'Lakshadweep']

code = '''crime_dataset = crime_dataset.replace({'STATE/UT':state_mapping})
crime_dataset = crime_dataset[crime_dataset['STATE/UT'] != 'Dadra and Nagar Haveli']
crime_dataset = crime_dataset[crime_dataset['STATE/UT'] != 'Daman and Diu']
crime_dataset = crime_dataset[crime_dataset['STATE/UT'] != 'Lakshadweep']
correct_state_list = sorted(crime_dataset['STATE/UT'].unique())
crime_dataset = crime_dataset.replace({'STATE/UT':state_mapping})

education_dataset = education_dataset[education_dataset['STATE/UT'] != 'D & N HAVELI']
education_dataset = education_dataset[education_dataset['STATE/UT'] != 'DAMAN & DIU']
education_dataset = education_dataset[education_dataset['STATE/UT'] != 'LAKSHADWEEP']

literacy_dataset = literacy_dataset[literacy_dataset['State/UT'] != 'Dadra and Nagar Haveli']
literacy_dataset = literacy_dataset[literacy_dataset['State/UT'] != 'Daman and Diu']
literacy_dataset = literacy_dataset[literacy_dataset['State/UT'] != 'Lakshadweep']

census_dataset = census_dataset[census_dataset['State/Union Territory'] != 'Dadra and Nagar Haveli']
census_dataset = census_dataset[census_dataset['State/Union Territory'] != 'Daman and Diu']
census_dataset = census_dataset[census_dataset['State/Union Territory'] != 'Lakshadweep']
'''
st.code(code, language="python")

st.subheader("Mapping the wrong state names to the correct versions for all the datasets:")
state_mapping = map_correct_to_wrong_states(correct_names=correct_state_list,
                                            wrong_names=sorted(gdp_dataset['State/union territory'].unique()))
gdp_dataset = gdp_dataset.replace({'State/union territory':state_mapping})

state_mapping = map_correct_to_wrong_states(correct_names=correct_state_list,
                                            wrong_names=sorted(education_dataset['STATE/UT'].unique()))

education_dataset = education_dataset.replace({'STATE/UT':state_mapping})

state_mapping = map_correct_to_wrong_states(correct_names=correct_state_list,
                                            wrong_names=sorted(literacy_dataset['State/UT'].unique()))
                        
literacy_dataset = literacy_dataset.replace({'State/UT':state_mapping})
code = '''state_mapping = map_correct_to_wrong_states(correct_names=correct_state_list,
                                            wrong_names=sorted(gdp_dataset['State/union territory'].unique()))
gdp_dataset = gdp_dataset.replace({'State/union territory':state_mapping})

state_mapping = map_correct_to_wrong_states(correct_names=correct_state_list,
                                            wrong_names=sorted(education_dataset['STATE/UT'].unique()))

education_dataset = education_dataset.replace({'STATE/UT':state_mapping})

state_mapping = map_correct_to_wrong_states(correct_names=correct_state_list,
                                            wrong_names=sorted(literacy_dataset['State/UT'].unique()))
                        
literacy_dataset = literacy_dataset.replace({'State/UT':state_mapping})'''
st.code(code, language="python")
st.write('''Another feature that is quite important is to see if all data is available for the given years. 
I found out that the population data and GDP are available only for the time period 2001-2011.
Therefore, I have to query all data present between the years 2001 until 2011 for crime and education datasets.''')
education_dataset = education_dataset[education_dataset['YEAR'] != 2012]
crime_dataset = crime_dataset[crime_dataset['YEAR'] != 2012]
code = '''education_dataset = education_dataset[education_dataset['YEAR'] != 2012]
crime_dataset = crime_dataset[crime_dataset['YEAR'] != 2012]'''
st.code(code, language="python")

st.subheader("After exporting the above datasets as csv files and performing some other minimal preprocesssing steps on Excel, I stored them as new csv files inside \"preprocessed_datasets\" folder(inside \"datasets\" folder.)")
st.subheader("Importing the new csv files representing Indian crime, population, GDP, education and literacy datasets:")
crime_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_dataset.csv")
census_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/census_data.csv")
gdp_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/gdp_dataset.csv")
education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/education_dataset.csv")
literacy_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/literacy_rate_dataset.csv")
code = '''crime_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_dataset.csv")
census_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/census_data.csv")
gdp_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/gdp_dataset.csv")
education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/education_dataset.csv")
literacy_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/literacy_rate_dataset.csv")
'''
st.code(code, language="python")

st.write('''As crime and total GDP of a state cannot be measured just as an absolute value, 
due to the fact that population plays a huge role in such progress, I need to scale them equally per capita. 
So I should convert all the available numeric continuous data to per capita form, by dividing each value 
by the total population of the respective Indian state.''')

st.subheader("Creating 2 Python lists, one containing the column names representing the crime types of the crime dataset and the second one containing the same elements but now adding 'PER_CAPITA' extension:")
columns_list = ['MURDER', 'ATTEMPT TO MURDER',
       'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 'RAPE', 'CUSTODIAL RAPE',
       'OTHER RAPE', 'KIDNAPPING & ABDUCTION',
       'KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS',
       'KIDNAPPING AND ABDUCTION OF OTHERS', 'DACOITY',
       'PREPARATION AND ASSEMBLY FOR DACOITY', 'ROBBERY', 'BURGLARY', 'THEFT',
       'AUTO THEFT', 'OTHER THEFT', 'RIOTS', 'CRIMINAL BREACH OF TRUST',
       'CHEATING', 'COUNTERFIETING', 'ARSON', 'HURT/GREVIOUS HURT',
       'DOWRY DEATHS', 'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY',
       'INSULT TO MODESTY OF WOMEN', 'CRUELTY BY HUSBAND OR HIS RELATIVES',
       'IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES',
       'CAUSING DEATH BY NEGLIGENCE', 'OTHER IPC CRIMES', 'TOTAL IPC CRIMES']

new_columns_list = ['MURDER_PER_CAPITA', 'ATTEMPT TO MURDER_PER_CAPITA',
       'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER_PER_CAPITA', 'RAPE_PER_CAPITA', 'CUSTODIAL RAPE_PER_CAPITA',
       'OTHER RAPE_PER_CAPITA', 'KIDNAPPING & ABDUCTION_PER_CAPITA',
       'KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS_PER_CAPITA',
       'KIDNAPPING AND ABDUCTION OF OTHERS_PER_CAPITA', 'DACOITY_PER_CAPITA',
       'PREPARATION AND ASSEMBLY FOR DACOITY_PER_CAPITA', 'ROBBERY_PER_CAPITA', 'BURGLARY_PER_CAPITA', 'THEFT_PER_CAPITA',
       'AUTO THEFT_PER_CAPITA', 'OTHER THEFT_PER_CAPITA', 'RIOTS_PER_CAPITA', 'CRIMINAL BREACH OF TRUST_PER_CAPITA',
       'CHEATING_PER_CAPITA', 'COUNTERFIETING_PER_CAPITA', 'ARSON_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA',
       'DOWRY DEATHS_PER_CAPITA', 'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY_PER_CAPITA',
       'INSULT TO MODESTY OF WOMEN_PER_CAPITA', 'CRUELTY BY HUSBAND OR HIS RELATIVES_PER_CAPITA',
       'IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES_PER_CAPITA',
       'CAUSING DEATH BY NEGLIGENCE_PER_CAPITA', 'OTHER IPC CRIMES_PER_CAPITA', 'TOTAL IPC CRIMES_PER_CAPITA',
       'STATE', 'YEAR']
code = '''columns_list = ['MURDER', 'ATTEMPT TO MURDER',
       'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER', 'RAPE', 'CUSTODIAL RAPE',
       'OTHER RAPE', 'KIDNAPPING & ABDUCTION',
       'KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS',
       'KIDNAPPING AND ABDUCTION OF OTHERS', 'DACOITY',
       'PREPARATION AND ASSEMBLY FOR DACOITY', 'ROBBERY', 'BURGLARY', 'THEFT',
       'AUTO THEFT', 'OTHER THEFT', 'RIOTS', 'CRIMINAL BREACH OF TRUST',
       'CHEATING', 'COUNTERFIETING', 'ARSON', 'HURT/GREVIOUS HURT',
       'DOWRY DEATHS', 'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY',
       'INSULT TO MODESTY OF WOMEN', 'CRUELTY BY HUSBAND OR HIS RELATIVES',
       'IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES',
       'CAUSING DEATH BY NEGLIGENCE', 'OTHER IPC CRIMES', 'TOTAL IPC CRIMES']

new_columns_list = ['MURDER_PER_CAPITA', 'ATTEMPT TO MURDER_PER_CAPITA',
       'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER_PER_CAPITA', 'RAPE_PER_CAPITA', 'CUSTODIAL RAPE_PER_CAPITA',
       'OTHER RAPE_PER_CAPITA', 'KIDNAPPING & ABDUCTION_PER_CAPITA',
       'KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS_PER_CAPITA',
       'KIDNAPPING AND ABDUCTION OF OTHERS_PER_CAPITA', 'DACOITY_PER_CAPITA',
       'PREPARATION AND ASSEMBLY FOR DACOITY_PER_CAPITA', 'ROBBERY_PER_CAPITA', 'BURGLARY_PER_CAPITA', 'THEFT_PER_CAPITA',
       'AUTO THEFT_PER_CAPITA', 'OTHER THEFT_PER_CAPITA', 'RIOTS_PER_CAPITA', 'CRIMINAL BREACH OF TRUST_PER_CAPITA',
       'CHEATING_PER_CAPITA', 'COUNTERFIETING_PER_CAPITA', 'ARSON_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA',
       'DOWRY DEATHS_PER_CAPITA', 'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY_PER_CAPITA',
       'INSULT TO MODESTY OF WOMEN_PER_CAPITA', 'CRUELTY BY HUSBAND OR HIS RELATIVES_PER_CAPITA',
       'IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES_PER_CAPITA',
       'CAUSING DEATH BY NEGLIGENCE_PER_CAPITA', 'OTHER IPC CRIMES_PER_CAPITA', 'TOTAL IPC CRIMES_PER_CAPITA',
       'STATE', 'YEAR']'''
st.code(code, language="python")

st.subheader("Creating 2 other Python lists, one for the unique years and the other one for the unique state names inside the crime dataset:")
years = list(crime_dataset.YEAR.unique())
states_list = list(crime_dataset['STATE/UT'].unique())
code = '''years = list(crime_dataset.YEAR.unique())
states_list = list(crime_dataset['STATE/UT'].unique())'''
st.code(code, language="python")

st.subheader("Creating the Pandas DataFrame containing the number of cases for all the crimes types in each indian state and the repspective year, but now their value per capita:")
df_data = []
i = 0
for year in years:
    for state in states_list:
        value_list = []
        temp_df = crime_dataset[crime_dataset.YEAR == 2001]
        crime_values = list(temp_df[columns_list][temp_df['STATE/UT'] == state].values)
        population = census_dataset[str(year)][census_dataset["State/Union Territory"] == state].values[0]

        temp_list = (crime_values/population).tolist()[0]

        temp_list.append(state)
        temp_list.append(year)
        df_data.append(temp_list)

temp_df = pd.DataFrame(df_data, columns=new_columns_list)
code = '''df_data = []
i = 0
for year in years:
    for state in states_list:
        value_list = []
        temp_df = crime_dataset[crime_dataset.YEAR == 2001]
        crime_values = list(temp_df[columns_list][temp_df['STATE/UT'] == state].values)
        population = census_dataset[str(year)][census_dataset["State/Union Territory"] == state].values[0]

        temp_list = (crime_values/population).tolist()[0]

        temp_list.append(state)
        temp_list.append(year)
        df_data.append(temp_list)

temp_df = pd.DataFrame(df_data, columns=new_columns_list)
temp_df'''
st.code(code, language="python")
st.write(temp_df)

st.subheader("Performing the same preprocessing step on the GDP dataset, which now contains data for all the indian states:")
states_list = gdp_dataset['State/union territory'].unique()
gdp_data = []
for state in states_list:
    temp_list = []
    temp_list.append(state)
    for year in years:
        year = str(year)
        population = census_dataset[year][census_dataset["State/Union Territory"] == state].values[0]
        gdp = gdp_dataset[year][gdp_dataset['State/union territory'] == state].values[0]
        temp_list.append(gdp/population)
    gdp_data.append(temp_list)

gdp_per_capita_df = pd.DataFrame(gdp_data, columns=gdp_dataset.columns)
gdp_per_capita_df = gdp_per_capita_df.sort_values('State/union territory', ascending=True)
code = '''states_list = gdp_dataset['State/union territory'].unique()
gdp_data = []
for state in states_list:
    temp_list = []
    temp_list.append(state)
    for year in years:
        year = str(year)
        population = census_dataset[year][census_dataset["State/Union Territory"] == state].values[0]
        gdp = gdp_dataset[year][gdp_dataset['State/union territory'] == state].values[0]
        temp_list.append(gdp/population)
    gdp_data.append(temp_list)

gdp_per_capita_df = pd.DataFrame(gdp_data, columns=gdp_dataset.columns)
gdp_per_capita_df = gdp_per_capita_df.sort_values('State/union territory', ascending=True)
gdp_per_capita_df.head()'''
st.code(code, language = "python")
st.write(gdp_per_capita_df)

st.subheader("After exporting the above Pandas DataFrames as csv files inside \"preprocessed_datasets\" and performing some other minor preprocessing steps, I import them again as DataFrames:")
crime_data_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/crime_dataset_per_capita.csv")
gdp_data_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/gdp_dataset_per_capita.csv")
code = '''crime_data_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/crime_dataset_per_capita.csv")
gdp_data_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/gdp_dataset_per_capita.csv")'''
st.code(code, language="python")

st.subheader("Merging all datasets together to create a final one including crimes per capita, GDP and literacy rate:")
code = '''years = crime_data_per_capita.YEAR.unique()
states = crime_data_per_capita['STATE'].unique()
concat_data = []
for state in states:
    for year in years:
        year = str(year)
        gdp = gdp_data_per_capita[year][gdp_data_per_capita["State/union territory"] == state].values[0]
        literacy_rate = literacy_dataset[year][literacy_dataset["STATE/UT"] == state].values[0]
        population = census_dataset[year][census_dataset["State/Union Territory"] == state].values[0]
        literacy_rate_pop = (literacy_rate/100)*population
        literacy_rate_per_capita = literacy_rate_pop/population
        concat_data.append([gdp, literacy_rate, literacy_rate_per_capita])

temp_df = pd.DataFrame(concat_data, columns=["GDP", "literacy_rate_percentage" ,"Literacy_Rate_per_capita"])

crime_data_per_capita = pd.concat([crime_data_per_capita, temp_df], axis=1)

crime_data_per_capita.head()'''
st.code(code, language="python")
years = crime_data_per_capita.YEAR.unique()
states = crime_data_per_capita['STATE'].unique()
concat_data = []
for state in states:
    for year in years:
        year = str(year)
        gdp = gdp_data_per_capita[year][gdp_data_per_capita["State/union territory"] == state].values[0]
        literacy_rate = literacy_dataset[year][literacy_dataset["STATE/UT"] == state].values[0]
        population = census_dataset[year][census_dataset["State/Union Territory"] == state].values[0]
        literacy_rate_pop = (literacy_rate/100)*population
        literacy_rate_per_capita = literacy_rate_pop/population
        concat_data.append([gdp, literacy_rate, literacy_rate_per_capita])

temp_df = pd.DataFrame(concat_data, columns=["GDP", "literacy_rate_percentage" ,"Literacy_Rate_per_capita"])

crime_data_per_capita = pd.concat([crime_data_per_capita, temp_df], axis=1)
st.write(crime_data_per_capita.head())
st.write("The reason behind that is to simplify the process of building the respective plots later.")


st.header("2. Analysing state-wise crime in India")

st.subheader("Importing the proprocessed csv files including data combinations between crime and education and also crime values per capita, as Pandas DataFrames:")
crime_education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_and_education_merged_dataset.csv")
crime_dataset_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/per_capita_crime_dataset_with_gdp_literacy_rate.csv")
code = '''crime_education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_and_education_merged_dataset.csv")
crime_dataset_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/per_capita_crime_dataset_with_gdp_literacy_rate.csv")'''
st.code(code, language = "python")

st.subheader("Plotting an animated choropleth map showing the \"TOTAL IPC Crimes\" number of cases per capita:")
code = '''fig = px.choropleth(
    crime_dataset_per_capita,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='STATE',
    color = "TOTAL IPC CRIMES_PER_CAPITA",
    animation_frame = "YEAR",
    range_color=(0, 0.004),
     color_continuous_scale=[[0, 'rgb(240,240,240)'],
                      [0.05, 'rgb(13,136,198)'],
                      [0.1, 'rgb(191,247,202)'],
                      [0.20, 'rgb(4,145,32)'],
                      [1, 'rgb(227,26,28,0.5)']],
    )

fig.update_geos(fitbounds="locations", visible=False)

fig.show()'''
st.code(code, language="python")
is_clicked = st.button("Show animated map", key="total_crimes_per_capita_map")
if is_clicked:
    fig = px.choropleth(
        crime_dataset_per_capita,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='STATE',
        color = "TOTAL IPC CRIMES_PER_CAPITA",
        animation_frame = "YEAR",
        range_color=(0, 0.004),
        color_continuous_scale=[[0, 'rgb(240,240,240)'],
                        [0.05, 'rgb(13,136,198)'],
                        [0.1, 'rgb(191,247,202)'],
                        [0.20, 'rgb(4,145,32)'],
                        [1, 'rgb(227,26,28,0.5)']],
    )

    fig.update_geos(fitbounds="locations", visible=False)

    st.plotly_chart(fig, use_container_width=True)

st.write("The data was collected by Indian Government website before the partition of Andhra Pradesh. The missing/white part in the map belonged to Andhra Pradesh before and is currently missing due to the updated GeoJSON file.")
st.write('''The above animated Choropleth Map demonstrates the progress 
of the Total IPC Crimes according to the Indian Penal Code, focusing on the 
time period from 2001 up to 2011. India has vastly developed in many sectors 
in the following years which has lead to a significant growth in the economy. 
On the other hand, I have also noticed a lot of crimes being committed. This 
could be a harmful factor in hindering the growth of the overall economy. I 
would first like to understand how the total crime rate has progressed 
in India in the 10 years that have passed. In the above map we can see a positive impact 
with colors changing to a lighter shade, giving an overview that total crimes per capita have 
decreased in overall. However, states like Madhya Pradesh, Rajasthan, Kerala and Tamil Nadu are 
quite evident, in terms of having higher crime rates compared to most other states. So these are 
the most affected states in India. What I can do now, is discovering the leading crime types for 
each of these states. ''')

st.subheader("Starting with analysing Madhya Pradesh, by firstly creating a Pandas DataFrame containing crime data only for this Indian state:")
madhya_pradesh_df = crime_dataset_per_capita[crime_dataset_per_capita['STATE'] == "Madhya Pradesh"]
code = '''madhya_pradesh_df = crime_dataset_per_capita[crime_dataset_per_capita['STATE'] == "Madhya Pradesh"]
madhya_pradesh_df'''
st.code(code, language="python")
st.write(madhya_pradesh_df)

st.write('''Secondly, I will determine the leading crime type in Madhya Pradesh for each year during the time period from 2001 up to 2011. 
In order to do that, I create a new Python list, where I store all the strings representing the leading crime types for the respective year. 
The most frequent values/strings in this list represent the leading crime type in this Indian state.''')

st.subheader("Defining a function to determine the leading crime type for each year from 2001 to 2011:")
def define_leading_crime_type(respective_df):
    crime_types_list = list(respective_df.columns)
    crime_types_list = crime_types_list[:len(crime_types_list) - 7]

    leading_crime_type_per_year = []

    for index, rows in respective_df.iterrows():
        crime_values_per_year = []
        for i in range(len(crime_types_list)):
            crime_values_per_year.append(rows[crime_types_list[i]])
        leading_crime_value = max(crime_values_per_year)
        leading_crime_index = crime_values_per_year.index(leading_crime_value)
        leading_crime_name = crime_types_list[leading_crime_index]
        leading_crime_type_per_year.append(leading_crime_name)
    return leading_crime_type_per_year

code = '''def define_leading_crime_type(respective_df):
    crime_types_list = list(respective_df.columns)
    crime_types_list = crime_types_list[:len(crime_types_list) - 7]

    leading_crime_type_per_year = []

    for index, rows in respective_df.iterrows():
        crime_values_per_year = []
        for i in range(len(crime_types_list)):
            crime_values_per_year.append(rows[crime_types_list[i]])
        leading_crime_value = max(crime_values_per_year)
        leading_crime_index = crime_values_per_year.index(leading_crime_value)
        leading_crime_name = crime_types_list[leading_crime_index]
        leading_crime_type_per_year.append(leading_crime_name)
    return leading_crime_type_per_year'''
st.code(code, language="python")
st.write('''The above function has only one argument, which is the Pandas dataframe, representing the respective Indian state between 
Madhya Pradesh, Rajasthan, Kerala or Tamil Nadu. Inside the function block, I create a list called "crime_types_list", which stores 
all the column names of the Pandas Dataframe (containing data about the respective Indian state), representing the crime types. 
I decided to exclude "Other IPC Crimes" while performing our data analysis part. The reason is that due to comprising lots of 
crime types, this column always contains the largest value compared to other crime columns. So it would always have been the leading 
crime type for each of the Indian states I am analysing. However, I will visualise the progress of "Other IPC Crimes" later, 
along with the other 3 leading crimes that I will discover below.''')

st.subheader("Calling the above function to define the leading crime types for Madhya Pradesh:")
years_list = list(range(2001,2012))
leading_crimes_mp_list = define_leading_crime_type(madhya_pradesh_df)
leading_crime_mp_dict = {years_list[i]: leading_crimes_mp_list[i] for i in range(len(years_list))}
code = '''years_list = list(range(2001,2012))
leading_crimes_mp_list = define_leading_crime_type(madhya_pradesh_df)
leading_crime_mp_dict = {years_list[i]: leading_crimes_mp_list[i] for i in range(len(years_list))}
leading_crime_mp_dict'''
st.code(code, language="python")
st.write(leading_crime_mp_dict)
st.write("As we can see from the above Python dictionary, Madhya Pradesh is mostly affected by \"HURT/GREVIOUS HURT\". This is the leading crime type for each year.")

st.subheader("Excluding this column from Madhya Pradesh dataset, in order to determine the second leading crime in this state:")
madhya_pradesh_df = madhya_pradesh_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)
code = '''madhya_pradesh_df = madhya_pradesh_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)
madhya_pradesh_df'''
st.code(code, language="python")

st.subheader("Discovering the second leading crime type in Madhya Pradesh from 2001 to 2011:")
leading_crimes_mp_list = define_leading_crime_type(madhya_pradesh_df)
leading_crime_mp_dict = {years_list[i]: leading_crimes_mp_list[i] for i in range(len(years_list))}
code = '''leading_crimes_mp_list = define_leading_crime_type(madhya_pradesh_df)
leading_crime_mp_dict = {years_list[i]: leading_crimes_mp_list[i] for i in range(len(years_list))}
leading_crime_mp_dict'''
st.code(code, language = "python")
st.write(leading_crime_mp_dict)
st.write("The above result clearly indicates that the second leading crime in Madhya Pradesh is \"THEFT\".")

st.subheader("Performing the same step as above, by excluding \"THEFT\" column from Madhya Pradesh dataset, in order to determine the third leading crime in this state:")
madhya_pradesh_df = madhya_pradesh_df.drop('THEFT_PER_CAPITA', axis=1)

leading_crimes_mp_list = define_leading_crime_type(madhya_pradesh_df)
leading_crime_mp_dict = {years_list[i]: leading_crimes_mp_list[i] for i in range(len(years_list))}
code = '''madhya_pradesh_df = madhya_pradesh_df.drop('THEFT_PER_CAPITA', axis=1)
madhya_pradesh_df

leading_crimes_mp_list = define_leading_crime_type(madhya_pradesh_df)
leading_crime_mp_dict = {years_list[i]: leading_crimes_mp_list[i] for i in range(len(years_list))}
leading_crime_mp_dict'''
st.code(code, language="python")
st.write(leading_crime_mp_dict)
st.write("So the third leading crime in Madhya Pradesh is \"OTHER THEFT\". It is worth mentioning that for the 3 dominant crimes that we discovered above, they remain in the \"champion\" position during the entire period from 2001 to 2011.")

st.subheader("Creating another Pandas DataFrame, which contains data only for the 4 Indian states that I am analysing here (Madhya Pradesh, Rajasthan, Kerala and Tamil Nadu):")
most_affected_states = ['Madhya Pradesh', 'Rajasthan', 'Kerala', 'Tamil Nadu'] 
most_affected_states_df = crime_dataset_per_capita[crime_dataset_per_capita['STATE'].isin(most_affected_states)]
code = '''most_affected_states = ['Madhya Pradesh', 'Rajasthan', 'Kerala', 'Tamil Nadu'] 
most_affected_states_df = crime_dataset_per_capita[crime_dataset_per_capita['STATE'].isin(most_affected_states)]
most_affected_states_df.head()'''
st.code(code, language="python")
st.write(most_affected_states_df)
st.write("This will simplify performing the same steps later for determining the leading crime types for the last 3 states.")

st.subheader("Visualising the progress of Madhya Pradesh GDP, 3 leading crime types that I discovered above and also \"Other IPC Crimes\", from 2001 to 2011:")
code = '''madhya_pradesh_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[0]]

fig = make_subplots(
    rows=3, cols=2,
    specs=[[{"colspan": 2}, None],
        [{}, {}],
        [{}, {}]],
    subplot_titles=(f"GDP of {most_affected_states[0]} (2001-2011)",
                    "Other IPC Crimes per capita (2001 - 2011)", 
                    "HURT/GREVIOUS HURT per capita (2001 - 2011)",
                    "THEFT per capita (2001 - 2011)", 
                    "OTHER THEFT per capita (2001 - 2011)"))


fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['GDP'].values),
                 row=1, col=1)
fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['OTHER IPC CRIMES_PER_CAPITA'].values),
                 row=2, col=1)
fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['HURT/GREVIOUS HURT_PER_CAPITA'].values),
                 row=2, col=2)
fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['THEFT_PER_CAPITA'].values),
                 row=3, col=1)
fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['OTHER THEFT_PER_CAPITA'].values),
                row=3, col=2)
fig.update_layout(height=1080, width=900,
                  title_text="Multiple Subplots with Shared Y-Axes", showlegend=False)'''
st.code(code, language="python")
madhya_pradesh_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[0]]
is_clicked1 = st.button("Show the plots", key="mp_plots")
if is_clicked1:
    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{"colspan": 2}, None],
            [{}, {}],
            [{}, {}]],
        subplot_titles=(f"GDP of {most_affected_states[0]} (2001-2011)",
                    "Other IPC Crimes per capita (2001 - 2011)", 
                    "HURT/GREVIOUS HURT per capita (2001 - 2011)",
                    "THEFT per capita (2001 - 2011)", 
                    "OTHER THEFT per capita (2001 - 2011)"))


    fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['GDP'].values),
                 row=1, col=1)
    fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['OTHER IPC CRIMES_PER_CAPITA'].values),
                 row=2, col=1)
    fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['HURT/GREVIOUS HURT_PER_CAPITA'].values),
                 row=2, col=2)
    fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['THEFT_PER_CAPITA'].values),
                 row=3, col=1)
    fig.add_trace(go.Scatter(x=madhya_pradesh_df['YEAR'].unique(), y=madhya_pradesh_df['OTHER THEFT_PER_CAPITA'].values),
                row=3, col=2)
    fig.update_layout(height=1080, width=900,
                  title_text="Multiple Subplots with Shared Y-Axes", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.write('''As we can see from the first plot, GDP per capita of Madhya Pradesh has tripled 
from 2001 to 2011, which is great news. In addition to that, the number of cases for each of 
the prevailing crimes in this state of India has decreased during this period of time. The 
very small values of each crime per capita are due to the large population, about 83 million 
inhabitants. To sum up, a negative correlation is observed between GDP and the predominant 
types of crime in Madhya Pradesh.''')

st.write("Let's now have a look at the second most affected state, which is Rajasthan. Again, I need to determine 3 leading crime types after \"Other IPC Crimes\".")

st.subheader("Extracting all the information about Rajasthan from \"most_affected_states_df\" and storing it into a new Pandas DataFrame:")
rajasthan_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[1]]
st.code("rajasthan_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[1]]",
        language="python")

st.subheader("Determining the first leading crime type throughout the yeasrs in Rajasthan:")
leading_crimes_r_list = define_leading_crime_type(rajasthan_df)
leading_crimes_r_dict = {years_list[i]: leading_crimes_r_list[i] for i in range(len(years_list))}
code = '''leading_crimes_r_list = define_leading_crime_type(rajasthan_df)
leading_crimes_r_dict = {years_list[i]: leading_crimes_r_list[i] for i in range(len(years_list))}
leading_crimes_r_dict'''
st.code(code, language="python")
st.write(leading_crimes_r_dict)
st.write("Just like in case of Madhya Pradesh, even in Rajasthan the first leading type after \"Other IPC Crimes\" is \"HURT/GREVIOUS HURT\".")

st.subheader("Dropping \"HURT/GREVIOUS HURT_PER_CAPITA\" column from the above DataFrame and determining the second leading crime type:")
rajasthan_df = rajasthan_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)

leading_crimes_r_list = define_leading_crime_type(rajasthan_df)
leading_crimes_r_dict = {years_list[i]: leading_crimes_r_list[i] for i in range(len(years_list))}
code = '''rajasthan_df = rajasthan_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)

leading_crimes_r_list = define_leading_crime_type(rajasthan_df)
leading_crimes_r_dict = {years_list[i]: leading_crimes_r_list[i] for i in range(len(years_list))}
leading_crimes_r_dict'''
st.code(code, language="python")
st.write(leading_crimes_r_dict)
st.write("Again we have the same situation as in case of Madhya Pradesh. Theft is one of the dominant crimes in Rajasthan.")

st.subheader("Dropping \"THEFT_PER_CAPITA\" column from the above DataFrame and determining the third leading crime type:")
rajasthan_df = rajasthan_df.drop('THEFT_PER_CAPITA', axis=1)

leading_crimes_r_list = define_leading_crime_type(rajasthan_df)
leading_crimes_r_dict = {years_list[i]: leading_crimes_r_list[i] for i in range(len(years_list))}
code = '''rajasthan_df = rajasthan_df.drop('THEFT_PER_CAPITA', axis=1)

leading_crimes_r_list = define_leading_crime_type(rajasthan_df)
leading_crimes_r_dict = {years_list[i]: leading_crimes_r_list[i] for i in range(len(years_list))}
leading_crimes_r_dict'''
st.code(code, language="python")
st.write(leading_crimes_r_dict)
st.write("Just like in Madhya Pradesh, even in Rajasthan \"Other Theft\" is the third leading crime type after \"Other IPC Crimes\".")

st.write("Now let's build the same plots for Rajasthan, the progress of GDP and 4 leading crime types from 2001 up to 2011. In order not to avoid writing repetitive code, we implement a function for this aim. It needs only 2 arguments, the specific Indian state and a list containing 4 leading crime types in the respective state. I will also use this function later for the visualisations of the last 2 most affected states.")

st.subheader("Defining the above function:")
def visualise_gdp_and_leading_crimes(most_affected_state, leading_crime_types):

    state_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_state]

    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{"colspan": 2}, None],
            [{}, {}],
            [{}, {}]],
        subplot_titles=(f"GDP of {most_affected_state} (2001-2011)",
                    "{} (2001 - 2011)".format(leading_crime_types[0]), 
                    "{} (2001 - 2011)".format(leading_crime_types[1]),
                    "{} (2001 - 2011)".format(leading_crime_types[2]), 
                    "{} (2001 - 2011)".format(leading_crime_types[3])))


    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df['GDP'].values),
                 row=1, col=1)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[0]].values),
                 row=2, col=1)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[1]].values),
                 row=2, col=2)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[2]].values),
                 row=3, col=1)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[3]].values),
                row=3, col=2)
    fig.update_layout(height=1080, width=900,
                  title_text="Multiple Subplots with Shared Y-Axes", showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

code = '''def visualise_gdp_and_leading_crimes(most_affected_state, leading_crime_types):

    state_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_state]

    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{"colspan": 2}, None],
            [{}, {}],
            [{}, {}]],
        subplot_titles=(f"GDP of {most_affected_state} (2001-2011)",
                    "{} (2001 - 2011)".format(leading_crime_types[0]), 
                    "{} (2001 - 2011)".format(leading_crime_types[1]),
                    "{} (2001 - 2011)".format(leading_crime_types[2]), 
                    "{} (2001 - 2011)".format(leading_crime_types[3])))


    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df['GDP'].values),
                 row=1, col=1)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[0]].values),
                 row=2, col=1)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[1]].values),
                 row=2, col=2)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[2]].values),
                 row=3, col=1)
    fig.add_trace(go.Scatter(x=state_df['YEAR'].unique(), y=state_df[leading_crime_types[3]].values),
                row=3, col=2)
    fig.update_layout(height=1080, width=900,
                  title_text="Multiple Subplots with Shared Y-Axes", showlegend=False)

    fig.show()'''
st.code(code, language="python")

st.subheader("Visualising Rajasthan's GDP and leading crime types progress:")
code = "visualise_gdp_and_leading_crimes(most_affected_state = most_affected_states[1], leading_crime_types = ['OTHER IPC CRIMES_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA', 'THEFT_PER_CAPITA', 'OTHER THEFT_PER_CAPITA'])"
st.code(code, language="python")
is_clicked2 = st.button("Show the plots")
if is_clicked2:
    visualise_gdp_and_leading_crimes(most_affected_state = most_affected_states[1], leading_crime_types = ['OTHER IPC CRIMES_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA', 'THEFT_PER_CAPITA', 'OTHER THEFT_PER_CAPITA'])

st.write("The situation appears very similar to the case of Madhya Pradesh. So once again we have a tripling of GDP from 2001 to 2011. Also, the prevailing crimes in Rajasthan have caused a decrease in the number of cases in this period of time. So even this state demonstrates a negative correlation between GDP and dominant crimes.")
st.write("Let's now concentrate on the third most affected Indian state, Kerala.")

st.subheader("Extracting all the information about Kerala from \"most_affected_states_df\" and storing it into the new Pandas DataFrame:")
kerala_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[2]]
code = "kerala_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[2]]"
st.code(code, language="python")

st.subheader("Defining the first leading crime type in Kerala throughout the years:")
leading_crimes_k_list = define_leading_crime_type(kerala_df)
leading_crimes_k_dict = {years_list[i]: leading_crimes_k_list[i] for i in range(len(years_list))}
code = '''leading_crimes_k_list = define_leading_crime_type(kerala_df)
leading_crimes_k_dict = {years_list[i]: leading_crimes_k_list[i] for i in range(len(years_list))}
leading_crimes_k_dict'''
st.code(code, language="python")
st.write(leading_crimes_k_dict)
st.write("Just like in case of Madhya Pradesh and Rajasthan, even in Kerala the first leading type after \"Other IPC Crimes\" is \"HURT/GREVIOUS HURT\".")

st.subheader("Dropping \"HURT/GREVIOUS HURT_PER_CAPITA\" column from the above DataFrame and determining the second leading crime type:")
kerala_df = kerala_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)
leading_crimes_k_list = define_leading_crime_type(kerala_df)
leading_crimes_k_dict = {years_list[i]: leading_crimes_k_list[i] for i in range(len(years_list))}
code = '''kerala_df = kerala_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)
leading_crimes_k_list = define_leading_crime_type(kerala_df)
leading_crimes_k_dict = {years_list[i]: leading_crimes_k_list[i] for i in range(len(years_list))}
leading_crimes_k_dict'''
st.code(code, language="python")
st.write(leading_crimes_k_dict)
st.write('''Now we have a different situation compared to the case of Madhya Pradesh and Rajasthan. RIOTS represent the second most dominant crime in Kerala, after "Other IPC Crimes". It looks like Kerala suffers from violent public disorders, so disturbances of the public peace by three or more persons assembled together and acting with a common intent.''')

st.subheader("Dropping \"RIOTS_PER_CAPITA\" column from the above DataFrame and determining the third leading crime type:")
kerala_df = kerala_df.drop('RIOTS_PER_CAPITA', axis=1)

leading_crimes_k_list = define_leading_crime_type(kerala_df)
leading_crimes_k_dict = {years_list[i]: leading_crimes_k_list[i] for i in range(len(years_list))}
code = '''kerala_df = kerala_df.drop('RIOTS_PER_CAPITA', axis=1)

leading_crimes_k_list = define_leading_crime_type(kerala_df)
leading_crimes_k_dict = {years_list[i]: leading_crimes_k_list[i] for i in range(len(years_list))}
leading_crimes_k_dict'''
st.code(code, language="python")
st.write(leading_crimes_k_list)
st.write('''Just like in Madhya Pradesh and Rajasthan, even in Kerala "Theft" is the one of the leading crime types after "Other IPC Crimes". The only difference consists in the fact that in this case, this type of crime ranks third (so not second), in terms of the number of cases.''')

st.subheader("Plotting Kerala's GDP and leading crime types progress:")
code = '''visualise_gdp_and_leading_crimes(most_affected_state = most_affected_states[2], leading_crime_types = ['OTHER IPC CRIMES_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA', 'RIOTS_PER_CAPITA', 'THEFT_PER_CAPITA'])'''
st.code(code, language="python")
is_clicked3 = st.button("Show the plots", key = "k_plots")
if is_clicked3:
    visualise_gdp_and_leading_crimes(most_affected_state = most_affected_states[2], leading_crime_types = ['OTHER IPC CRIMES_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA', 'RIOTS_PER_CAPITA', 'THEFT_PER_CAPITA'])
st.write('''The situation appears similar to the case of Madhya Pradesh and Rajasthan. Kerala has seen an even greater increase in GDP in the 11-year period from 2001 to 2011. It is about a 5-fold increase in its value, which is excellent news. As for the dominant crimes in this state, each of them has experienced a small reduction.''')

st.write("Lastly, I will focus on the fourth most affected Indian state, Tamil Nadu.")

st.subheader("Extracting all the information about this state from \"most_affected_states_df\" and storing it into the new Pandas DataFrame:")
tamil_nadu_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[3]]
code = "tamil_nadu_df = most_affected_states_df[most_affected_states_df['STATE'] == most_affected_states[3]]"
st.code(code, language="python")

st.subheader("Determining the first leading crime type in Tamil Nadu:")
leading_crimes_tn_list = define_leading_crime_type(tamil_nadu_df)
leading_crimes_tn_dict = {years_list[i]: leading_crimes_tn_list[i] for i in range(len(years_list))}
code = '''leading_crimes_tn_list = define_leading_crime_type(tamil_nadu_df)
leading_crimes_tn_dict = {years_list[i]: leading_crimes_tn_list[i] for i in range(len(years_list))}
leading_crimes_tn_dict'''
st.write(leading_crimes_tn_dict)
st.write('''Just like in case of Madhya Pradesh and Rajasthan, even in Tamil Nadu the first leading type after "Other IPC Crimes" is "HURT/GREVIOUS HURT".''')

st.subheader("Dropping \"HURT/GREVIOUS HURT_PER_CAPITA\" column from the above DataFrame and determining the second leading crime type:")
tamil_nadu_df = tamil_nadu_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)

leading_crimes_tn_list = define_leading_crime_type(tamil_nadu_df)
leading_crimes_tn_dict = {years_list[i]: leading_crimes_tn_list[i] for i in range(len(years_list))}
code = '''tamil_nadu_df = tamil_nadu_df.drop('HURT/GREVIOUS HURT_PER_CAPITA', axis=1)

leading_crimes_tn_list = define_leading_crime_type(tamil_nadu_df)
leading_crimes_tn_dict = {years_list[i]: leading_crimes_tn_list[i] for i in range(len(years_list))}
leading_crimes_tn_dict'''
st.code(code, language="python")
st.write(leading_crimes_tn_dict)
st.write('''Again we have the same situation compared to the case of Madhya Pradesh and Rajasthan. THEFT represents the second most dominant crime in Tamil Nadu, after "Other IPC Crimes".''')

st.subheader("Dropping \"THEFT_PER_CAPITA\" column from the above DataFrame and determining the third leading crime type:")
tamil_nadu_df = tamil_nadu_df.drop('THEFT_PER_CAPITA', axis=1)

leading_crimes_tn_list = define_leading_crime_type(tamil_nadu_df)
leading_crimes_tn_dict = {years_list[i]: leading_crimes_tn_list[i] for i in range(len(years_list))}
code = '''tamil_nadu_df = tamil_nadu_df.drop('THEFT_PER_CAPITA', axis=1)

leading_crimes_tn_list = define_leading_crime_type(tamil_nadu_df)
leading_crimes_tn_dict = {years_list[i]: leading_crimes_tn_list[i] for i in range(len(years_list))}
leading_crimes_tn_dict'''
st.code(code, language="python")
st.write(leading_crimes_tn_dict)
st.write('''Just like in Madhya Pradesh and Rajasthan, even in Tamil Nadu "Other Theft" is the third leading crime type after "Other IPC Crimes".''')

st.subheader("Visualising Tamil Nadu's GDP and leading crime types progress:")
code = "visualise_gdp_and_leading_crimes(most_affected_state = most_affected_states[3], leading_crime_types = ['OTHER IPC CRIMES_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA', 'THEFT_PER_CAPITA', 'OTHER THEFT_PER_CAPITA'])"
st.code(code, language="python")
is_clicked4 = st.button("Show the plots", key = "tn_plots")
if is_clicked4:
    visualise_gdp_and_leading_crimes(most_affected_state = most_affected_states[3], leading_crime_types = ['OTHER IPC CRIMES_PER_CAPITA', 'HURT/GREVIOUS HURT_PER_CAPITA', 'THEFT_PER_CAPITA', 'OTHER THEFT_PER_CAPITA'])
st.write('''The situation appears similar to the case of Kerala. Even Tamil Nadu has seen a great increase in GDP in the 11-year period from 2001 to 2011. It is about a 5-fold increase in its value, which again is excellent news. As for the dominant crimes in this state, even in this case each of them has experienced a small reduction.''')
st.write('''All in all, analysing the 4 most affected Indian states and the progress of their GDP and the 4 leading crime types in each of them, proves a negative correlation between Crime and GDP.''')

st.header("3. Analysing Crime and Illiteracy")

st.subheader("Importing preprocessed csv files containing data about indian crime and education, as Pandas DataFrames:")
education_dataset =  pd.read_csv('./datasets folder/preprocessed_datasets/education_dataset.csv')
crime_education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_and_education_merged_dataset.csv")
crime_dataset_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/per_capita_crime_dataset_with_gdp_literacy_rate.csv")
code = '''education_dataset =  pd.read_csv('./datasets folder/preprocessed_datasets/education_dataset.csv')
crime_education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_and_education_merged_dataset.csv")
crime_dataset_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/per_capita_crime_dataset_with_gdp_literacy_rate.csv")'''
st.code(code, language="python")

st.subheader("Plotting literacy rate for all Indian states in 2001:")
temp_df = education_dataset[(education_dataset["YEAR"] == 2001) & (education_dataset["DEMOGRAPHIC PARTICULARS"] == "Educational Standard - Illiterate")]

crime = crime_dataset_per_capita[['literacy_rate_percentage', 'STATE', 'Literacy_Rate_per_capita']][crime_dataset_per_capita['YEAR'] == 2001]

test_df = pd.merge(temp_df, crime, left_on=['STATE/UT'], right_on=['STATE'])
test_df = test_df.drop('STATE', axis=1)
code = '''temp_df = education_dataset[(education_dataset["YEAR"] == 2001) & (education_dataset["DEMOGRAPHIC PARTICULARS"] == "Educational Standard - Illiterate")]

crime = crime_dataset_per_capita[['literacy_rate_percentage', 'STATE', 'Literacy_Rate_per_capita']][crime_dataset_per_capita['YEAR'] == 2001]

test_df = pd.merge(temp_df, crime, left_on=['STATE/UT'], right_on=['STATE'])
test_df = test_df.drop('STATE', axis=1)
fig = make_subplots(1, 1)

fig.add_trace(go.Bar(
                        x = test_df['STATE/UT'].unique(), 
                        y = test_df['literacy_rate_percentage']
                    ), row=1, col=1)

fig.update_layout(width = 1080, showlegend=False)
fig.show()'''
st.code(code, language="python")
is_clicked5 = st.button("Show the plot", "literacy_2001")
if is_clicked5:
    fig = make_subplots(1, 1)

    fig.add_trace(go.Bar(
                        x = test_df['STATE/UT'].unique(), 
                        y = test_df['literacy_rate_percentage']
                    ), row=1, col=1)

    fig.update_layout(width = 1080, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
st.write('''We see that Bihar, Jharkhand, Uttar Pradesh, Rajasthan, Madhya Pradesh are the states with a lower literacy rate compared to most other states that is below 60%. Therefore, I will later plot a graph of literacy and the total number of illiterate convicts during the years 2001 - 2011 for these states.''')

st.subheader("Normalising the data using MinMaxScaler(), as the literacy rate and crimes per capita are on different scales:")
temp_df = education_dataset[(education_dataset["DEMOGRAPHIC PARTICULARS"] == "Educational Standard - Illiterate")]
temp_df = temp_df.sort_values('STATE/UT')
crime = crime_dataset_per_capita[['literacy_rate_percentage', 'STATE', 'Literacy_Rate_per_capita', 'YEAR']]
test_df = pd.merge(temp_df, crime, left_on=['STATE/UT', 'YEAR'], right_on=['STATE', 'YEAR'])
test_df = test_df.drop('STATE', axis=1)
cols = ['Male Convicts', 'Female Convicts', 'Total Convicts',
       'Male Under trial', 'Female Under trial', 'Total Under trial',
       'Male Detenues', 'Female Detenues', 'Total Detenues', 'Male Others',
       'Female Others', 'Total Others', 'Total Male', 'Total Female',
       'Grand Total', 'literacy_rate_percentage']
scaler = MinMaxScaler()
edu = scaler.fit_transform(test_df[cols].values)
test_df[cols] = edu
code = '''temp_df = education_dataset[(education_dataset["DEMOGRAPHIC PARTICULARS"] == "Educational Standard - Illiterate")]
temp_df = temp_df.sort_values('STATE/UT')
crime = crime_dataset_per_capita[['literacy_rate_percentage', 'STATE', 'Literacy_Rate_per_capita', 'YEAR']]
test_df = pd.merge(temp_df, crime, left_on=['STATE/UT', 'YEAR'], right_on=['STATE', 'YEAR'])
test_df = test_df.drop('STATE', axis=1)
cols = ['Male Convicts', 'Female Convicts', 'Total Convicts',
       'Male Under trial', 'Female Under trial', 'Total Under trial',
       'Male Detenues', 'Female Detenues', 'Total Detenues', 'Male Others',
       'Female Others', 'Total Others', 'Total Male', 'Total Female',
       'Grand Total', 'literacy_rate_percentage']
scaler = MinMaxScaler()
edu = scaler.fit_transform(test_df[cols].values)
test_df[cols] = edu'''
st.code(code, language="python")
st.write("Data still maintains the normal distribution as before.")

st.subheader("Plotting the progress of literacy rate and illiterate convicts rate from 2001 to 2011 for the indian states with the lowest literacy rate:")
states = ["Bihar", "Jharkhand", "Uttar Pradesh", "Rajasthan", "Madhya Pradesh"]
df = test_df[test_df['STATE/UT'].isin(states)]
code = '''states = ["Bihar", "Jharkhand", "Uttar Pradesh", "Rajasthan", "Madhya Pradesh"]

df = test_df[test_df['STATE/UT'].isin(states)]

fig = make_subplots(5, 1,
    subplot_titles=(f"Literacy and Total number of illiterate convicts in {states[0]}",
    f"Literacy and Total number of illiterate convicts in {states[1]}",
    f"Literacy and Total number of illiterate convicts in {states[2]}",
    f"Literacy and Total number of illiterate convicts in {states[3]}",
    f"Literacy and Total number of illiterate convicts in {states[4]}")
)


for i, state in enumerate(states):
    i +=1
    y = df[df['STATE/UT'] == state].sort_values('YEAR')
    
    fig.add_trace(go.Scatter(
                            x = y['YEAR'].unique(), 
                            y = y['Grand Total'],
                            name=" illiterate convicts"
                        ), row=i, col=1)

    fig.add_trace(go.Scatter(
                                x = y['YEAR'].unique(),
                                y = y['literacy_rate_percentage'],
                                name="Literacy"
                                
                            ),row=i, col=1)

fig.update_layout(width = 700, height = 1000, showlegend=True)
fig.show()'''
st.code(code, language="python")
is_clicked6 = st.button("Show plots", "low_literacy_states")
if is_clicked6:
    fig = make_subplots(5, 1,
    subplot_titles=(f"Literacy and Total number of illiterate convicts in {states[0]}",
    f"Literacy and Total number of illiterate convicts in {states[1]}",
    f"Literacy and Total number of illiterate convicts in {states[2]}",
    f"Literacy and Total number of illiterate convicts in {states[3]}",
    f"Literacy and Total number of illiterate convicts in {states[4]}")
    )


    for i, state in enumerate(states):
        i +=1
        y = df[df['STATE/UT'] == state].sort_values('YEAR')
    
        fig.add_trace(go.Scatter(
                            x = y['YEAR'].unique(), 
                            y = y['Grand Total'],
                            name=" illiterate convicts"
                        ), row=i, col=1)

        fig.add_trace(go.Scatter(
                                x = y['YEAR'].unique(),
                                y = y['literacy_rate_percentage'],
                                name="Literacy"
                                
                            ),row=i, col=1)

    fig.update_layout(width = 700, height = 1000, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

st.write('''The graph shows a clear indication of how the increase in literacy has lead to the decrease in overall number of illiterate convicts in all states. Especially when we see Bihar, Jharkhand and Madhya Pradesh who started with a very low literacy rate and highest number of convicts. The state has shown significant progress throughout the years.''')

st.subheader("Plotting the same features for the states with the highest literacy rate(Goa, Kerala, Mizoram, Puducherry and Tamil Nadu):")
states = ["Goa", "Kerala", "Mizoram", "Puducherry", "Tamil Nadu"]
df = test_df[test_df['STATE/UT'].isin(states)]

code = '''states = ["Goa", "Kerala", "Mizoram", "Puducherry", "Tamil Nadu"]

df = test_df[test_df['STATE/UT'].isin(states)]

fig = make_subplots(len(states), 1,
    subplot_titles=(f"Literacy and Totoal number of illiterate convicts in {states[0]}",
    f"Literacy and Total number of illiterate convicts in {states[1]}",
    f"Literacy and Total number of illiterate convicts in {states[2]}",
    f"Literacy and Total number of illiterate convicts in {states[3]}",
    f"Literacy and Total number of illiterate convicts in {states[4]}")
)


for i, state in enumerate(states):
    i +=1
    y = df[df['STATE/UT'] == state].sort_values('YEAR')
    
    fig.add_trace(go.Scatter(
                            x = y['YEAR'].unique(), 
                            y = y['Grand Total'],
                            name=" illeterate convicts"
                        ), row=i, col=1)

    fig.add_trace(go.Scatter(
                                x = y['YEAR'].unique(),
                                y = y['literacy_rate_percentage'],
                                name="Literacy"
                                
                            ),row=i, col=1)

fig.update_layout(width = 700, height = 1000, showlegend=True)
fig.show()'''
st.code(code, language="python")
is_clicked7 = st.button("Show the plots", key = "high_literacy_states")
if is_clicked7:
    fig = make_subplots(len(states), 1,
        subplot_titles=(f"Literacy and Totoal number of illiterate convicts in {states[0]}",
            f"Literacy and Total number of illiterate convicts in {states[1]}",
            f"Literacy and Total number of illiterate convicts in {states[2]}",
            f"Literacy and Total number of illiterate convicts in {states[3]}",
            f"Literacy and Total number of illiterate convicts in {states[4]}")
    )

    for i, state in enumerate(states):
        i +=1
        y = df[df['STATE/UT'] == state].sort_values('YEAR')
    
        fig.add_trace(go.Scatter(
                            x = y['YEAR'].unique(), 
                            y = y['Grand Total'],
                            name=" illeterate convicts"
                        ), row=i, col=1)

        fig.add_trace(go.Scatter(
                                x = y['YEAR'].unique(),
                                y = y['literacy_rate_percentage'],
                                name="Literacy"
                                
                            ),row=i, col=1)

    fig.update_layout(width = 700, height = 1000, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

st.write('''It is important to note that literacy rates in India have generally been improving over time, but there are still significant disparities between different states and regions. In addition, literacy rates can vary significantly within a state, and there may be pockets of low literacy even in states with relatively high overall literacy rates. Improving literacy rates in India is a key priority for the government, and various initiatives have been implemented to increase access to education and improve the quality of education in the country. Definitely the increase in overall literacy of the country would lead to lower crimes committed.''')

st.header("4. Analysing crime against women.")

st.subheader("Importing the required csv files for this part of analysis:")
code = '''crime_education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_and_education_merged_dataset.csv")
crime_dataset_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/per_capita_crime_dataset_with_gdp_literacy_rate.csv")'''
st.code(code, language="python")
crime_education_dataset = pd.read_csv("./datasets folder/preprocessed_datasets/crime_and_education_merged_dataset.csv")
crime_dataset_per_capita = pd.read_csv("./datasets folder/preprocessed_datasets/per_capita_crime_dataset_with_gdp_literacy_rate.csv")

st.subheader('''Crime against women is a significant issue in India, and the country has a high rate of violence against women, including sexual assault, domestic violence, and human trafficking.
There are a number of factors that contribute to the high rate of crime against women in India, including:''')

st.write('''- Patriarchy and gender inequality: India has a long history of patriarchy and gender inequality, and these cultural beliefs can contribute to a lack of respect for women's rights and a tolerance for violence against women.''')
st.write('''- Weak laws and enforcement: India's laws regarding violence against women are often weak and poorly enforced, which can make it difficult to hold perpetrators accountable for their actions.''')
st.write('''- Stigma and victim blaming: There is often a stigma attached to victims of violence, and women who report crimes against them may be subject to victim blaming and disbelief.''')
st.write('''- Lack of access to resources: Many women in India lack access to resources such as education, employment, and healthcare, which can make them more vulnerable to violence.''')

st.subheader('''Lack of access to resources: Many women in India lack access to resources such as education, employment, and healthcare, which can make them more vulnerable to violence.''')
st.write('''As I have data between the years of 2001 - 2011, I will try to find some interesting insight regarding crime against women. Below we see an interactive bar graph which shows the progression of number of rape cases booked in all the states in India. In general we see that on overall decrease in cases in all states even from the states with highest rape cases in India.''')
st.write("But is the crime really decreasing?")

st.subheader("Plotting an animated bar graph representing the progress of \"RAPE_PER_CAPITA\" from 2001 to 2011 for all indian states:")
code = '''fig = px.bar(
    crime_dataset_per_capita, 
    x="STATE", 
    y="RAPE_PER_CAPITA",
    animation_frame = "YEAR",
    barmode="relative"
)

fig.update_layout(
    height = 800,
    width = 800,
    yaxis_range=[0, 0.00007])
fig.show()'''
st.code(code, language="python")
is_clicked8 = st.button("Show the animated plot", key = "rape_progress")
if is_clicked8:
    fig = px.bar(
        crime_dataset_per_capita, 
     x="STATE", 
        y="RAPE_PER_CAPITA",
        animation_frame = "YEAR",
        barmode="relative"
    )

    fig.update_layout(
        height = 800,
        width = 800,
        yaxis_range=[0, 0.00007])
    st.plotly_chart(fig, use_container_width=True)

st.write('''It looks like literacy and educated men are more likely not to harm women which would be the most basic understanding for such type of crime. I compare the literacy rate of the states with highest crime against women and crime rate with respect to the year 2001 and 2011.''')

st.subheader("Scaling crime per capita and literacy rate values using MinMaxScaler(), to properly deal with completely different scales:")
state_list = crime_dataset_per_capita['STATE'].unique()
temp_df = crime_dataset_per_capita[crime_dataset_per_capita["STATE"].isin(state_list)]
temp_df = temp_df[["STATE", "YEAR", "RAPE_PER_CAPITA", "literacy_rate_percentage"]]
scaler = MinMaxScaler()
crime_w = scaler.fit_transform(temp_df[["RAPE_PER_CAPITA", "literacy_rate_percentage"]].values)
temp_df[["RAPE_PER_CAPITA", "literacy_rate_percentage"]] = crime_w
state_list = ["Chhattisgarh", "Madhya Pradesh", "Mizoram", "Maharashtra", "Assam", "Arunachal Pradesh"]
df = temp_df[temp_df['STATE'].isin(state_list)]
code = '''state_list = crime_dataset_per_capita['STATE'].unique()
temp_df = crime_dataset_per_capita[crime_dataset_per_capita["STATE"].isin(state_list)]
temp_df = temp_df[["STATE", "YEAR", "RAPE_PER_CAPITA", "literacy_rate_percentage"]]
scaler = MinMaxScaler()
crime_w = scaler.fit_transform(temp_df[["RAPE_PER_CAPITA", "literacy_rate_percentage"]].values)
temp_df[["RAPE_PER_CAPITA", "literacy_rate_percentage"]] = crime_w
state_list = ["Chhattisgarh", "Madhya Pradesh", "Mizoram", "Maharashtra", "Assam", "Arunachal Pradesh"]
df = temp_df[temp_df['STATE'].isin(state_list)]'''
st.code(code, language="python")

st.subheader("Plotting rape per capita and literacy rate in 2001 and 2011 for 6 Indian states with high cases of rape:")
code = '''fig = make_subplots(1, 2,
    specs=[[{},{}]],
    subplot_titles=(f"Rape(bar graph) & literacy rate(line graph) 2001",
                    "Rape(bar graph) & literacy rate(line graph) 2011"))

fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2001]
                    ), row=1, col=1)
fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2001]
                        ), row=1, col=1)


fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2011]
                    ), row=1, col=2)
fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2011] 
                        ), row=1, col=2)

fig.update_yaxes(range=[0, 1.2])
fig.update_layout(width = 1000, showlegend=False)
fig.show()'''
st.code(code, language="python")
is_clicked9 = st.button("Show the plots", key = "rape_and_literacy")
if is_clicked9:
    fig = make_subplots(1, 2,
        specs=[[{},{}]],
        subplot_titles=(f"Rape(bar graph) & literacy rate(line graph) 2001",
                    "Rape(bar graph) & literacy rate(line graph) 2011"))

    fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2001]
                    ), row=1, col=1)
    fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2001]
                        ), row=1, col=1)


    fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2011]
                    ), row=1, col=2)
    fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2011] 
                        ), row=1, col=2)

    fig.update_yaxes(range=[0, 1.2])
    fig.update_layout(width = 1000, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.write('''The graph of 2001 shows us that there was very low literacy rate(line graph) below 40% and the rapes committed were high(bar graph). Coming to the year 2011 when I compare both of them we can see there is an increase in the literacy rate in all of these states but some have made huge progress for example we see Chhattisgarh, Assam, Madhya Pradesh who had very low literacy rate after 10 years has progressed alot. With Chhattisgarh with reduction of 20%, Madhya Pradesh around 16%. Arunachal Pradesh with the lowest literacy with these states shows a huge difference of 15%. Mizoram is known for its problem with crime against women due to high trafficking of women with the increase in literacy there is a reduction of alomst 30% but still stays highest due to the underworld human trafficking taking place. Maharashtra on the other hand had a high literacy rate already and hence has low rape cases from the beginning.''')

st.subheader("Plotting rape per capita and literacy rate in 2001 and 2011 for 6 Indian states with low cases of rape:")
code = '''state_list = ["Gujarat", "Karnataka", "Tamil Nadu", "Puducherry"]

df = temp_df[temp_df['STATE'].isin(state_list)]

fig = make_subplots(1, 2,
    specs=[[{},{}]],
    subplot_titles=(f"Rape(bar graph) & literacy rate(line graph) 2001",
                    "Rape(bar graph) & literacy rate(line graph) 2011"))

fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2001]
                    ), row=1, col=1)
fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2001]
                        ), row=1, col=1)


fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2011]
                    ), row=1, col=2)
fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2011] 
                        ), row=1, col=2)

fig.update_yaxes(range=[0, 1.2])
fig.update_layout(width = 1000, showlegend=False)
fig.show()'''
st.code(code, language="python")
state_list = ["Gujarat", "Karnataka", "Tamil Nadu", "Puducherry"]
df = temp_df[temp_df['STATE'].isin(state_list)]
is_clicked10 = st.button("Show plots", key = "low_rape_plots")
if is_clicked10:
    fig = make_subplots(1, 2,
    specs=[[{},{}]],
    subplot_titles=(f"Rape(bar graph) & literacy rate(line graph) 2001",
                    "Rape(bar graph) & literacy rate(line graph) 2011"))

    fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2001]
                    ), row=1, col=1)
    fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2001]
                        ), row=1, col=1)


    fig.add_trace(go.Bar(
                        x = df['STATE'].unique(), 
                        y = df['RAPE_PER_CAPITA'][df['YEAR'] == 2011]
                    ), row=1, col=2)
    fig.add_trace(go.Scatter(
                            x = df['STATE'].unique(),
                            y = df['literacy_rate_percentage'][df['YEAR'] == 2011] 
                        ), row=1, col=2)

    fig.update_yaxes(range=[0, 1.2])
    fig.update_layout(width = 1000, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.write('''In these graphs already we see that these particular states already have a literacy rate above 40% in the year 2001. Which is high compartively to the states seen before. In 2011 we see that the cases are already reduced drastically with the increase in literacy.''')
st.write("Due to scaling Gujarat and Karnataka have been reduced to close to 0 and hence not seen in the graph.")
st.markdown("""---""")
st.write('''There is a relationship between literacy and rape in India, as higher literacy rates are generally associated with lower rates of sexual violence. According to data from the National Family Health Survey (NFHS), states with higher literacy rates in India tend to have lower rates of sexual violence against women. For example, states with literacy rates above the national average of 73% tend to have lower rates of rape and other forms of sexual violence, while states with literacy rates below the national average tend to have higher rates of sexual violence. There are several reasons why literacy may be associated with lower rates of sexual violence in India. Higher literacy rates may be accompanied by increased gender equality, as education can empower women and give them more control over their lives. Literacy may also lead to increased awareness of women's rights and the negative impacts of sexual violence, which can discourage individuals from committing these crimes. Hence studying these graphs also give a negative co-realtion between them. Giving proper education to states with lower literacy can help benefit women and reduce the amount of crime committed towards.''')