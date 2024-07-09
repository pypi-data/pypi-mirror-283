from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReenablingCls:
	"""Reenabling commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reenabling", core, parent)

	def set(self, index: int, reenabling: bool) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:REENabling \n
		Snippet: driver.source.listPy.reenabling.set(index = 1, reenabling = False) \n
		Defines or queries the 'Reenable On / Off' setting of a selected frequency/level step. The setting is valid if the list
		increment is enabled by a measurement (see method RsCmwGprfGen.Source.ListPy.Increment.Enabling.value) . \n
			:param index: integer Number of the frequency/level step in the table Range: 0 to 1999
			:param reenabling: OFF | ON Disable/enable retriggered frequency/level steps
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('reenabling', reenabling, DataType.Boolean))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:REENabling {param}'.rstrip())

	def get(self, index: int) -> bool:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:REENabling \n
		Snippet: value: bool = driver.source.listPy.reenabling.get(index = 1) \n
		Defines or queries the 'Reenable On / Off' setting of a selected frequency/level step. The setting is valid if the list
		increment is enabled by a measurement (see method RsCmwGprfGen.Source.ListPy.Increment.Enabling.value) . \n
			:param index: integer Number of the frequency/level step in the table Range: 0 to 1999
			:return: reenabling: OFF | ON Disable/enable retriggered frequency/level steps"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:LIST:REENabling? {param}')
		return Conversions.str_to_bool(response)

	def get_all(self) -> List[bool]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:REENabling:ALL \n
		Snippet: value: List[bool] = driver.source.listPy.reenabling.get_all() \n
		Defines or queries the 'Reenable On / Off' setting of all frequency/level steps. The setting is valid if the list
		increment is enabled by a measurement (see method RsCmwGprfGen.Source.ListPy.Increment.Enabling.value) . \n
			:return: all_reenables: OFF | ON Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Each value disables/enables a retriggered frequency/level step.
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:REENabling:ALL?')
		return Conversions.str_to_bool_list(response)

	def set_all(self, all_reenables: List[bool]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:REENabling:ALL \n
		Snippet: driver.source.listPy.reenabling.set_all(all_reenables = [True, False, True]) \n
		Defines or queries the 'Reenable On / Off' setting of all frequency/level steps. The setting is valid if the list
		increment is enabled by a measurement (see method RsCmwGprfGen.Source.ListPy.Increment.Enabling.value) . \n
			:param all_reenables: OFF | ON Comma-separated list of n values, one per frequency/level step, where n 2001. The query returns 2000 results. Each value disables/enables a retriggered frequency/level step.
		"""
		param = Conversions.list_to_csv_str(all_reenables)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:REENabling:ALL {param}')
