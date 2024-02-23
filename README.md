# NHL-Edge-API
The goal of this project is to build a dataset and api for the new NHL edge site

# How to Use:
> .\env\scripts\activate 

> uvicorn main:app --reload


# Process of data collection:
1. Get all team data (primarily the team tricode)

2. Get all player data by team

    ^ This is the easiest way of getting all player data via the official NHL api ^

3. Use Get Edge Data script to gather and combine all player data AND their nhl edge data
    - This includes Goalie data