import streamlit as st
import info1
import pandas as pd

#About me
def about_me_section():
    st.header("About Me")
    st.image(info1.profile_picture, width = 200 )
    st.write(info1.about_me)
    st.write('---')
about_me_section()

#Sidebar Links
def links_section():
    #st.sidebar.header("Links")
    #st.sidebar.text("Connect with me on LinkedIn")
    #linkedin_link= f'<a href="{info.my_linkedin_url}"><img src="{info.linkedin_image_url}" aly="LinkedIn" width = "75" height ="75"></a>'
    #st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
    st.sidebar.text("Email me!")
    email_html = f'<a href="mailto:{info1.my_email_address}"><img src="{info1.email_image_url}" alt = "Email" width ="75" height ="75"></a>'
    st.sidebar.markdown(email_html, unsafe_allow_html=True)
links_section()
    
#Education
def education_section(education_data, course_data):
    st.header("Education")
    st.subheader(f"**{education_data['Institution']}**") #asterics are to make the text bold
    st.write(f"**Degree:** {education_data['Degree']}")
    st.write(f"**Graduation Date:** {education_data['Graduation Date']}")
    st.write(f"**GPA:** {education_data['GPA']}")
    st.write("**Relevant Coursework:**")
    coursework = pd.DataFrame(course_data)
    st.dataframe(coursework, column_config={
        "code": "Course Code",
        "names": "Course Names",
        "semester_taken": "Semester Taken",
        "skills": "What I Learned"},
        hide_index=True, #If you change to False it will add an index to the table
        )
    st.write("---")

education_section(info1.education_data, info1.course_data)

#Professional Experience
def experience_section(experience_data):
    st.header("Professional Experience")
    for job_title, (job_description, image) in experience_data.items():
        expander = st.expander(f"{job_title}") #expanders are the tabs that when pressed expand to show more info
        expander.image(image, width=250)
        for bullet in job_description:
            expander.write(bullet)
    st.write("---")
experience_section(info1.experience_data)

#Projects
def project_section(projects_data):
    st.header("Projects")
    for project_name, project_description in projects_data.items():
        expander = st.expander(f"{project_name}")
        expander.write(project_description)
    st.write("---")
project_section(info1.projects_data)

#Skills
def skills_section(programming_data, spoken_data):
    st.header("Skills")
    st.subheader("Languages")
    for skill, percentage in programming_data.items():
        st.write(f"{skill}{info1.programming_icons.get(skill,'')}")
        st.progress(percentage)
    st.write("---")
skills_section(info1.programming_data, info1.spoken_data)

#Activities
def activities_section(leadership_data, activity_data):
    st.header("Activities")
    tab1, tab2 = st.tabs(["Leadership", "Community Service"]) #for more tabs add another tab (tab3) as well as another "tabname"
    with tab1:
        st.subheader("Leadership")
        for title, (details, image) in leadership_data.items():
            expander = st.expander(f"{title}")
            expander.image(image, width=250)
            for bullet in details:
                expander.write(bullet)
    with tab2:
        st.subheader("Community Service")
        for title, details in activity_data.items():
            expander = st.expander(f"{title}")
            for bullet in details:
                expander.write(bullet)

    st.write("---")

activities_section(info1.leadership_data, info1.activity_data)