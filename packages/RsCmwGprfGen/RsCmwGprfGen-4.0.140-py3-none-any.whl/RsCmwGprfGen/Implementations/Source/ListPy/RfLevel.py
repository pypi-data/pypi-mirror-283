from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfLevelCls:
	"""RfLevel commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfLevel", core, parent)

	def set(self, index: int, level: float or bool) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:RFLevel \n
		Snippet: driver.source.listPy.rfLevel.set(index = 1, level = 1.0) \n
		Defines or queries the level of the frequency/level step number <Index>. \n
			:param index: integer Number of the frequency/level step in the table. Range: 0 to 1999
			:param level: (float or boolean) numeric | ON | OFF Level of the frequency/level step Range: Depends on the instrument model, the connector and other settings; please notice the ranges quoted in the data sheet , Unit: dBm ON | OFF enables or disables the frequency/level step.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('level', level, DataType.FloatExt))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:RFLevel {param}'.rstrip())

	def get(self, index: int) -> float or bool:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:RFLevel \n
		Snippet: value: float or bool = driver.source.listPy.rfLevel.get(index = 1) \n
		Defines or queries the level of the frequency/level step number <Index>. \n
			:param index: integer Number of the frequency/level step in the table. Range: 0 to 1999
			:return: level: (float or boolean) numeric | ON | OFF Level of the frequency/level step Range: Depends on the instrument model, the connector and other settings; please notice the ranges quoted in the data sheet , Unit: dBm ON | OFF enables or disables the frequency/level step."""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:LIST:RFLevel? {param}')
		return Conversions.str_to_float_or_bool(response)

	def get_all(self) -> List[float or bool]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:RFLevel:ALL \n
		Snippet: value: List[float or bool] = driver.source.listPy.rfLevel.get_all() \n
		Defines the levels of all frequency/level steps. \n
			:return: all_levels: (float or boolean items) numeric | ON | OFF Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Range: Depends on the instrument model, the connector and other settings; please notice the ranges quoted in the data sheet , Unit: dBm ON | OFF enables or disables the frequency/level step.
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:RFLevel:ALL?')
		return Conversions.str_to_float_or_bool_list(response)

	def set_all(self, all_levels: List[float or bool]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:RFLevel:ALL \n
		Snippet: driver.source.listPy.rfLevel.set_all(all_levels = [1.1, True, 2.2, False, 3.3]) \n
		Defines the levels of all frequency/level steps. \n
			:param all_levels: (float or boolean items) numeric | ON | OFF Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Range: Depends on the instrument model, the connector and other settings; please notice the ranges quoted in the data sheet , Unit: dBm ON | OFF enables or disables the frequency/level step.
		"""
		param = Conversions.list_to_csv_str(all_levels)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:RFLevel:ALL {param}')
