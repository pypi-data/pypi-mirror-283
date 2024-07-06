from __future__ import annotations

import shlex
from dataclasses import dataclass

from pyselector import constants
from pyselector import helpers
from pyselector.menus.arguments import Options


# @dataclass
# class Roof:
#     name: str = 'rofi'
#     url = constants.HOMEPAGE_ROFI
#     opts = Options()
#
#     @property
#     def command(self) -> str:
#         return helpers.check_command(self.name, self.url)
#
#     @property
#     def args(self) -> list[str]:
#         cmd = shlex.split(self.command)
#         cmd.extend(self.opts.current())
#         return cmd
