import httpx
import time
from pydantic import Field
from typing import Dict, Any
import mcp_config as cfg

def resgister_tools(mcp):
    @mcp.tool()
    async def get_race_list(
        year: int= Field(default=time.localtime().tm_year, description="The year for which the race list needs to be fetched")
        ) -> Dict[str, Any]:
        """
        get_race_list is used to fetch the list of race for a particular year.
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get( 
                    url= cfg.BASE_URL + f'f1/{year}/races/'
                )
                if response.status_code == 200:
                    json = response.json()
                    races = json["MRData"]["RaceTable"]["Races"]
                    response_races = []
                    for race in races :
                        one_race = {
                            "raceName": race.get("raceName", "Unknown"),
                            "date" : race.get("date", "Unknown"),
                            "time" : race.get("time", "Unknown")
                        }
                        response_races.append(one_race)
                    response = {
                        "race_list": response_races
                    }
                    return response
                else:
                    return {
                        "error": f"Can't fetch f1 races for {year}"
                    }
            except Exception as e:
                return {
                        "error": f"error fetching f1 races for {year}"
                    }
    @mcp.tool()
    async def get_drivers_standings(
        year: int= Field(default=time.localtime().tm_year, description="The year for which the driver standings needs to be fetched")
    ) -> Dict[str, Any]:
        """
        get_drivers_standings gives the final results , who won the drivers championship in f1 for a particular year,
        If is a happening year, it will give the current table standings
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get( 
                    url= cfg.BASE_URL + f'f1/{year}/driverstandings/'
                )
                if response.status_code == 200:
                    json = response.json()
                    standings = json["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
                    response_pos = []
                    for pos in standings :
                        one_pos = {
                            "position": pos.get("position", "Unknown"),
                            "points" : pos.get("points", "Unknown"),
                            "wins" : pos.get("wins", "Unknown"),
                            "driver" : pos["Driver"]["givenName"] + ' ' + pos["Driver"]["familyName"]
                        }
                        response_pos.append(one_pos)
                    response = {
                        # "total_races": json["MRData"]["total"],
                        "driver_standings": response_pos
                    }
                    return response
                else:
                    return {
                        "error": f"Can't fetch f1 races for {year}"
                    }
            except Exception as e:
                return {
                        "error": f"error fetching f1 races for {year}"
                    }
    @mcp.tool()
    async def get_constructor_standings(
        year: int= Field(default=time.localtime().tm_year, description="The year for which the constructor standings needs to be fetched")
    ) -> Dict[str, Any]:
        """
        get_constructor_standings gives the final results , who won the constructor championship in f1 for a particular year,
        If is a happening year, it will give the current table standings
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get( 
                    url= cfg.BASE_URL + f'f1/{year}/constructorstandings/'
                )
                if response.status_code == 200:
                    json = response.json()
                    standings = json["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
                    response_pos = []
                    for pos in standings :
                        one_pos = {
                            "position": pos.get("position", "Unknown"),
                            "points" : pos.get("points", "Unknown"),
                            "wins" : pos.get("wins", "Unknown"),
                            "name" : pos["Constructor"]["name"]
                        }
                        response_pos.append(one_pos)
                    response = {
                        # "total_races": json["MRData"]["total"],
                        "driver_standings": response_pos
                    }
                    return response
                else:
                    return {
                        "error": f"Can't fetch f1 races for {year}"
                    }
            except Exception as e:
                return {
                        "error": f"error fetching f1 races for {year}"
                    }