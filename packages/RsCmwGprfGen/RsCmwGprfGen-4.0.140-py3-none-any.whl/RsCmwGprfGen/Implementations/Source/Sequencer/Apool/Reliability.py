from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReliabilityCls:
	"""Reliability commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reliability", core, parent)

	def get(self, index: int) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:RELiability \n
		Snippet: value: int = driver.source.sequencer.apool.reliability.get(index = 1) \n
		Queries the reliability indicator for the ARB file with the specified <Index>. For possible values, see 'Reliability
		indicator'. \n
			:param index: integer
			:return: reliability: decimal Reliability indicator"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:APOol:RELiability? {param}')
		return Conversions.str_to_int(response)
