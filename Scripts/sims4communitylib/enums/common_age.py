"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Union, Tuple

from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonAge(CommonInt):
    """Custom Age enum containing all ages, because there have been too many problems when referencing the vanilla Age in various places.

    """
    INVALID: 'CommonAge' = 0
    BABY: 'CommonAge' = 1
    TODDLER: 'CommonAge' = 2
    CHILD: 'CommonAge' = 4
    TEEN: 'CommonAge' = 8
    YOUNGADULT: 'CommonAge' = 16
    ADULT: 'CommonAge' = 32
    ELDER: 'CommonAge' = 64

    @classmethod
    def get_all(cls) -> Tuple['CommonAge']:
        """get_all()

        Retrieve a collection of all CommonAge, excluding CommonAge.INVALID.

        :return: A collection of all CommonAge, without CommonAge.INVALID.
        :rtype: Tuple[CommonAge]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonAge, ...] = tuple([value for value in cls.values if value != cls.INVALID])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonAge, excluding INVALID.

        :return: A collection of the names of all CommonAge, without INVALID.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls) -> str:
        """get_comma_separated_names_string()

        Create a string containing all names of all CommonAge values (excluding INVALID), separated by a comma.

        :return: A string containing all names of all CommonAge values (excluding INVALID), separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names())

    @staticmethod
    def get_age(sim_info: SimInfo) -> 'CommonAge':
        """get_age(sim_info)

        Retrieve the CommonAge of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonAge that represents what age a Sim is or INVALID if their age cannot be determined.
        :rtype: CommonAge
        """
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonAgeUtils.is_baby(sim_info):
            return CommonAge.BABY
        elif CommonAgeUtils.is_toddler(sim_info):
            return CommonAge.TODDLER
        elif CommonAgeUtils.is_child(sim_info):
            return CommonAge.CHILD
        elif CommonAgeUtils.is_teen(sim_info):
            return CommonAge.TEEN
        elif CommonAgeUtils.is_young_adult(sim_info):
            return CommonAge.YOUNGADULT
        elif CommonAgeUtils.is_adult(sim_info):
            return CommonAge.ADULT
        elif CommonAgeUtils.is_elder(sim_info):
            return CommonAge.ELDER
        return CommonAge.INVALID

    @staticmethod
    def convert_to_vanilla(value: 'CommonAge') -> Union[Age, None]:
        """convert_to_vanilla(value)

        Convert a CommonAge into the vanilla Age enum.

        :param value: An instance of CommonAge
        :type value: CommonAge
        :return: The specified CommonAge translated to Age or None if the value could not be translated.
        :rtype: Union[Age, None]
        """
        if value is None or value == CommonAge.INVALID:
            return None
        if isinstance(value, Age):
            return value
        age_conversion_mapping: Dict[CommonAge, Age] = {
            CommonAge.BABY: Age.BABY,
            CommonAge.TODDLER: Age.TODDLER,
            CommonAge.CHILD: Age.CHILD,
            CommonAge.TEEN: Age.TEEN,
            CommonAge.YOUNGADULT: Age.YOUNGADULT,
            CommonAge.ADULT: Age.ADULT,
            CommonAge.ELDER: Age.ELDER
        }
        return age_conversion_mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: Union[int, Age]) -> 'CommonAge':
        """convert_from_vanilla(value)

        Convert a vanilla Age to a CommonAge.

        :param value: An instance of Age
        :type value: Age
        :return: The specified Age translated to CommonAge or INVALID if the value could not be translated.
        :rtype: CommonAge
        """
        if value is None:
            return CommonAge.INVALID
        if isinstance(value, CommonAge):
            return value
        age_conversion_mapping: Dict[int, CommonAge] = {
            int(Age.BABY): CommonAge.BABY,
            int(Age.TODDLER): CommonAge.TODDLER,
            int(Age.CHILD): CommonAge.CHILD,
            int(Age.TEEN): CommonAge.TEEN,
            int(Age.YOUNGADULT): CommonAge.YOUNGADULT,
            int(Age.ADULT): CommonAge.ADULT,
            int(Age.ELDER): CommonAge.ELDER
        }
        value = int(value)
        if value not in age_conversion_mapping:
            return CommonAge.INVALID
        return age_conversion_mapping[value]

    @staticmethod
    def convert_to_localized_string_id(value: Union[int, 'CommonAge']) -> Union[int, str]:
        """convert_to_localized_string_id(value)

        Convert a CommonAge into a Localized String identifier.

        :param value: An instance of a CommonAge
        :type value: CommonAge
        :return: The specified CommonAge translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        display_name_mapping = {
            CommonAge.BABY: CommonStringId.BABY,
            CommonAge.TODDLER: CommonStringId.TODDLER,
            CommonAge.CHILD: CommonStringId.CHILD,
            CommonAge.TEEN: CommonStringId.TEEN,
            CommonAge.YOUNGADULT: CommonStringId.YOUNG_ADULT,
            CommonAge.ADULT: CommonStringId.ADULT,
            CommonAge.ELDER: CommonStringId.ELDER
        }
        if isinstance(value, int) and not isinstance(value, CommonAge):
            value = CommonAge.convert_from_vanilla(value)
        return display_name_mapping.get(value, value.name if hasattr(value, 'name') else str(value))
