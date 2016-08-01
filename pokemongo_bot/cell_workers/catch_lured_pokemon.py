import time

from pokemongo_bot import logger
from pokemongo_bot.constants import Constants
from pokemongo_bot.cell_workers.utils import fort_details
from pokemongo_bot.cell_workers.pokemon_catch_worker import PokemonCatchWorker
from pokemongo_bot.cell_workers.base_task import BaseTask
from utils import distance

class CatchLuredPokemon(BaseTask):
    def work(self):
        return self.get_lured_pokemon()

    def get_lured_pokemon(self):
        forts = self.get_lured_forts_in_range()

        for fort in forts[:2]:
            self.catch_pokemon({
                'encounter_id': fort['lure_info']['encounter_id'],
                'fort_id': fort['id'],
                'latitude': fort['latitude'],
                'longitude': fort['longitude']
            })

            self.bot.fort_lured_timeouts.update({ fort['id']: time.time() + 120 })

    def get_lured_forts_in_range(self):
        forts = self.bot.get_forts(order_by_distance=True)

        forts = filter(lambda x: x.get('lure_info', {}).get('encounter_id', None), forts)

        forts = filter(lambda x: x['id'] not in self.bot.fort_lured_timeouts, forts)

        in_range_forts = []

        # remove forts too far
        for fort in forts:
            distance_to_fort = distance(
                self.bot.position[0],
                self.bot.position[1],
                fort['latitude'],
                fort['longitude']
            )

            if distance_to_fort <= Constants.MAX_DISTANCE_FORT_IS_REACHABLE:
                in_range_forts.append(fort)

        return in_range_forts

    def catch_pokemon(self, pokemon):
        worker = PokemonCatchWorker(pokemon, self.bot)
        return_value = worker.work()

        return return_value
