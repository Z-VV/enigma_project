www.enigma-lab.com  :
 Automated Trading Software  :
 Web and desktop apps using Django and Tkinter :

After registration on the website main page,the user will be able to download the desktop application installer.
The web app then generates one week trial API token and sends it to the user via Gmail.
After installation, the Enigma app connects the Metatrader platform on the User's desk machine with the website via the provided API token.
The Trading System in  https://github.com/Z-VV/Trading_System  ,sends POST request to the API framework everytime it detects trading opportunities.
The signals are retrieved by the Enigma app and it executes them on the user's MT platform.

The website recieves PayPal IPN and handles all emails,tokens and processes automatically.
