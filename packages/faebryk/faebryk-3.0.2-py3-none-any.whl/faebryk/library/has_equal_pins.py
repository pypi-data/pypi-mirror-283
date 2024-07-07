# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

from abc import abstractmethod

from faebryk.library.FootprintTrait import FootprintTrait
from faebryk.library.Pad import Pad


class has_equal_pins(FootprintTrait):
    @abstractmethod
    def get_pin_map(self) -> dict[Pad, str]: ...
