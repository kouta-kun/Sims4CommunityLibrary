"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Any, Tuple, Union, List

from sims.outfits.outfit_enums import OutfitCategory, BodyTypeFlag, BodyType
from sims.sim_info import SimInfo
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.common_appearance_modifier_type import CommonAppearanceModifierType
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from buffs.appearance_modifier.appearance_modifier import AppearanceModifier
else:
    # noinspection PyMissingOrEmptyDocstring
    class AppearanceModifier:
        # noinspection PyMissingOrEmptyDocstring
        class BaseAppearanceModification:
            # noinspection PyPep8Naming
            @classmethod
            def TunableFactory(cls) -> Any:
                pass


class CommonAttachCASPartsAppearanceModifier(AppearanceModifier.BaseAppearanceModification, HasLog):
    """CommonAttachCASPartsAppearanceModifier()
    
    Attach CAS Parts to a Sim by utilizing Appearance Modifiers.
    
    .. note:: Appearance Modifiers will apply to any outfit a Sim wears, when switching outfits ALL of their outfits will APPEAR to have the attached CAS Part. However, appearance modifiers are only temporary.

    .. note:: To see an example of this appearance modifier in action, run the command `s4clib_testing.toggle_example_appearance_modifier_buff` in the console. (The Sim will have bare feet)

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        class CommonExampleApplyBareFeetAppearanceModifier(AppearanceModifier):

            class CommonAttachBareFeetModifier(CommonAttachCASPartsAppearanceModifier):
                # noinspection PyMissingOrEmptyDocstring
                @property
                def mod_identity(self) -> CommonModIdentity:
                    return ModInfo.get_identity()

                # noinspection PyMissingOrEmptyDocstring
                @property
                def log_identifier(self) -> str:
                    return 'common_example_apply_bare_feet'

                def _get_cas_part_ids(
                    self,
                    source_sim_info: SimInfo,
                    modified_sim_info: SimInfo,
                    original_unmodified_sim_info: SimInfo,
                    random_seed: int
                ) -> Tuple[int]:
                    # Human
                    # yfShoes_Nude
                    adult_human_female_bare_feet_id = 6543
                    # ymShoes_Nude
                    adult_human_male_bare_feet_id = 6563
                    # cuShoes_Nude
                    child_human_bare_feet_id = 22018
                    # puShoes_Nude
                    toddler_human_bare_feet_id = 132818

                    # Dog
                    # adShoes_Nude
                    adult_large_dog_bare_feet_id = 125251
                    # alShoes_Nude
                    adult_small_dog_bare_feet_id = 148839
                    # cdShoes_Nude
                    child_dog_bare_feet_id = 158046

                    # Cat
                    # acShoes_Nude
                    adult_cat_bare_feet_id = 150367
                    # ccShoes_Nude
                    child_cat_bare_feet_id = 164111

                    # Fox
                    adult_fox_bare_feet_id = 277492

                    bare_feet_cas_part_id = None
                    if CommonAgeUtils.is_teen_adult_or_elder(original_unmodified_sim_info):
                        if CommonSpeciesUtils.is_human(original_unmodified_sim_info):
                            if CommonGenderUtils.is_female(original_unmodified_sim_info):
                                bare_feet_cas_part_id = adult_human_female_bare_feet_id
                            elif CommonGenderUtils.is_male(original_unmodified_sim_info):
                                bare_feet_cas_part_id = adult_human_male_bare_feet_id
                        elif CommonSpeciesUtils.is_large_dog(original_unmodified_sim_info):
                            bare_feet_cas_part_id = adult_large_dog_bare_feet_id
                        elif CommonSpeciesUtils.is_small_dog(original_unmodified_sim_info):
                            bare_feet_cas_part_id = adult_small_dog_bare_feet_id
                        elif CommonSpeciesUtils.is_cat(original_unmodified_sim_info):
                            bare_feet_cas_part_id = adult_cat_bare_feet_id
                        elif CommonSpeciesUtils.is_fox(original_unmodified_sim_info):
                            bare_feet_cas_part_id = adult_fox_bare_feet_id
                    elif CommonAgeUtils.is_child(original_unmodified_sim_info):
                        if CommonSpeciesUtils.is_human(original_unmodified_sim_info):
                            bare_feet_cas_part_id = child_human_bare_feet_id
                        elif CommonSpeciesUtils.is_large_dog(original_unmodified_sim_info) or CommonSpeciesUtils.is_small_dog(original_unmodified_sim_info):
                            bare_feet_cas_part_id = child_dog_bare_feet_id
                        elif CommonSpeciesUtils.is_cat(original_unmodified_sim_info):
                            bare_feet_cas_part_id = child_cat_bare_feet_id
                    elif CommonAgeUtils.is_toddler(original_unmodified_sim_info):
                        bare_feet_cas_part_id = toddler_human_bare_feet_id

                    if bare_feet_cas_part_id is None:
                        return tuple()

                    return bare_feet_cas_part_id,

            # We override the original "appearance_modifiers" to so we can insert our custom appearance modifier.
            FACTORY_TUNABLES = {
                'appearance_modifiers': TunableList(
                    description='            The specific appearance modifiers to use for this buff.            ',
                    tunable=TunableList(
                        description='                A tunable list of weighted modifiers. When applying modifiers                one of the modifiers in this list will be applied. The weight                will be used to run a weighted random selection.                ',
                        tunable=TunableTuple(
                            description='                    A Modifier to apply and weight for the weighted random                     selection.                    ',
                            modifier=TunableVariant(
                                custom_bare_feet_modifier=CommonAttachBareFeetModifier.TunableFactory(),
                            ),
                            weight=TunableMultiplier.TunableFactory(
                                description='                        A weight with testable multipliers that is used to                         determine how likely this entry is to be picked when                         selecting randomly.                        '
                            )
                        )
                    )
                )
            }


        # We use this buff in a Buff tuning and then apply the buff to the Sim.
        class CommonExampleApplyBareFeetBuff(Buff):

            # We override the original "appearance_modifier" to so we can insert our custom appearance modifier.
            INSTANCE_TUNABLES = {
                'appearance_modifier': OptionalTunable(CommonExampleApplyBareFeetAppearanceModifier.TunableFactory()),
            }


    :Example Tuning:

    Buff Tuning:

    .. highlight:: xml
    .. code-block:: xml

        <?xml version="1.0" encoding="utf-8"?>
        <I c="CommonExampleApplyBareFeetBuff" i="buff" m="sims4communitylib.examples.common_example_apply_bare_feet_buff" n="S4CL_Example_Buff_ApplyBareFeet" s="16461769487103204847">
          <V n="appearance_modifier" t="enabled">
            <U n="enabled">
              <L n="appearance_modifiers">
                <L>
                  <U>
                    <V n="modifier" t="custom_bare_feet_modifier">
                      <U n="custom_bare_feet_modifier" />
                    </V>
                  </U>
                </L>
              </L>
            </U>
          </V>
          <T n="audio_sting_on_add" p="OnAddSound">39b2aa4a:00000000:8af8b916cf64c646</T>
          <T n="audio_sting_on_remove" p="OnRemoveSound">39b2aa4a:00000000:3bf33216a25546ea</T>
          <T n="icon" p="Icon">2f7d0004:00000000:30f0846c783606f9</T>
          <T n="visible">False</T>
        </I>

    Sim Data:

    .. highlight:: xml
    .. code-block:: xml

        <?xml version="1.0" encoding="utf-8"?>
        <SimData version="0x00000101" u="0x0000001F">
          <Instances>
            <I name="S4CL_Example_Buff_ApplyBareFeet" schema="Buff" type="Object">
              <T name="audio_sting_on_add">FD04E3BE-001407EC-8AF8B916CF64C646</T>
              <T name="audio_sting_on_remove">FD04E3BE-001407EC-3BF33216A25546EA</T>
              <T name="buff_description">0x00000000</T>
              <T name="buff_name">0x00000000</T>
              <T name="icon">00B2D882-00000000-30F0846C783606F9</T>
              <T name="mood_type">0</T>
              <T name="mood_weight">0</T>
              <T name="timeout_string">0x00000000</T>
              <T name="timeout_string_no_next_buff">0x00000000</T>
              <T name="ui_sort_order">1</T>
            </I>
          </Instances>
          <Schemas>
            <Schema name="Buff" schema_hash="0x0D045687">
              <Columns>
                <Column name="audio_sting_on_add" type="ResourceKey" flags="0x00000000" />
                <Column name="audio_sting_on_remove" type="ResourceKey" flags="0x00000000" />
                <Column name="buff_description" type="LocalizationKey" flags="0x00000000" />
                <Column name="buff_name" type="LocalizationKey" flags="0x00000000" />
                <Column name="icon" type="ResourceKey" flags="0x00000000" />
                <Column name="mood_type" type="TableSetReference" flags="0x00000000" />
                <Column name="mood_weight" type="Int32" flags="0x00000000" />
                <Column name="timeout_string" type="LocalizationKey" flags="0x00000000" />
                <Column name="timeout_string_no_next_buff" type="LocalizationKey" flags="0x00000000" />
                <Column name="ui_sort_order" type="Int32" flags="0x00000000" />
              </Columns>
            </Schema>
          </Schemas>
        </SimData>

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def modify_sim_info(self, source_sim_info: SimInfo, modified_sim_info: SimInfo, random_seed: int) -> BodyTypeFlag:
        try:
            if not hasattr(modified_sim_info, 'original_unmodified_sim_info'):
                self.log.format_with_message('No Based On Sim Info found, using current source Sim!', original_unmodified_sim=source_sim_info)
                original_unmodified_sim_info = source_sim_info
            else:
                original_unmodified_sim_info = getattr(modified_sim_info, 'original_unmodified_sim_info')
                self.log.format_with_message('Based On Sim Info found, using Based On Sim Info!', original_unmodified_sim=original_unmodified_sim_info)

            self.log.format_with_message('Copying the base attributes of Sim to the modified Sim.', sim=source_sim_info, original_unmodified_sim=original_unmodified_sim_info, modified_sim=modified_sim_info)
            from sims.sim_info_base_wrapper import SimInfoBaseWrapper
            SimInfoBaseWrapper.copy_base_attributes(modified_sim_info, source_sim_info)
            SimInfoBaseWrapper.copy_physical_attributes(modified_sim_info, source_sim_info)
            modified_sim_info.skin_tone = source_sim_info._base.skin_tone
            modified_sim_info.skin_tone_val_shift = source_sim_info._base.skin_tone_val_shift
            modified_sim_info.load_outfits(source_sim_info.save_outfits())

            cas_part_ids = self._get_cas_part_ids(source_sim_info, modified_sim_info, original_unmodified_sim_info, random_seed)
            body_types = self._apply_cas_part_ids(cas_part_ids, source_sim_info, modified_sim_info, original_unmodified_sim_info, random_seed)

            if not body_types:
                self.log.format_with_message('Failed to apply CAS Parts! No body parts', sim=original_unmodified_sim_info, cas_part_ids=cas_part_ids)
                return BodyTypeFlag.NONE
            self.log.format_with_message('Done applying CAS Parts!', sim=original_unmodified_sim_info, cas_part_ids=cas_part_ids)
            return BodyTypeFlag.make_body_type_flag(*body_types)
        except Exception as ex:
            self.log.error('An error occurred while applying selected part.', exception=ex)
        return BodyTypeFlag.NONE

    def _get_cas_part_ids(self, source_sim_info: SimInfo, modified_sim_info: SimInfo, original_unmodified_sim_info: SimInfo, random_seed: int) -> Tuple[int]:
        """_get_cas_part_ids(source_sim_info, modified_sim_info, original_unmodified_sim_info, random_seed)

        Retrieve a collection of CAS Part ids being applied to the Sim.

        :param source_sim_info: The Sim the parts are being applied to. (This Sim is replaced with "modified_sim_info" after the first appearance modifier modification)
        :type source_sim_info: SimInfo
        :param modified_sim_info: A cloned instance of "source_sim_info" that the parts are applied to. (The value of this property replaces "source_sim_info" after the first appearance modifier modification)
        :type modified_sim_info: SimInfo
        :param original_unmodified_sim_info: The original unmodified Sim, from before any modifications were made to them. This value will never be replaced and keeps the original information about the Sim, especially their Sim Id.
        :type original_unmodified_sim_info: SimInfo
        :param random_seed: The seed used to assign the appearance modifier.
        :type random_seed: int
        :return: A collection of CAS Part Identifiers that will be applied to the Sim.
        :rtype: Tuple[int]
        """
        raise NotImplementedError()

    def _apply_cas_part_ids(self, cas_part_ids: Tuple[int], source_sim_info: SimInfo, modified_sim_info: SimInfo, original_unmodified_sim_info: SimInfo, random_seed: int) -> Tuple[Union[BodyType, int]]:
        if not cas_part_ids:
            self.log.format_with_message('No CAS Parts were found to apply.', sim=original_unmodified_sim_info)
            return tuple()

        self.log.format_with_message('Applying CAS Parts with ids', sim=original_unmodified_sim_info, cas_part_ids=cas_part_ids)

        body_types: List[Union[BodyType, int]] = list()
        for cas_part_id in cas_part_ids:
            body_type = self._apply_cas_part_id(cas_part_id, source_sim_info, modified_sim_info, original_unmodified_sim_info, random_seed)
            body_types.append(body_type)
            source_sim_info = modified_sim_info
        self.log.format_with_message('Finished applying CAS Parts.', original_sim=original_unmodified_sim_info, cas_part_ids=cas_part_ids)
        return tuple(body_types)

    def _apply_cas_part_id(self, cas_part_id: int, source_sim_info: SimInfo, modified_sim_info: SimInfo, original_unmodified_sim_info: SimInfo, random_seed: int) -> Union[BodyType, int]:
        from cas.cas import set_caspart
        # Source Sim, Modified Sim, CAS Part Id, Should Toggle, Replace With Random, Update Genetics, Random Seed, Remove Conflicting
        result = set_caspart(source_sim_info._base, modified_sim_info._base, cas_part_id, False, False, False, random_seed, remove_conflicting=True)
        if result:
            self.log.format_with_message('Applied CAS part.', sim=original_unmodified_sim_info, cas_part_id=cas_part_id)
            return CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        else:
            self.log.format_with_message('Failed to apply CAS Part.', sim=original_unmodified_sim_info, cas_part_id=cas_part_id, result=result)

    @property
    def modifier_type(self) -> CommonAppearanceModifierType:
        """The type of modifier being applied."""
        return CommonAppearanceModifierType.CUSTOM

    @property
    def is_permanent_modification(self) -> bool:
        """Whether the modification is permanent or not."""
        return False

    @property
    def combinable_sorting_key(self) -> str:
        """A key used to combine this appearance modifiers with other appearance modifiers."""
        return self.__class__.__name__

    # noinspection PyUnusedLocal
    def is_compatible_with_outfit(self, outfit_category: OutfitCategory) -> bool:
        """is_compatible_with_outfit(outfit_category)

        Whether or not the appearance modifier is compatible with the specified outfit category.

        .. note:: If the appearance modifier is not compatible, then the buff that applies it will be removed.

        :param outfit_category: The outfit category being checked.
        :type outfit_category: OutfitCategory
        :return: True, if the appearance modifier is compatible with the specified outfit category. False, if not.
        :rtype: bool
        """
        return True

    def __repr__(self) -> str:
        return self.__class__.__name__


if not ON_RTD:
    from sims4.commands import Output
    from server_commands.argument_helpers import OptionalTargetParam

    @CommonConsoleCommand(ModInfo.get_identity(), 's4clib_testing.toggle_example_appearance_modifier_buff', 'Apply an example S4CL buff that will make the feet of the Sims with it bare.')
    def _s4cl_testing_apply_example_bare_feet_buff(output: Output, opt_sim: OptionalTargetParam=None):
        from server_commands.argument_helpers import get_optional_target
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, output._context))
        if sim_info is None:
            output(f'ERROR: The Sim did not exist: {opt_sim}')
            return False
        output(f'Toggling bare feet example buff on Sim {sim_info}.')
        from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
        if CommonBuffUtils.has_buff(sim_info, CommonBuffId.S4CL_EXAMPLE_APPLY_BARE_FEET):
            output(f'Removing bare feet example buff from Sim {sim_info}')
            CommonBuffUtils.remove_buff(sim_info, CommonBuffId.S4CL_EXAMPLE_APPLY_BARE_FEET)
        else:
            output(f'Adding bare feet example buff on Sim {sim_info}')
            CommonBuffUtils.add_buff(sim_info, CommonBuffId.S4CL_EXAMPLE_APPLY_BARE_FEET)
        output(f'Done toggling bare feet example buff on Sim {sim_info}')