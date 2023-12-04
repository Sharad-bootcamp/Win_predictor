import streamlit as st
import pandas as pd
import pickle
import os

# Get the absolute path to the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'pipe.pkl')

# Load the pre-trained model
try:
    with open(model_path, 'rb') as file:
        pipe = pickle.load(file)
except FileNotFoundError:
    st.error(f"File not found: {model_path}. Make sure the file exists at the specified path.")

# Declaring the teams
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

# Declaring the venues where the matches are going to take place
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur', 'Chennai',
          'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur',
          'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

# Setting up the app's title
st.title('IPL Win Predictor')

# Setting up the layout with two columns
col1, col2 = st.columns(2)

# Creating a dropdown selector for the batting team
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))

# Creating a dropdown selector for the bowling team
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

# Creating a dropdown selector for the city where the match is being played
city = st.selectbox('Select the city where the match is being played', sorted(cities))

# Creating a numeric input for the target score using number_input method in streamlit
target = int(st.number_input('Target', step=1))

# Setting up the layout with three columns
col3, col4, col5 = st.columns(3)

# Creating a numeric input for the current score
with col3:
    score = int(st.number_input('Score', step=1))

# Creating a numeric input for the number of overs completed
with col4:
    overs = int(st.number_input('Overs Completed', step=1))

# Creating a numeric input for the number of wickets fallen
with col5:
    wickets = int(st.number_input('Wickets Fallen', step=1))

# Checking for different match results based on the input provided
if score > target:
    st.write(batting_team, "won the match")
    
elif score == target - 1 and overs == 20:
    st.write("Match Drawn")
    
elif wickets == 10 and score < target - 1:
    st.write(bowling_team, 'Won the match')
    
elif wickets == 10 and score == target - 1:
    st.write('Match tied')
    
elif batting_team == bowling_team:
    st.write('To proceed, please select different teams because no match can be played between the same teams')

else:
    # Checking if the input values are valid or not
    if 0 <= target <= 400 and 0 <= overs <= 20 and 0 <= wickets <= 10 and 0 <= score:

        try:
            if st.button('Predict Probability'):
                # Calculating the number of runs left for the batting team to win
                runs_left = target - score
                
                # Calculating the number of balls left
                balls_left = 120 - (overs * 6)
                
                # Calculating the number of wickets left for the batting team
                wickets_left = 10 - wickets
                
                # Calculating the current Run-Rate of the batting team
                current_run_rate = score / overs
                
                # Calculating the Required Run-Rate for the batting team to win
                required_run_rate = (runs_left * 6) / balls_left

                # Creating a pandas DataFrame containing the user inputs
                input_df = pd.DataFrame({
                    'batting_team': [batting_team],
                    'bowling_team': [bowling_team],
                    'city': [city],
                    'runs_left': [runs_left],
                    'balls_left': [balls_left],
                    'wickets_left': [wickets_left],
                    'total_runs_x': [target],
                    'cur_run_rate': [current_run_rate],
                    'req_run_rate': [required_run_rate]
                })

                # Loading the trained machine learning pipeline to make the prediction
                result = pipe.predict_proba(input_df)

                # Extracting the likelihood of loss and win
                loss_prob = result[0][0]
                win_prob = result[0][1]

                # Displaying the predicted likelihood of winning and losing in percentage
                st.header(batting_team + " - " + str(round(win_prob * 100)) + "%")
                st.header(bowling_team + " - " + str(round(loss_prob * 100)) + "%")

        # Catching ZeroDivisionError
        except ZeroDivisionError:
            st.error("Please fill all the details")

    # Displaying an error message if the input is incorrect
    else:
        st.error('There is something wrong with the input, please fill the correct details')
