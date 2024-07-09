from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RmarkerCls:
	"""Rmarker commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rmarker", core, parent)

	def get_delay(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:RMARker:DELay \n
		Snippet: value: float = driver.source.sequencer.rmarker.get_delay() \n
		Defines a delay time for the ARB output trigger events relative to the restart marker events. \n
			:return: restart_marker: numeric Range: 0 s to 0.1 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:RMARker:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, restart_marker: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:RMARker:DELay \n
		Snippet: driver.source.sequencer.rmarker.set_delay(restart_marker = 1.0) \n
		Defines a delay time for the ARB output trigger events relative to the restart marker events. \n
			:param restart_marker: numeric Range: 0 s to 0.1 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(restart_marker)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:RMARker:DELay {param}')
