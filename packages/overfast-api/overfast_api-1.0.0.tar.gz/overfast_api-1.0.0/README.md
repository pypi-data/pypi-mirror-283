## overfast-api
### Python wrapper for the Overfast API

## Features

- Access to all endpoints of the Overfast API
- Data returned as easy to use custom classes
- Ability to set optional parameters for all endpoints

## Usage

### Install via pip
```
pip install overfast-api
```
### Player Examples

Example look up summary of specific player (requires full battle.net id)

```python
from overfast_api import Players

# Create an instance of the Players class
players = Players()

# Note: replace hash mark in player name with hyphen when looking up players by id
my_summary = players.get_player_summary(username="redjordan-1382")
print(f'{my_summary.username}\n{my_summary.title}\nEndorsement Level: {my_summary.endorsement_level}')
```
Result:
```
redjordan
Hashimoto Goon
Endorsement Level: 5
```

Example search for all users with in-game username
```python
from overfast_api import Players

players = Players()

# Search for all players the in-game name "sourdough"
results = players.player_search(username="sourdough")

for player in results:
    print(f'{player.name}\tTitle: {player.title}')
```

Result:
```
SourDough#11454	Title: Demigod
SourDough#11463	Title: None
SourDough#11713	Title: Stalwart Hero
SourDough#11835	Title: Mercy's Angel
SourDough#11967	Title: None
Sourdough#11204	Title: Eldritch Nightmare
Sourdough#11216	Title: Mortal
...
```
More examples will be added soon
### Hero Examples

## Endpoint information
For information on what data the endpoints return and optional parameters available please check out the Overfast API docs
(https://overfast-api.tekrop.fr/)

## Roadmap

- Class methods to convert custom classes to different default python types i.e. dict, list etc
- Additional documentation in source code
- Example files showing more complex usage
- Option to use self-hosted or unofficial host of Overfast API

## Rate Limiting
Currently, this wrapper is hardcoded to use the official Overfast API hosted by TeKrop. As such please note that usage 
of this wrapper is limited by the rate limits set by TeKrop.

Current rate limits are 30 requests/second shared across all endpoints.


## Credits
All data provided by TeKrop's Overfast API (https://overfast-api.tekrop.fr/)
