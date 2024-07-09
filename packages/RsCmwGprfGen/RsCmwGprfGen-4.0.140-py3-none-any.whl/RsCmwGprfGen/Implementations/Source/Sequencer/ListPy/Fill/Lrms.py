from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LrmsCls:
	"""Lrms commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lrms", core, parent)

	def get_svalue(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:SVALue \n
		Snippet: value: float = driver.source.sequencer.listPy.fill.lrms.get_svalue() \n
		Configures the start value for filling the sequencer list with level values. \n
			:return: start_value: numeric Range: Please notice the ranges quoted in the data sheet. , Unit: dBm
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:SVALue?')
		return Conversions.str_to_float(response)

	def set_svalue(self, start_value: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:SVALue \n
		Snippet: driver.source.sequencer.listPy.fill.lrms.set_svalue(start_value = 1.0) \n
		Configures the start value for filling the sequencer list with level values. \n
			:param start_value: numeric Range: Please notice the ranges quoted in the data sheet. , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(start_value)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:SVALue {param}')

	def get_increment(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:INCRement \n
		Snippet: value: float = driver.source.sequencer.listPy.fill.lrms.get_increment() \n
		Configures the increment for filling the sequencer list with level values. \n
			:return: increment: numeric Range: Depends on the number of entries and on the start value , Unit: dBm
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:INCRement?')
		return Conversions.str_to_float(response)

	def set_increment(self, increment: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:INCRement \n
		Snippet: driver.source.sequencer.listPy.fill.lrms.set_increment(increment = 1.0) \n
		Configures the increment for filling the sequencer list with level values. \n
			:param increment: numeric Range: Depends on the number of entries and on the start value , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(increment)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:INCRement {param}')

	def get_keep(self) -> bool:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:KEEP \n
		Snippet: value: bool = driver.source.sequencer.listPy.fill.lrms.get_keep() \n
		Selects whether the level of existing entries is kept or overwritten when the sequencer list is filled. \n
			:return: keep_flag: OFF | ON OFF: overwrite values ON: keep values
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:KEEP?')
		return Conversions.str_to_bool(response)

	def set_keep(self, keep_flag: bool) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:KEEP \n
		Snippet: driver.source.sequencer.listPy.fill.lrms.set_keep(keep_flag = False) \n
		Selects whether the level of existing entries is kept or overwritten when the sequencer list is filled. \n
			:param keep_flag: OFF | ON OFF: overwrite values ON: keep values
		"""
		param = Conversions.bool_to_str(keep_flag)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:LRMS:KEEP {param}')
