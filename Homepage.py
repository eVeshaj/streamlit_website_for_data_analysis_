import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Advanced Project 2",
)

st.title("Analysing Indian Crime, GDP and Education, using Data Mining and Visualisation techniques.")
st.sidebar.success("Select a page above.")

st.header("Abstract")
st.write('''Crime progress and economic growth are very current topics in India. Motivated by that, I have decided to analyse 3 datasets provided by Indian Government, containing accurate information about crime rates, GDP and the level of education in different states and their progress over years. Using data mining and visualisation methods, I will identify data trends, discover the relationships between various features (crime types, GDP, number of educated people etc.) and draw the right conclusions. These represent the basic pillars of making successful predictions and developing a compelling and meaningful story, using the respective data. The main goal is to determine the correlation between crime, GDP and education, its nature per various Indian states/districts and where it is more evident with respect to state or crime type. This can provide valuable insights, supporting Indian institutions to find more efficient ways to fight crime and reach a better balance between crime, GDP and education. By using real world data, I also aim at discovering the power of interactive visualisation, using Plotly and Dash and helping other students to master their skills in them.''')

st.header("Audience")
st.markdown('''
    - Individuals and institutions (e.g. Indian police authorities) who want to know about the correlation that exists between different crime types, GDP and the level of education in various states/districts in India. They can be interested in getting valuable information for a research topic or perhaps finding more efficient ways to fight crime and discovering the right balance between different types of crime, GDP and education.
    - Individuals (mainly students) who want to learn the right tools and the most efficient ways to build professional visualizations, in our case interactive ones.
    - Individuals who want to improve their ability to differentiate between different types of visualizations and discover the right one for the respective data, and this through concrete examples.
''')

st.header("Methodology")
st.markdown('''
    1. Exploring datasets to get a clear idea of their content (number of features, their nature, range of values etc.).
    2.	Pre-processing the data (modifying the datasets or creating subsets of them) according to our project’s objectives. For this step, I will use 2 main Python libraries, Pandas and NumPy.
    3.	Building numerous interactive visualisations (histograms, scatter/line plots to show the correlation between couples of features, choropleth maps etc.) using Python libraries such as Matplotlib, Cufflinks, Plotly and Dash.
    4.	Draw the respective conclusions based on the visualisations and other informations that I can get by researching on internet (to better understand the data).
    5.	Develop a meaningful story.
''')

st.header("Introducing the crime situation in India")
st.write("According to a research conducted in 2012 by “Igarape”, a Brazilian Institution that tracks the murders across the globe, India was ranked in second place, after Brazil in the list of countries with most intentional murders – homicides.")
st.write('''India’s homicide rate is 4.5 per 100,000 people and this figure has been going down and levelling off, but it is still a bit alarming. It is still four times higher than the homicide rate in the UK.''')
st.write('''Gun-related violence in India, according to the Homicide Monitor, is concentrated in Manipur, Nagaland, Bihar, Jharkhand, Jammu and Uttar Pradesh, which together account for over 60 percent of all registered homicides involving a firearm.''')
st.write('''Despite that, India is following the old pattern of a spike in the murder rate with rapid economic growth accompanied by income and social inequality. So, this kind of explosive situation exists across India, but it’s more pronounced in smaller cities. According to the Homicide Monitor data, the most violent places in India are not mega-cities, but rather mid-sized cities of between one and three million people. Big cities like Delhi and Mumbai are not necessarily the most dangerous places. The smaller, medium-sized cities in India face the biggest challenge. And the countryside too. According to Robert Muggah, the founder and research director of Igarapé institution, these cities are outside the public gaze and unregulated urbanisation could be the reason for growing violence. He also compares that to the situation in the Latin America, which transited from rural to urban society in the space of two generations. While India according to his opinion, is going to do it probably in less than one. So, it’s the medium and small cities, which you have never heard of, that are going to have the maximum concentration of homicides.''')
st.write('''Another aspect of these cities is disproportionately large populations of unemployed and under-educated youth, which is even more alarming. With more than 50% of its population under the age of 25 and 10 million people entering the job market every year, rapid urbanization coupled with lack of opportunities makes a dangerous cocktail. “When you have young males who are uneducated and unemployed, you tend to see high rate of violence. When a certain proportion of the population is under 30, you have high propensity to violence. So, India is highly at risk.''')
st.write('''Lack of education and jobs is further accentuated by inequality, as happened in Latin America. In India, according to Igarapé, income inequality doubled between 1990 and 2010, and this has led India’s richest 10% to currently own 370 times the share of wealth that the poorest 10% hold. “It’s not extreme poverty and not even poverty at large in material sense that fuels violence. The problem is inequality.''')
st.write('''Lastly, it is worth mentioning that In India, discussion on homicides is often sparked by sensational crimes like Aarushi-Hemraj and Sheena Bora murder cases. But the media coverage and debates remain limited to the whodunit aspect of the crime. Moreover, this problem is absent from the public safety and development agendas in India.''')

st.header("Another research conducted for this topic")
st.write('''According to Statista, a German online platform for statistics, in 2021, the Indian city of Delhi ranked first with 1859 crime cases reported per 100,000 inhabitants. This was followed by the city of Surat, with over 1600 criminal cases that year.''')
st.write('''According to a post published in August 2022 by Hindustan Times, Delhi saw over 40% jump in crimes against women in 2021, most unsafe metropolitan city. Among Union Territories, this city reported the highest rate of crime against women (147.6 per cent). A 15.3% increase in crime against women has been recorded with a total of 428278 cases registered during 2021, according to National Crime Records Bureau data. The majority of cases under crime against women under the Indian Penal Code (IPC) were registered under ‘Cruelty by Husband or His Relatives’ (31.8%) followed by ‘Assault on Women with Intent to Outrage her Modesty’ (20.8%), ‘Kidnapping & Abduction of Women’ (17.6 per cent) and ‘Rape’ (7.4 per cent).''')

st.header("Consequences")
st.write("According to Wikipedia, India ranks 148 out of 170 countries in the ‘Women, Peace and Security Index 2021’.")
st.write('''Then, the World’s Safest Countries rankings produced by Berkshire Hathaway Travel Protection have tracked India’s relative safety for four years. In 2022 the country ranked 23rd for safety out of the 30 most popular countries for travellers. In the past, it has finished as low as 29th out of 30 countries and as high as 36th out of 56 in the BHTP rankings, showing some of the uncertainty American travellers have about travel to India.''')
st.subheader("To sum up, India can be a very safe destination. But it can also be unsafe.")

