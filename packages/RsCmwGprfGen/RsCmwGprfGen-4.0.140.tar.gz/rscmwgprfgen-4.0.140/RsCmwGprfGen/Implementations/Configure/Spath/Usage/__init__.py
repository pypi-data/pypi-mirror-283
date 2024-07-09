from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsageCls:
	"""Usage commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("usage", core, parent)

	@property
	def bench(self):
		"""bench commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bench'):
			from .Bench import BenchCls
			self._bench = BenchCls(self._core, self._cmd_group)
		return self._bench

	def get_value(self) -> List[bool]:
		"""SCPI: CONFigure:GPRF:GENerator<Instance>:SPATh:USAGe \n
		Snippet: value: List[bool] = driver.configure.spath.usage.get_value() \n
		No command help available \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:GENerator<Instance>:SPATh:USAGe?')
		return Conversions.str_to_bool_list(response)

	def set_value(self, enable: List[bool]) -> None:
		"""SCPI: CONFigure:GPRF:GENerator<Instance>:SPATh:USAGe \n
		Snippet: driver.configure.spath.usage.set_value(enable = [True, False, True]) \n
		No command help available \n
			:param enable: No help available
		"""
		param = Conversions.list_to_csv_str(enable)
		self._core.io.write(f'CONFigure:GPRF:GENerator<Instance>:SPATh:USAGe {param}')

	def clone(self) -> 'UsageCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UsageCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
