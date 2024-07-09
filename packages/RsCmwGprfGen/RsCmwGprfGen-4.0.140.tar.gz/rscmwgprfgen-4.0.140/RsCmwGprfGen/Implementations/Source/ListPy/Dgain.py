from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DgainCls:
	"""Dgain commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dgain", core, parent)

	def set(self, index: int, digital_gain: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DGAin \n
		Snippet: driver.source.listPy.dgain.set(index = 1, digital_gain = 1.0) \n
		Defines the digital gain of a selected frequency/level step. \n
			:param index: integer Number of the frequency/level step in the table Range: 0 to 1999
			:param digital_gain: numeric Digital gain at the step Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('digital_gain', digital_gain, DataType.Float))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:DGAin {param}'.rstrip())

	def get(self, index: int) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DGAin \n
		Snippet: value: float = driver.source.listPy.dgain.get(index = 1) \n
		Defines the digital gain of a selected frequency/level step. \n
			:param index: integer Number of the frequency/level step in the table Range: 0 to 1999
			:return: digital_gain: numeric Digital gain at the step Unit: dB"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:LIST:DGAin? {param}')
		return Conversions.str_to_float(response)

	def get_all(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DGAin:ALL \n
		Snippet: value: List[float] = driver.source.listPy.dgain.get_all() \n
		Defines the digital gains of all frequency/level steps. \n
			:return: all_digital_gains: numeric Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Unit: dB
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:LIST:DGAin:ALL?')
		return response

	def set_all(self, all_digital_gains: List[float]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:DGAin:ALL \n
		Snippet: driver.source.listPy.dgain.set_all(all_digital_gains = [1.1, 2.2, 3.3]) \n
		Defines the digital gains of all frequency/level steps. \n
			:param all_digital_gains: numeric Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Unit: dB
		"""
		param = Conversions.list_to_csv_str(all_digital_gains)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:DGAin:ALL {param}')
