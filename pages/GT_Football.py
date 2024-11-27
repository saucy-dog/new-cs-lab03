import streamlit as st
import os
import cfbd as cfb #rememebr to write this to there file (so they know to download)
from cfbd.rest import ApiException


configuration = cfb.Configuration()
configuration.api_key["Authorization"] = (
    os.getenv("CFB_API_KEY")
)
configuration.api_key_prefix["Authorization"] = "Bearer"

# uses game ID to find who won and lost as well as the score
def GetWinnerWithID(gameID, year):
    if gameID == -99:
        winner = "No one"
        winnerStr = "These two teams haven't played yet or did not play this season"
        return winner, winnerStr
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
        if not items.home_points or not items.away_points: #if current season but game has not yet happened
            winner = "No one"
            winnerStr = "These two teams haven't played yet or did not play this season"
            return winner, winnerStr

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

        return str(winner), winnerStr



#get the game ID from API to input
def GetID(inputTeam_1, inputTeam_2, inputYear):
    inputYear= int(inputYear)
    gameID = -99
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



# Show the score of each team in each year
def football(team, year_played=1990):
    st.title(team) #1st New Stremalit Methods
    image_filename = os.path.join("Team_Images/"+team.lower() + ".jpg") #Will Include 3 Images
    st.image(image_filename, use_column_width=True)
    st.header("Winner:")
    if team == "Clemson":
        gameID = GetID("Georgia Tech", "Clemson", year_played)
        winner, winStr = GetWinnerWithID(gameID, year_played)
        st.write(winStr)
        st.write(f"{winner} won! To find out more information about this game and many more try out my CFB API LLM.")
    elif team == "Georgia":
        gameID = GetID("Georgia Tech", "Georgia", year_played)
        winner, winStr = GetWinnerWithID(gameID, year_played)
        st.write(winStr)
        st.write(f"{winner} won! To find out more information about this game and many more try out my CFB API LLM.")
    elif team == "Virginia Tech":
        gameID = GetID("Georgia Tech", "Virginia Tech", year_played)
        winner, winStr = GetWinnerWithID(gameID, year_played)
        st.write(winStr)
        st.write(f"{winner} won! To find out more information about this game and many more try out my CFB API LLM.")
    elif team == "North Carolina":
        gameID = GetID("Georgia Tech", "North Carolina", year_played)
        winner, winStr = GetWinnerWithID(gameID, year_played)
        st.write(winStr)
        st.write(f"{winner} won! To find out more information about this game and many more try out my CFB API LLM.")
    elif team == "Duke":
        gameID = GetID("Georgia Tech", "Duke", year_played)
        winner, winStr = GetWinnerWithID(gameID, year_played)
        st.write(winStr)
        st.write(f"{winner} won! To find out more information about this game and many more try out my CFB API LLM.")
    
       
   
# Pick which GT Rival You Want
st.sidebar.title("GT Rivals")
team_choice = st.sidebar.radio("Select a Rival", ["Clemson", "Georgia", "Virginia Tech", "North Carolina", "Duke"])#2nd New Streamlit Method



# Input for year played
year_played = st.sidebar.number_input("What Year?", min_value=1990, value=1990)#3rd New Streamlit Method

# Display the selected recipe page with serving size and image
if team_choice == "Clemson":
    football("Clemson", year_played)
elif team_choice == "Georgia":
    football("Georgia", year_played)
elif team_choice == "Virginia Tech":
    football("Virginia Tech", year_played)
elif team_choice == "North Carolina":
    football("North Carolina", year_played)
elif team_choice == "Duke":
    football("Duke", year_played)


