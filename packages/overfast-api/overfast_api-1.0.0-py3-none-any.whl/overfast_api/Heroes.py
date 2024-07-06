from overfast_api.RestAdapter import RestAdapter
from overfast_api.models import HeroSearchResult, Hero
from typing import Dict, List


class Heroes:
    def __init__(self):
        self.adapter = RestAdapter()

    def get_all_heroes(self, role: str = None, locale: str = 'en-us') -> List[HeroSearchResult]:
        """
        Function to get all heroes. Can be filtered by role and langauge of the results can be set by change locale

        :param role: Role to filter results by (tank, damage, support)
        :param locale: Locale to return results in. Matches locale and languages in battle.net
        :return: List of all heroes as HeroSearchResult Objects
        """
        params = dict(locale=locale)
        if role:
            params["role"] = role
        result = self.adapter.get(endpoint="heroes", params=params)
        heroes = []
        for hero in result.data:
            heroes.append(HeroSearchResult(hero))
        return heroes

    def get_hero(self, hero_key: str, locale: str = 'en-us') -> Hero:
        """
        Function to get detailed information on a specific hero.

        :param hero_key: Key of hero. Note this will differ from hero name in some cases. Refer to API docs for more info
        :param locale: Locale to return results in. Matches locale and languages in battle.net
        :return: Hero Object with all hero information
        """
        params = dict(locale=locale)
        result = self.adapter.get(endpoint=f"heroes/{hero_key}", params=params)
        return Hero(result.data[0])

    def get_roles(self) -> List[Dict]:
        """
        Function to get a list of all hero roles

        :return: list of all gamemodes represented as dicts
        """
        result = self.adapter.get(endpoint="roles")
        return result.data
