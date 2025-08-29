# assignments
Building an comprehensive cricket analytics dashboard that integrates live data from the Cricbuzz API with a SQL database to create an interactive web application

# Setup
# Create project directory
mkdir cricbuzz-livestats
cd cricbuzz-livestats

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install streamlit pandas requests python-dotenv plotly seaborn matplotlib

# Create environment file
touch .env
Add these to the env file
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
# Edit .env and add your RapidAPI key
# Get your API key from: https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/

# Start the Streamlit app
streamlit run main.py
