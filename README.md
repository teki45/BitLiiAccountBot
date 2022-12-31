# BitLiiAccountBot
A Python tool that uses Selenium, SQLite3 and the TrueCaptcha + GuerrillaMail APIs to create accounts on VidLii and BitView

# Initial setup
Before using this tool, make sure you have Chrome/Chromium 108+ and Python 3+ installed with these packages:
- selenium
- webdriver-manager
- python-guerrillamail

You must also create an account at TrueCaptcha in order to process the captchas (they offer 100 free requests per day). Once you have made an account here, insert your user ID and API key into the variables "api_uid" and "api_key" respectively.

If you would like to use your own custom usernames, edit the usernames.txt and templates.txt files. The usernames text file just contains strings, seperated by newlines. The templates text file is to add a bit of variance to the usernames, where there is a pair of curly braces in the template is where the username will be inserted. You can choose to not use these and just generate a random username using ASCII characters.
