from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DgainCls:
	"""Dgain commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dgain", core, parent)

	def set(self, index: int, digital_gain: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin \n
		Snippet: driver.source.sequencer.listPy.dgain.set(index = 1, digital_gain = 1.0) \n
		Defines or queries the digital gain for the sequencer list entry with the selected <Index>. \n
			:param index: integer
			:param digital_gain: numeric Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('digital_gain', digital_gain, DataType.Float))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin {param}'.rstrip())

	def get(self, index: int) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin \n
		Snippet: value: float = driver.source.sequencer.listPy.dgain.get(index = 1) \n
		Defines or queries the digital gain for the sequencer list entry with the selected <Index>. \n
			:param index: integer
			:return: digital_gain: numeric Unit: dB"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin? {param}')
		return Conversions.str_to_float(response)

	def get_all(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin:ALL \n
		Snippet: value: List[float] = driver.source.sequencer.listPy.dgain.get_all() \n
		Defines the digital gains for all sequencer list entries. \n
			:return: digital_gain: numeric Comma-separated list of values, one value per list entry Unit: dB
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin:ALL?')
		return response

	def set_all(self, digital_gain: List[float]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin:ALL \n
		Snippet: driver.source.sequencer.listPy.dgain.set_all(digital_gain = [1.1, 2.2, 3.3]) \n
		Defines the digital gains for all sequencer list entries. \n
			:param digital_gain: numeric Comma-separated list of values, one value per list entry Unit: dB
		"""
		param = Conversions.list_to_csv_str(digital_gain)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:DGAin:ALL {param}')
