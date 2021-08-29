"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Tuple

from sims.sim_info import SimInfo
from sims.sim_info_types import Species, SpeciesExtended
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonSpecies(CommonInt):
    """Custom Species enum containing all species (including extended species).

    """
    INVALID: 'CommonSpecies' = 0
    HUMAN: 'CommonSpecies' = 1
    SMALL_DOG: 'CommonSpecies' = 2
    LARGE_DOG: 'CommonSpecies' = 3
    CAT: 'CommonSpecies' = 4
    FOX: 'CommonSpecies' = 5

    @classmethod
    def get_all(cls) -> Tuple['CommonSpecies']:
        """get_all()

        Retrieve a collection of all CommonSpecies, excluding CommonSpecies.INVALID.

        :return: A collection of all CommonSpecies, without CommonSpecies.INVALID.
        :rtype: Tuple[CommonSpecies]
        """
        value_list: Tuple[CommonSpecies] = tuple([value for value in cls.values if value != cls.INVALID])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonSpecies, excluding CommonSpecies.INVALID.

        :return: A collection of the names of all CommonSpecies, without CommonSpecies.INVALID.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list

    @staticmethod
    def get_species(sim_info: SimInfo) -> 'CommonSpecies':
        """get_species(sim_info)

        Retrieve the CommonSpecies of a sim. Use this instead of CommonSpeciesUtils.get_species to determine a more specific species.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A species matching the Sim or CommonSpecies.INVALID if no matching species is found.
        :rtype: CommonSpecies
        """
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonSpecies.HUMAN
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonSpecies.FOX
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonSpecies.SMALL_DOG
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonSpecies.LARGE_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonSpecies.CAT
        return CommonSpecies.INVALID

    @staticmethod
    def convert_to_vanilla(species: 'CommonSpecies') -> Union[Species, None]:
        """convert_to_vanilla(species)

        Convert a CommonSpecies into the vanilla Species enum.

        :param species: An instance of a CommonSpecies
        :type species: CommonSpecies
        :return: The specified CommonSpecies translated to a Species or SpeciesExtended or None if the CommonSpecies could not be translated.
        :rtype: Union[Species, None]
        """
        if species is None or species == CommonSpecies.INVALID:
            return None
        if isinstance(species, Species):
            return species
        conversion_mapping: Dict[CommonSpecies, Species] = {
            CommonSpecies.HUMAN: Species.HUMAN,
            CommonSpecies.SMALL_DOG: SpeciesExtended.SMALLDOG if hasattr(SpeciesExtended, 'SMALLDOG') else None,
            CommonSpecies.LARGE_DOG: Species.DOG if hasattr(Species, 'DOG') else None,
            CommonSpecies.CAT: Species.CAT if hasattr(Species, 'CAT') else None,
            CommonSpecies.FOX: Species.FOX if hasattr(Species, 'FOX') else None
        }
        return conversion_mapping.get(species, None)

    @staticmethod
    def convert_to_localized_string_id(species: 'CommonSpecies') -> Union[int, str]:
        """convert_to_localized_string_id(species)

        Convert a CommonSpecies into a Localized String identifier.

        :param species: An instance of a CommonSpecies
        :type species: CommonSpecies
        :return: The specified CommonSpecies translated to a localized string identifier or the name property of the value, if no localized string id is found.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        display_name_mapping = {
            CommonSpecies.HUMAN: CommonStringId.HUMAN,
            CommonSpecies.LARGE_DOG: CommonStringId.LARGE_DOG,
            CommonSpecies.SMALL_DOG: CommonStringId.SMALL_DOG,
            CommonSpecies.CAT: CommonStringId.CAT,
            CommonSpecies.FOX: CommonStringId.FOX
        }
        return display_name_mapping.get(species, species.name)
