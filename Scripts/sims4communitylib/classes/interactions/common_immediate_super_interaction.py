"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction


class CommonImmediateSuperInteraction(CommonInteraction, ImmediateSuperInteraction):
    """An inheritable class that provides a way to create Custom Immediate Super Interactions.


    The main use for this class is to create interactions that do something upon starting the interaction, without the Sim needing to anything.
    One example would be the `Replace` interaction to replace objects that were destroyed in a fire.
    """
    pass
