import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("Second approach")

st.subheader("Selecting only columns representing crime types from the Indian Crime Dataset:")
indian_crime_df = pd.read_csv('./datasets folder/dstrIPC_1.csv')
crime_types_df = indian_crime_df[indian_crime_df.columns[3:len(indian_crime_df.columns)-1]]
code = '''indian_crime_df = pd.read_csv('../datasets folder/dstrIPC_1.csv')
crime_types_df = indian_crime_df[indian_crime_df.columns[3:len(indian_crime_df.columns)-1]]
display(indian_crime_df)'''
st.code(code, language="python")
st.write(crime_types_df)

st.subheader("Calculating the total number of cases for each crime type for the entire time period 2001-2011 and showing the 6 leading crime types:")
most_common_crime_types_df = crime_types_df.sum().sort_values(ascending=False).head(6)
code = '''most_common_crime_types_df = crime_types_df.sum().sort_values(ascending=False).head(6)
most_common_crime_types_df'''
st.code(code, language="python")
st.write(most_common_crime_types_df)
st.write("As we can see from the above Pandas Series, 6 most common crimes in India are: Other IPC crimes, Theft, Hurt/Grevious Hurt, Other Theft, Auto theft and Burglary.")

st.subheader("Determining the most affected indian states from these 6 leading crime types and displaying the result as a Pandas DataFrame:")
required_columns = list(most_common_crime_types_df.keys())
required_columns.insert(0, "STATE/UT")

most_common_crimes_df = indian_crime_df[required_columns]

leading_crime_types = required_columns[1:]
most_affected_states = []
total_cases_per_state = []

for i in range(1, len(required_columns)):
    temp_crime_types_df = most_common_crimes_df.groupby('STATE/UT')[required_columns[i]].sum().sort_values(ascending=False)
    most_affected_states.append(temp_crime_types_df.keys()[0]) 
    total_cases_per_state.append(temp_crime_types_df[0])
    
most_affected_states_per_crime = {
    "Crime type": leading_crime_types,
    "Most affected state": most_affected_states,
    "Total number of cases": total_cases_per_state
}
code = '''most_common_crimes_df = indian_crime_df[required_columns]
most_common_crimes_df

most_common_crimes_df = indian_crime_df[required_columns]
most_common_crimes_df

leading_crime_types = required_columns[1:]
most_affected_states = []
total_cases_per_state = []

for i in range(1, len(required_columns)):
    temp_crime_types_df = most_common_crimes_df.groupby('STATE/UT')[required_columns[i]].sum().sort_values(ascending=False)
    most_affected_states.append(temp_crime_types_df.keys()[0]) 
    total_cases_per_state.append(temp_crime_types_df[0])
    
most_affected_states_per_crime = {
    "Crime type": leading_crime_types,
    "Most affected state": most_affected_states,
    "Total number of cases": total_cases_per_state
}

pd.DataFrame(most_affected_states_per_crime)'''
st.code(code, language="python")
st.write(pd.DataFrame(most_affected_states_per_crime))

st.subheader("Visualising the progress over the years for the most common crime types in the respective Indian states:")
is_clicked1 = st.button("Show the plots:")
if is_clicked1:
    for i in range(len(leading_crime_types)):
        # Creating the dataset containing the progress over the years for each crime type and the most affected state
        respective_state_crime_df = indian_crime_df.loc[indian_crime_df["STATE/UT"] == most_affected_states[i]]
        respective_state_and_crime_df = respective_state_crime_df[["YEAR", leading_crime_types[i]]]
        respective_state_and_crime_df = respective_state_and_crime_df.groupby("YEAR")[leading_crime_types[i]].sum()
        respective_state_and_crime_df = pd.DataFrame({
            "YEAR" : list(respective_state_and_crime_df.keys()),
            "NUMBER OF CASES PER YEAR" : list(respective_state_and_crime_df.values)
        })
    
        # Visualising the respective dataset
        fig = px.line(respective_state_and_crime_df, x="YEAR", y="NUMBER OF CASES PER YEAR",
                title="{} in {}".format(leading_crime_types[i], most_affected_states[i]),
                hover_data=["NUMBER OF CASES PER YEAR"], markers=True)

        st.plotly_chart(fig, use_container_width=True)

st.write('''The reasons behind such progresses could be, for example, the large number of illiterate people, low GDP, large population or other motivations.''')

st.subheader('''One problem that we have is that GDP dataset contains data only for ANDHRA PRADESH and not
the other most affected Indian states for each of the leading crime types. Therefore, 
I will focus only on this state, which suffers the most from "HURT/GREVIOUS HURT".''')

st.subheader("Plotting the GDP progress for all the districts of Andhra Pradesh, from 2004 to 2012:")
code = '''gdp_dataset = pd.read_csv('./datasets folder/Districtwise_GDP_and_growth_rate_based_at_current_price_2004-05_AndhraPradesh_1.csv')

andhra_pradesh_districts = list(gdp_dataset.columns)[2:]

fig = px.line(gdp_dataset, x="Year", y=andhra_pradesh_districts, title="GDP progress in Andhra Pradesh",
              markers=True)

# Making y_axis scale unchangeable
fig.update_layout(yaxis_range=[0,60000])

fig.show()
'''
st.code(code, language="python")
is_clicked2 = st.button("Show the plot", key = "ap_districts_gdp")
gdp_dataset = pd.read_csv('./datasets folder/Districtwise_GDP_and_growth_rate_based_at_current_price_2004-05_AndhraPradesh_1.csv')
if is_clicked2:
    andhra_pradesh_districts = list(gdp_dataset.columns)[2:]

    fig = px.line(gdp_dataset, x="Year", y=andhra_pradesh_districts, title="GDP progress in Andhra Pradesh",
              markers=True)
    # Making y_axis scale unchangeable
    fig.update_layout(yaxis_range=[0,60000])
    st.plotly_chart(fig, use_container_width=True)

st.write("For districts such as Adilabad, Vizianagaram, Srikakulam, Nizambad etc. GDP increases very slowly. Therefore these districts might be the most affected ones in Andhra Pradesh by Hurt/Grevious Hurt.")

st.subheader("Analysing the crime situation only in Andhra Pradesh to determine the most affected districts and probably explain this using the GDP progress in those areas:")
andhra_pradesh_crime_df = pd.read_csv('./datasets folder/gdp_crime_dataset_ap.csv')
code = '''andhra_pradesh_crime_df = pd.read_csv('./datasets folder/gdp_crime_dataset_ap.csv')
fig = px.line(andhra_pradesh_crime_df, x="GDP", y="HURT/GREVIOUS HURT", color="DISTRICT", 
              title="Progress of \"HURT/GREVIOUS HURT\" vs \"GDP\" for each district in Andhra Pradesh",
              hover_name="DISTRICT",
              hover_data=["YEAR", "HURT/GREVIOUS HURT", "GDP"],
              markers=True)

# Making y_axis scale unchangeable
fig.update_layout(yaxis_range=[0,5300])

st.plotly_chart(fig.show, use_container_width=True)'''
st.code(code, language="python")
is_clicked3 = st.button("Show the plot", key = "ap_districts_hurt")
if is_clicked3:
    fig = px.line(andhra_pradesh_crime_df, x="GDP", y="HURT/GREVIOUS HURT", color="DISTRICT", 
                title="Progress of \"HURT/GREVIOUS HURT\" vs \"GDP\" for each district in Andhra Pradesh",
                hover_name="DISTRICT",
                hover_data=["YEAR", "HURT/GREVIOUS HURT", "GDP"],
                markers=True)

    # Making y_axis scale unchangeable
    fig.update_layout(yaxis_range=[0,5300])

    st.plotly_chart(fig, use_container_width=True)

st.write("In this plot it is worth focusing on districts such as Guntur, Hyderabad city, Visakhapatnam and Vizianagaram.")

