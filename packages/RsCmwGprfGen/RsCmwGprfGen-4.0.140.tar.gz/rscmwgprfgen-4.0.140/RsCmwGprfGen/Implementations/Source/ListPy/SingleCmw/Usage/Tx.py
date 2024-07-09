from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxCls:
	"""Tx commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tx", core, parent)

	def set(self, index: int, usage: List[bool]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:CMWS:USAGe:TX \n
		Snippet: driver.source.listPy.singleCmw.usage.tx.set(index = 1, usage = [True, False, True]) \n
		No command help available \n
			:param index: No help available
			:param usage: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle.as_open_list('usage', usage, DataType.BooleanList, None))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:CMWS:USAGe:TX {param}'.rstrip())

	def get(self, index: int) -> List[bool]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:CMWS:USAGe:TX \n
		Snippet: value: List[bool] = driver.source.listPy.singleCmw.usage.tx.get(index = 1) \n
		No command help available \n
			:param index: No help available
			:return: usage: No help available"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:LIST:CMWS:USAGe:TX? {param}')
		return Conversions.str_to_bool_list(response)
