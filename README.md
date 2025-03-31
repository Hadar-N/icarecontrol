# iCareControl

iCareControl is a python program that functions as a remote for the [iCare](https://github.com/Hadar-N/icare) system. It has a Flask-based front end and communicates with the iCare installation using the [iCareComm](https://github.com/Hadar-N/icare-comm) private package.

The project is developed under the supervision of National Tsing Hua University.

## Structure

The program has 3 pages following the game process:
1. `gamestart.html` - Allows choosing game mode and level required to initialize the game
2. `gameprocess.html` - Displayed during the game itself, presenting words as they are received, allowing vocabulary option selection and provides controls to pause or stop the game
3. `gameend.html` - Appears as the game finishes, displaying the game results
- All pages extend the `base.html` page, responsible for importing the relevant style and helper files and implements page redirection based on socket actions
- `GameState.js` and `GameHelpers.js` include relevant data and functions to support the functionality of the main 3 pages

Additionally important logic can be found in:
- `main.py` - The entry point for the game, sets up the Flask app and MQTT client
- `gameroutes.py` - Defines all web page routes, ensuring each page is loaded with the necessary information (consts, etc)
- `adminroutes.py` - Handles backend logic accessed via HTTP calls for data communication, returning JSON-parsable strings instead of web pages

## Software Requirements

The application requires usage of the following packages:
- *python-dotenv* - loads environment variables from a .env file, which acts as the project’s configuration file
- *Flask* - Creates the web application and manages page rendering
- *WTForms* - Designs and validates the gamestart form
- *Flask-SocketIO* - Handles real-time communication of MQTT messages to the web pages
- *[iCareComm](https://github.com/Hadar-N/icare-comm)* - a private package storing required constants, structures and responsible for managing the MQTT client

## Required Config

The programs requires a .env file to store environment-specific settings. This file serves as a configuration file, listing essential parameters for game setup.

The relevant information expected in the file:

```bash
SECRET_KEY=XXX                  # used for wtforms validations
ENV=pc                          # ENV can be pi or pc

# MQTT connection information
HOST=XXX
PORT=XXX
USERNAME=XXX
PASSWORD=XXX
```

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)