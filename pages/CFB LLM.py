import google.generativeai as genai
import os
import streamlit as st
import cfbd as cfb #rememebr to write this to there file (so they know to download)
from cfbd.rest import ApiException
import requests



genai.configure(api_key=os.environ['API_KEY'])
print(os.environ['API_KEY'])



google_api_key = os.getenv("API_KEY")


genai.configure(api_key=google_api_key)


configuration = cfb.Configuration()
configuration.api_key["Authorization"] = (
    os.getenv("CFB_API_KEY")
)
configuration.api_key_prefix["Authorization"] = "Bearer"

def GetWinnerWithIDForAI(gameID, year):
    if gameID == -99:
        winner = "No one"
        prompt = ("Invent me two imaginary football teams and have them play each other and tell me about the game. "
        "At the end of the output, print \"You listed two teams that didn't play that year. So I made two up!\"")
        return prompt
    year = int(year)
    try:
        api_instance = cfb.GamesApi(cfb.ApiClient(configuration)).get_games(
            id = gameID,
            year = year,
            season_type="regular",
        )
    except ApiException as err:
        print("Exception when calling Api: %s\n" % err)
    if not api_instance:
        return -99
    for items in api_instance:
        if not items.home_points or not items.away_points:
            winner = "No one"
            prompt = ("Invent me two imaginary football teams and have them play each other and tell me about the game. "
            "At the end of the output, print \"The api timed out so I made up an imaginary game!\"")
            return prompt
        if (items.home_points > items.away_points):
            winner = items.home_team
            loser = items.away_team
            winnerPts = items.home_points
            loserPts = items.away_points
        else:
            winner = items.away_team
            loser = items.home_team
            winnerPts = items.away_points
            loserPts = items.home_points
        winnerStr = f"{winner}: {winnerPts} | {loser}: {loserPts}"
        prompt = (f"Must proide me  an overview of the football game between {winner} and {loser} in the year {year} where {winner} won and {loser} lost!"
        "Look up the game using ESPN and google and give me a summary. ")

        return prompt 



def GetID(inputTeam_1, inputTeam_2, inputYear):
    inputYear= int(inputYear)
    gameID = -99
    if inputYear < 1900 or inputYear > 2040:
        return -99
    try:
        api_instance = cfb.GamesApi(cfb.ApiClient(configuration)).get_games(
            team=inputTeam_1,
            year=inputYear,
            season_type="regular",
        )
    except ApiException as err:
        print("Exception when calling Api: %s\n" % err)
    if not api_instance:
        return -99
    for items in api_instance:
        if (items.home_team == inputTeam_1 or items.away_team == inputTeam_1):
            if items.home_team == inputTeam_2 or items.away_team == inputTeam_2:
                gameID = items.id
    return gameID

def GetPressConference(gameID, year):
    dictList_1 = {}
    dictList_2 = {}
    if gameID == -99:
        winner = "No one"
        prompt = ("Tell me about a postgame press conference between two imaginary football teams and have them play each other and tell me about the game. "
        "At the end of the output, print \"You listed two teams that didn't play that year. So I made two up!\"")
        return prompt
    year = int(year)
    try:
        api_instance = cfb.GamesApi(cfb.ApiClient(configuration)).get_team_game_stats(
            game_id = gameID,
            year = year,
            season_type="regular",
        )
        for items in api_instance:
            team_1 = items.teams[0]
            dictList_1['points'] = team_1.points
            team_2 = items.teams[1]
            dictList_2['points'] = team_2.points
            team1_name = team_1.school
            team2_name = team_2.school

            for items in team_1.stats:

                dictList_1[items.category] = items.stat

            for items in team_2.stats:
                dictList_2[items.category] = items.stat

    except ApiException as err:
        print("Exception when calling Api: %s\n" % err)
    prompt = (f"Write a postgame press conference using the football stats given. Team: {team1_name} stats are as follows: Turnovers={dictList_1['turnovers']}, "
              f"Total Yards={dictList_1['totalYards']}",
              f"Points Scored={dictList_1['points']}",
              f"Passing Yards={dictList_1['netPassingYards']}",
              f"Rushing Yards={dictList_1['rushingYards']}",
              f"Team: {team2_name} stats are as follows: Turnovers={dictList_2['turnovers']}",
              f"Total Yards={dictList_2['totalYards']}",
              f"Points Scored={dictList_2['points']}",
              f"Passing Yards={dictList_2['netPassingYards']}",
              f"Rushing Yards={dictList_2['rushingYards']}")
 

    return prompt



team1 = st.text_input("Enter a Team:")
team2= st.text_input("Enter another Team:")
year_played = st.number_input("What year did they play?: ", min_value=2004, max_value=2024, value=2004)

model = genai.GenerativeModel("gemini-1.5-flash")


gameID = GetID(team1,team2,year_played)
prompt = GetPressConference(gameID, year_played)
context = GetPressConference(gameID,year_played)

try:
    response = model.generate_content(prompt)
except:
    response = "LLM had an issue."
st.write(response.text)
#for items in response:
 #   print(items)







    





def rolesForStreamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role


if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


st.title("CFB AI CHatbot")


for message in st.session_state.chat_session.history:
    with st.chat_message(rolesForStreamlit(message.role)):
        st.markdown(message.parts[0].text)


user_message = st.chat_input("What would you like to know?")
if user_message:
    st.chat_message("user").markdown(user_message)
    response = st.session_state.chat_session.send_message(user_message)


    with st.chat_message("asistant"):
        st.markdown(response.text)






