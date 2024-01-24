import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df =pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis: Medals, Moments, and Metrics")
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfWaV0uCq_lrBexy39yUwicwz40G2LenJTdg&usqp=CAU')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    # Using Markdown with HTML styling for a blue title
    st.markdown("<h1 style='color:black;'>Top Statistics</h1>", unsafe_allow_html=True)



    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.markdown(f"<h1 style='color:blue;'>{editions}</h1>", unsafe_allow_html=True)

    with col2:
        st.subheader("Hosts")
        st.markdown(f"<h1 style='color:blue;'>{cities}</h1>", unsafe_allow_html=True)

    with col3:
        st.subheader("Sports")
        st.markdown(f"<h1 style='color:blue;'>{sports}</h1>", unsafe_allow_html=True)

    # Using HTML for custom styling
    st.markdown("<hr/>", unsafe_allow_html=True)  # horizontal line for separation

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.markdown(f"<h1 style='color:blue;'>{events}</h1>", unsafe_allow_html=True)

    with col2:
        st.subheader("Nations")
        st.markdown(f"<h1 style='color:blue;'>{nations}</h1>", unsafe_allow_html=True)
    with col3:
        st.subheader("Athletes")
        st.markdown(f"<h1 style='color:blue;'>{athletes}</h1>", unsafe_allow_html=True)

# Sending df and column name , function will return me the the df and logic of obtaining participating nations is
#     written there
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="Participating Nations")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time1(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="Participating Events")
    st.title("Events over the years")
    st.plotly_chart(fig)

    st.title("Participation of Athletes over the years in a specific Sport/as a whole")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list, key='sport')

    athlete_over_time = helper.data_over_time2(df, 'Name',selected_sport)
    fig = px.line(athlete_over_time,x="Edition", y="Athletes Over The Years")
    st.plotly_chart(fig)


    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(30, 30))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True,cmap="PiYG")
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport1 = st.selectbox('Select a Sport', sport_list,key='sport1')
    x = helper.most_successful(df, selected_sport1)
    st.table(x)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    # st.title(selected_country + " Medal Tally over the years")
    title_html = f"""
        <style>
            .title {{
                font-size: 36px;
                font-weight: bold;
                color: #FF5733; /* Change the color as needed */
                text-align: center;
                padding: 20px;
                animation: colorChange 3s infinite alternate; /* Add animation */
            }}

            @keyframes colorChange {{
                from {{
                    color: #FF5733; /* Start color */
                }}
                to {{
                    color: #33FF57; /* End color */
                }}
            }}
        </style>
        <div class="title"> Medal Tally of {selected_country} over the years</div>
    """

    # Render the styled title using st.markdown
    st.markdown(title_html, unsafe_allow_html=True)
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True,cmap='coolwarm')
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)


    st.title(f"Men Vs Women Participation Over the Years for {selected_country}")
    final = helper.country_wise_gender(df,selected_country)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    x1=[]
    name1=[]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x1.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name1.append(sport)

    fig = ff.create_distplot(x1, name1, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age wrt Sports(Silver Medalist)")
    st.plotly_chart(fig)

    x2 = []
    name2 = []
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        age_data = temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna()

        if not age_data.empty:
            x2.append(age_data.tolist())
            name2.append(sport)

    fig = ff.create_distplot(x2, name2, show_hist=False, show_rug=False)
    st.title("Distribution of Age wrt Sports(Bronze Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y= temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)