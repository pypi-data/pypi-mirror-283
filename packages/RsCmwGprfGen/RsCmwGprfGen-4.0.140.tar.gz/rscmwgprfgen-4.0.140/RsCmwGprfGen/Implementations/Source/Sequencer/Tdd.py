from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TddCls:
	"""Tdd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tdd", core, parent)

	def get_mode(self) -> bool:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:TDD:MODE \n
		Snippet: value: bool = driver.source.sequencer.tdd.get_mode() \n
		No command help available \n
			:return: tdd_mode: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:TDD:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, tdd_mode: bool) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:TDD:MODE \n
		Snippet: driver.source.sequencer.tdd.set_mode(tdd_mode = False) \n
		No command help available \n
			:param tdd_mode: No help available
		"""
		param = Conversions.bool_to_str(tdd_mode)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:TDD:MODE {param}')
