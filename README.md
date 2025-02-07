# iCareControl

iCareControl is a python program working as a remote for the [iCare](https://github.com/Hadar-N/icare) system. It has a Front-End run by Flask and it communicates with the board running iCare using MQTT protocol.

The project is developed under the supervision of National Tsing Hua University.

## Structure

The program has 3 pages allowing the status change of :
- **gamestart.html** - allows level-choosing prior to beginning the game.
  - *Note: the game currently does not support different levels, instead this is a preparation for the future.*
  - Enables game start
- **gameprocess.html** - the window displayed during the game itself, presents words as they are received from the iCarePi game/data topic.
  - Provides controls for game pause or stop
- **gameend.html** - appears as the game finishes to present the game stats.

Additionally important logic can be found in:
- **MQTTSingle.py** - a singleton managing the MQTT connection to promise a single connection at all times.
- **main.py** - manages all the routes accessible by the program.

## Required Config

The programs uses a .env file specific to the environment and acts as a config file, required for a smooth run of the program.

The relevant information expected in the file:

```bash
# used for wtforms validations
SECRET_KEY=XXX

# MQTT connection information
HOST=XXX
PORT=XXX
USERNAME=XXX
PASSWORD=XXX
``` 

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)