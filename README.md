# FantasyScraper

Grabs NFL fixture data by week.

### Data Structure

In the script's current state, it produces a JSON file in the format:

```
{
   "<Week #>":[
      {
         "<Fixture Id>": {
            "player_data": {
               "<player_id>": {...},
               "<player_id>": {...},
               ...
            },
            "fixture_data": {
               "home_stat": {...},
               "vis_stat": {...}
            },
            "pbp_data": [
               {
                  "details": "...",
                  "players": [
                     ("<player_id>", "<player_name>"),
                     ("<player_id>", "<player_name>"),
                     ...
                  ]
               }
            ]
         }
      },
      {
         "<Fixture Id>": {
            "player_data": {
               "<player_id>": {...},
               "<player_id>": {...},
               ...
            },
            "fixture_data": {
               "home_stat": {...},
               "vis_stat": {...}
            },
            "pbp_data": [
               {
                  "details": "...",
                  "players": [
                     ("<player_id>", "<player_name>"),
                     ("<player_id>", "<player_name>"),
                     ...
                  ]
               }
            ]
         }
      },
      ...
   ]
}
```

Functionality can easily be expanded to process multiple weeks or years at a time.

### Notice

Data sourced from [Pro Footall Reference](https://www.pro-football-reference.com/).

Do not violate any of PFR's [Data Use](https://www.sports-reference.com/bot-traffic.html) and [Bot Traffic](https://www.sports-reference.com/bot-traffic.html) policies. Any violations will possibly result in a site ban.

Due to necessary `sleep()` functions embedded in the code, this script will be too slow to be called from within another program and should be run independently.
