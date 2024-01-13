# Jamie

## Installing Modules
pip install -r requirements.txt

## Make .env file add api keys there as such:
* GOOGLE_API_KEY=your_key_here_no_quotes
* #to get key sign up to deepgram with github or email (gmail doesn't work gives errors) # and click create api key button once logged in
DEEPGRAM_API_KEY=deepgram-api-key-no-quotes 
* OPEN_AI_KEY=sk-your-open-ai-key
* AIRTABLE_ACCESS_TOKEN=ask-fellow-mentors-i-send-it-via-discord-to-some-of-them

## You can now run code like so
First load the environment variable
for windows I wrote a powershell script you can run like so:
 `.\load_envs.ps1`

In the root directory of the project run following code in terminal
`streamlit run .\streamlit_app.py`

This command will keep running , you may need to run it multiple times, if it just executes and you can type new command it didn't work, try like 10 - 20 times it will keep running eventually.It may help to comment out some of the lines in `recording_time()`:
`record_audio() up to at.create(...)` then run streamlit app and then uncomment them and refresh the page