import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("First approach")


st.subheader("Importing the indian crime dataset as a Pandas dataframe:")
indian_crime_df = pd.read_csv('./datasets folder/dstrIPC_1.csv')
code = '''pd.read_csv('./datasets folder/dstrIPC_1.csv')
display(indian_crime_df)'''
st.code(code, language='python')
st.write(indian_crime_df)

st.subheader("Extracting data only for year 2001, calculating the total number of cases for the crime type \"Total IPC Crimes\" and adding an arbitrary value for a missing Indian state, Telangana:")
crime_dataset_2001 = indian_crime_df.loc[indian_crime_df.YEAR == 2001]
crime_dataset_2001 = crime_dataset_2001.groupby('STATE/UT')['TOTAL IPC CRIMES'].sum()
crime_dataset_2001['TELANGANA'] = 1000
code = '''crime_dataset_2001 = indian_crime_df.loc[indian_crime_df.YEAR == 2001]
crime_dataset_2001 = crime_dataset_2001.groupby('STATE/UT')['TOTAL IPC CRIMES'].sum()
crime_dataset_2001['TELANGANA'] = 1000
crime_dataset_2001'''
st.code(code, language='python')
st.write(crime_dataset_2001)

st.subheader("Extracting the coordinates for the indian map from the respective geojson file:")
india_states = json.load(open('./datasets folder/states_india.geojson', 'r'))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
code = '''india_states = json.load(open('./datasets folder/states_india.geojson', 'r'))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
state_id_map'''
st.code(code, language='python')
st.write(state_id_map)

st.subheader("Converting the Pandas Series that I created above, into a Python dictionary, in order to simply the further data preprocessing steps:")
crime_dataset_2001_dict = crime_dataset_2001.to_dict()
code = '''crime_dataset_2001_dict = crime_dataset_2001.to_dict()
crime_dataset_2001_dict'''
st.code(code, language='python')
st.write(crime_dataset_2001_dict)
st.write('''Since we need to create a Pandas Dataframe containing Indian states, respective id(according to the geojson file) 
and total number of cases for Total IPC Crimes, it's easier to perform the mapping process on two Python dictionaries.''')

st.subheader('''Definining a function which checks for Indian states that are not present in both Python dictionaries that we created above or that have different name formats:''')
def check_missing_state_names(state_id_map, crime_dict):
    if type(state_id_map) != type(list()):
        state_id_map_list = state_id_map.keys()
        crime_list = crime_dict.keys()
    else:
        state_id_map_list = state_id_map
        crime_list = crime_dict
        
    missing_states = [state for state in crime_list if state not in [state.upper() for state in state_id_map_list]]
    correct_states = [state for state in state_id_map_list if state.upper() not in [state for state in crime_list]]
    return missing_states, correct_states

missing_state_list, correct_states = check_missing_state_names(state_id_map=state_id_map, crime_dict=crime_dataset_2001_dict)
code = '''def check_missing_state_names(state_id_map, crime_dict):
    if type(state_id_map) != type(list()):
        state_id_map_list = state_id_map.keys()
        crime_list = crime_dict.keys()
    else:
        state_id_map_list = state_id_map
        crime_list = crime_dict
        
    missing_states = [state for state in crime_list if state not in [state.upper() for state in state_id_map_list]]
    correct_states = [state for state in state_id_map_list if state.upper() not in [state for state in crime_list]]
    return missing_states, correct_states

missing_state_list, correct_states = check_missing_state_names(state_id_map=state_id_map, crime_dict=crime_dataset_2001_dict)
print(missing_state_list)
print(correct_states)'''
st.code(code, language='python')
st.write(missing_state_list)
st.write(correct_states)

st.subheader("Defining a function to correct the wrong/missing state names:")
def change_state_names(missing_state_list, crime_dict, correct_states):
    for i in range(len(missing_state_list)):
        crime_dict[correct_states[i].upper()] = crime_dict[missing_state_list[i]]
        del crime_dict[missing_state_list[i]]
    return crime_dict
code = '''def change_state_names(missing_state_list, crime_dict, correct_states):
    for i in range(len(missing_state_list)):
        crime_dict[correct_states[i].upper()] = crime_dict[missing_state_list[i]]
        del crime_dict[missing_state_list[i]]
    return crime_dict'''
st.code(code, language='python')

st.subheader("Calling the function defined above:")
code = '''changed_crime_dict = change_state_names(missing_state_list=missing_state_list, crime_dict=crime_dataset_2001_dict, correct_states=correct_states)'''
st.code(code, language='python')
changed_crime_dict = change_state_names(missing_state_list=missing_state_list, crime_dict=crime_dataset_2001_dict, correct_states=correct_states)
st.write(changed_crime_dict)

st.subheader("Checking if the state names are now corrected, using the function that checks for missing/wrong state names:")
check_missing_state_names(state_id_map=state_id_map, crime_dict=changed_crime_dict)
code = '''check_missing_state_names(state_id_map=state_id_map, crime_dict=changed_crime_dict)'''
st.code(code, language='python')
st.write(check_missing_state_names(state_id_map=state_id_map, crime_dict=changed_crime_dict))
st.write('''Based on the result above(2 empty Python lists), it is quite evident there are no more Indian
state names that are missing or have the wrong name format.''')

st.subheader("Sorting the 2 Python dictionaries:")
state_id_map = dict(sorted(state_id_map.items()))
change_crime_dict = dict(sorted(changed_crime_dict.items()))
code = '''state_id_map = dict(sorted(state_id_map.items()))
change_crime_dict = dict(sorted(changed_crime_dict.items()))'''
st.code(code, language='python')

st.subheader("Creating the Pandas DataFrame, containing Indian state names, respective id and the total number of cases for \"Total IPC Crimes\" for 2001:")
total_crime_2001_dataset = pd.DataFrame({
    "id" : list(state_id_map.values()),
    "STATE/UT" : list(state_id_map.keys()),
    "TOTAL IPC CRIMES" : list(change_crime_dict.values()),
})
code = '''total_crime_2001_dataset = pd.DataFrame({
    "id" : list(state_id_map.values()),
    "STATE/UT" : list(state_id_map.keys()),
    "TOTAL IPC CRIMES" : list(change_crime_dict.values()),
})
total_crime_2001_dataset'''
st.code(code, language='python')
st.write(total_crime_2001_dataset)

st.subheader("Plotting a choropleth map using the data of the above Pandas DataFrame:")
code = '''fig = px.choropleth(
    total_crime_2001_dataset,
    locations="id",
    geojson=india_states,
    color="TOTAL IPC CRIMES",
    color_continuous_scale=[[0, 'rgb(240,240,240)'],
                      [0.05, 'rgb(13,136,198)'],
                      [0.1, 'rgb(191,247,202)'],
                      [0.20, 'rgb(4,145,32)'],
                      [1, 'rgb(227,26,28,0.5)']],
    hover_name="STATE/UT",
    hover_data=["TOTAL IPC CRIMES"],
    title="India Total Crimes per State"
)
fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(yaxis_range=[0,60000])
fig.show()'''
st.code(code, language='python')
is_clicked = st.button("Show the map", key = "map") 
if is_clicked:
    fig = px.choropleth(
        total_crime_2001_dataset,
        locations="id",
        geojson=india_states,
        color="TOTAL IPC CRIMES",
        color_continuous_scale=[[0, 'rgb(240,240,240)'],
                            [0.05, 'rgb(13,136,198)'],
                            [0.1, 'rgb(191,247,202)'],
                            [0.20, 'rgb(4,145,32)'],
                            [1, 'rgb(227,26,28,0.5)']],
        hover_name="STATE/UT",
        hover_data=["TOTAL IPC CRIMES"],
        title="India Total Crimes per State"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(yaxis_range=[0,60000])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Importing the education dataset as a Pandas DataFrame:")
indian_education_dataset = pd.read_csv('./datasets folder/Educational_standard_of_inmates.csv')
code = '''indian_education_dataset = pd.read_csv('../datasets folder/Educational_standard_of_inmates.csv')
display(indian_education_dataset)'''
st.code(code, language='python')
st.write(indian_education_dataset)

st.subheader("Selecting only \"STATE/UT\",\"YEAR\",\"DEMOGRAPHIC PARTICULARS\" and \"Male Convicts\" columns and only records/rows where \"DEMOGRAPHIC PARTICULARS\" is equal to \"Educational Standard - Illiterate\":")
education_dataset_illiterate = indian_education_dataset[['STATE/UT','YEAR','DEMOGRAPHIC PARTICULARS', 'Male Convicts']].loc[
    indian_education_dataset['DEMOGRAPHIC PARTICULARS'] == 'Educational Standard - Illiterate']
code = '''education_dataset_illiterate = indian_education_dataset[['STATE/UT','YEAR','DEMOGRAPHIC PARTICULARS', 'Male Convicts']].loc[
    indian_education_dataset['DEMOGRAPHIC PARTICULARS'] == 'Educational Standard - Illiterate']'''
st.code(code, language='python')

st.subheader("Adding arbitrary values for Telangana for the number of \"Male Convicts\" for the time period 2001-2012:")
for year in range(2001, 2013):
    new_row = pd.DataFrame([{
        'STATE/UT': 'TELANGANA', 
        'YEAR': year, 
        'DEMOGRAPHIC PARTICULARS': 'Educational Standard - Illiterate', 
        'Male Convicts': 100
    }])

education_dataset_illiterate = pd.concat([education_dataset_illiterate, new_row], ignore_index=True)
code = '''for year in range(2001,2013):
    education_dataset_illiterate = education_dataset_illiterate.append({'STATE/UT': 'TELANGANA', 'YEAR': year, 'DEMOGRAPHIC PARTICULARS':'Educational Standard - Illiterate', 'Male Convicts': 100}, ignore_index=True)
    education_dataset_illiterate'''
st.code(code, language='python')
st.write(education_dataset_illiterate)

st.subheader("Getting the state names from the education dataset:")
education_states_list = list(education_dataset_illiterate["STATE/UT"].unique())
code = '''education_states_list = list(education_dataset_illiterate["STATE/UT"].unique())
education_states_list'''
st.write(education_states_list)

st.subheader("Applying the same procedure for identifying the wrong/missing state names and the correct format:")
state_id_map_list = list(state_id_map.keys())
missing_states, correct_states = check_missing_state_names(state_id_map=state_id_map_list, crime_dict=education_states_list)
missing_states.sort()
correct_states.sort()
code = '''state_id_map_list = list(state_id_map.keys())
missing_states, correct_states = check_missing_state_names(state_id_map=state_id_map_list, crime_dict=education_states_list)
missing_states.sort()
correct_states.sort()
print(missing_states)
print(correct_states)'''
st.write(missing_states)
st.write(correct_states)

st.subheader("Substituting the wrong/missing state names with the correct versions")
for i in range(len(missing_states)):
    education_dataset_illiterate['STATE/UT'] = education_dataset_illiterate['STATE/UT'].replace(missing_states[i],correct_states[i].upper())
code = '''for i in range(len(missing_states)):
    education_dataset_illiterate['STATE/UT'] = education_dataset_illiterate['STATE/UT'].replace(missing_states[i],correct_states[i].upper())
'''
st.code(code, language='python')

st.subheader("Checking again for missing/wrong state names:")
check_missing_state_names(state_id_map=state_id_map_list, crime_dict=list(education_dataset_illiterate['STATE/UT'].unique()))
code = '''check_missing_state_names(state_id_map=state_id_map_list, crime_dict=list(education_dataset_illiterate['STATE/UT'].unique()))'''
st.code(code, language='python')
st.write(check_missing_state_names(state_id_map=state_id_map_list, crime_dict=list(education_dataset_illiterate['STATE/UT'].unique())))
st.write("Based on the result above(2 empty python lists), the issue is solved.")

st.subheader("Getting again the state names from the education dataset(the correct versions now) and sorting the respective Python list:")
states_list = list(education_dataset_illiterate['STATE/UT'].unique())
states_list.sort()
code = '''states_list = list(education_dataset_illiterate['STATE/UT'].unique())
states_list.sort()
states_list'''
st.code(code, language = 'python')
st.write(states_list)

st.subheader("Adding the id information to the \"education_dataset_illiterate\" dataset and displaying its final version:")
states_dict = {}
sorted_state_id_map = sorted_dict = dict(sorted(state_id_map.items()))
for upper_case_state, correct_state in zip(states_list, list(sorted_state_id_map.keys())):
    states_dict[upper_case_state] = state_id_map[correct_state]

education_dataset_illiterate['id'] = education_dataset_illiterate['STATE/UT'].map(states_dict)
code = '''states_dict = {}
sorted_state_id_map = sorted_dict = dict(sorted(state_id_map.items()))
for upper_case_state, correct_state in zip(states_list, list(sorted_state_id_map.keys())):
    states_dict[upper_case_state] = state_id_map[correct_state]

education_dataset_illiterate['id'] = education_dataset_illiterate['STATE/UT'].map(states_dict)
education_dataset_illiterate'''
st.code(code, language='python')
st.write(education_dataset_illiterate)

st.subheader("Plotting an animated choropleth map, demonstrating the progress of \"Male Convicts\" for each Indian state, from 2001 to 2012:")
code = '''fig = px.choropleth(
    education_dataset_illiterate,
    locations="id",
    geojson=india_states,
    color="Male Convicts",
    hover_name="STATE/UT",
    hover_data=["Male Convicts"],
    title="India's number of male convicts per State/Ut",
    animation_frame="YEAR"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()'''
st.code(code, language="python")
st.write("It takes up to 3 minutes to show the plot, since animated plots require some time to build.")
is_clicked2 = st.button("Show the map", key = "animated_map") 
if is_clicked2:
    fig = px.choropleth(
        education_dataset_illiterate,
        locations="id",
        geojson=india_states,
        color="Male Convicts",
        hover_name="STATE/UT",
        hover_data=["Male Convicts"],
        title="India's number of male convicts per State/Ut",
        animation_frame="YEAR"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Working on the GDP dataset:")
gdp_dataset = pd.read_csv('./datasets folder/Districtwise_GDP_and_growth_rate_based_at_current_price_2004-05_AndhraPradesh_1.csv')
code = '''gdp_dataset = pd.read_csv('../datasets folder/Districtwise_GDP_and_growth_rate_based_at_current_price_2004-05_AndhraPradesh_1.csv')
gdp_dataset'''
st.code(code, language="python")
st.write(gdp_dataset)
st.write("As we can see from the above Pandas DataFrame, GDP dataset contains data only for the state of Andhra Pradesh.")

st.subheader("Extracting only information about gdp since the above dataset contains data also for Growth Rate:")
gdp_dataset = gdp_dataset.loc[gdp_dataset['Description'] == 'GDP (in Rs. Cr.)']
code = '''gdp_dataset = gdp_dataset.loc[gdp_dataset['Description'] == 'GDP (in Rs. Cr.)']
gdp_dataset'''
st.code(code, language="python")
st.write(gdp_dataset)

st.subheader("Extracting crime data only for Andhra Pradesh and the time period from 2004-2012, due to the same limitation of the GDP dataset:")
crime_dataset_AP = indian_crime_df.loc[(indian_crime_df['STATE/UT'] == "ANDHRA PRADESH")]
crime_dataset_AP = crime_dataset_AP[crime_dataset_AP['YEAR'].isin([2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012])]
code = '''crime_dataset_AP = indian_crime_df.loc[(indian_crime_df['STATE/UT'] == "ANDHRA PRADESH")]
crime_dataset_AP = crime_dataset_AP[crime_dataset_AP['YEAR'].isin([2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012])]'''
st.code(code, language="python")
st.write(crime_dataset_AP)

st.subheader("Focusing only 2 Andhra Pradesh districts, called Chittoor and Visakhapatnam and therefore creating 2 new dataframes:")
crime_dataset_chittoor = crime_dataset_AP.loc[crime_dataset_AP['DISTRICT'] == 'CHITTOOR']
crime_dataset_visakhapatnam = crime_dataset_AP.loc[crime_dataset_AP['DISTRICT'] == 'VISAKHAPATNAM']
code = '''crime_dataset_chittoor = crime_dataset_AP.loc[crime_dataset_AP['DISTRICT'] == 'CHITTOOR']
crime_dataset_visakhapatnam = crime_dataset_AP.loc[crime_dataset_AP['DISTRICT'] == 'VISAKHAPATNAM']'''
st.code(code, language="python")
st.write("Chittoor crime dataset:")
st.write(crime_dataset_chittoor)
st.write("Visakhapatnam crime dataset:")
st.write(crime_dataset_visakhapatnam)

st.subheader("Adding the GDP information to the Chittor crime dataset:")
chittoor_gdp = gdp_dataset['Chittoor'].values
crime_dataset_chittoor['GDP'] = chittoor_gdp
code = '''chittoor_gdp = gdp_dataset['Chittoor'].values
crime_dataset_chittoor['GDP'] = chittoor_gdp
crime_dataset_chittoor'''
st.code(code, language="python")
st.write(crime_dataset_chittoor)

st.subheader("Adding the GDP information to the Visakhapatnam crime dataset:")
visakhapatnam_gdp = gdp_dataset['Visakapatnam'].values
crime_dataset_visakhapatnam['GDP'] = visakhapatnam_gdp
code = '''visakhapatnam_gdp = gdp_dataset['Visakapatnam'].values
crime_dataset_visakhapatnam['GDP'] = visakhapatnam_gdp
crime_dataset_visakhapatnam'''
st.code(code, language="python")
st.write(crime_dataset_visakhapatnam)

st.subheader("Plotting the progress of all crime types versus GDP of Chittoor:")
list_of_crimes =[
    'MURDER', 'ATTEMPT TO MURDER',
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
       'CAUSING DEATH BY NEGLIGENCE', 'OTHER IPC CRIMES', 'TOTAL IPC CRIMES',
       'GDP'
]
code = '''fig = px.line(crime_dataset_chittoor, x="GDP", y=list_of_crimes, title="Crime type vs GDP for Chittoor",
              hover_data=["YEAR"], markers=True)
# Making y_axis scale unchangeable
fig.update_layout(yaxis_range=[0,7800])
fig.show()'''
st.code(code, language="python")
is_clicked3 = st.button("Show plot", key = "chittor_progress")
if is_clicked3:
    fig = px.line(crime_dataset_chittoor, x="GDP", y=list_of_crimes, title="Crime type vs GDP for Chittoor",
              hover_data=["YEAR"], markers=True)
    # Making y_axis scale unchangeable
    fig.update_layout(yaxis_range=[0,7800])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Plotting the progress of all crime types versus GDP of Visakhapatnam:")
code = '''fig = px.line(crime_dataset_visakhapatnam, x="GDP", y=list_of_crimes, title="Crime type vs GDP for Visakhapatnam", hover_data=["YEAR"], markers=True)

# Making y_axis scale unchangeable
fig.update_layout(yaxis_range=[0,7300])

fig.show()'''
st.code(code, language="python")
is_clicked4 = st.button("Show plot", key = "visakhapatnam_progress")
if is_clicked4:
    fig = px.line(crime_dataset_visakhapatnam, x="GDP", y=list_of_crimes, title="Crime type vs GDP for Visakhapatnam", hover_data=["YEAR"], markers=True)
    #Making y_axis scale unchangeable
    fig.update_layout(yaxis_range=[0,7300])
    st.plotly_chart(fig, use_container_width=True)




