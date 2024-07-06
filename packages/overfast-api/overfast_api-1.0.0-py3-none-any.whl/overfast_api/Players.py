from overfast_api.RestAdapter import RestAdapter
from overfast_api.models import PlayerSearchResult, PlayerSummary, PlayerStatSummary, PlayerCareerStats, PlayerFullData
from typing import List


class Players:
    def __init__(self):
        self.adapter = RestAdapter()

    def player_search(
            self,
            username: str,
            order_by: str = 'name:asc',
            offset: int = 0,
            limit: int = 20
    ) -> List[PlayerSearchResult]:
        """
        Function to search for all players with a given username.

        :param username: username to search for
        :param order_by: setting to change ordering of results
        :param offset: amount of results to skip
        :param limit: limit number of results to return
        :return: returns a list of all players as PlayerSearchResult objects
        """
        params = {
            'name': username,
            'order_by': order_by,
            'offset': offset,
            'limit': limit,
        }
        result = self.adapter.get(endpoint='/players', params=params)
        players = []
        if "error" not in result.data[0]:
            for player in result.data[0]['results']:
                players.append(PlayerSearchResult(player))
        return players

    def get_player_summary(self, username: str) -> PlayerSummary:
        """
        Function to get a player summary.

        :param username: full battle.net name of user in format of username-xxxx
        :return: player summary object
        """
        result = self.adapter.get(endpoint=f'/players/{username}/summary')
        return PlayerSummary(result.data[0])

    def get_player_stat_summary(self, username: str, gamemode: str = None, platform: str = None) -> PlayerStatSummary:
        """
        function to get a player stats summary, a short list of basic stats of the player

        :param username: full battle.net name of user in format of username-xxxx
        :param gamemode: gamemode of the returned results. Defaults to quickplay if none is provided
        :param platform: filter results by platform, pc or console. If none provided, all results are returned
        :return: player stats summary object
        """
        params = {}
        if gamemode:
            params['gamemode'] = gamemode
        if platform:
            params['platform'] = platform
        result = self.adapter.get(endpoint=f'/players/{username}/stats/summary', params=params)
        return PlayerStatSummary(username, result.data[0])

    def get_player_career_stats(
            self,
            username: str,
            gamemode: str = "quickplay",
            platform: str = None,
            hero: str = None,
            with_labels: bool = False
    ) -> PlayerCareerStats:
        """
        function to return detailed career stats for a player

        :param username: full battle.net name of user in format of username-xxxx
        :param gamemode: gamemode of the returned results.
        :param platform: platform for results. If none provided will give results for whatever platform the player has
        played on. If player has played on both, will default to pc.
        :param hero: filter by hero provided. "all-heroes" will return general stats
        :param with_labels: if True will return results with labels. Same as using the /{player}/stats endpoint
        :return: player career stats object
        """
        if with_labels:
            endpoint = f'/players/{username}/stats'
        else:
            endpoint = f'/players/{username}/stats/career'
        params = {"gamemode": gamemode}
        if platform:
            params['platform'] = platform
        if hero:
            params['hero'] = hero
        result = self.adapter.get(endpoint=endpoint, params=params)
        return PlayerCareerStats(username, result.data[0])

    def get_all_player_stats(self, username: str) -> PlayerFullData:
        """
        Function to return full player stats

        :param username: full battle.net name of user in format of username-xxxx
        :return: player full data object that contains a player summary, comp stats for pc and console and lists of
        hero stats for all heroes.
        """
        result = self.adapter.get(endpoint=f'/players/{username}')
        return PlayerFullData(result.data[0])
