from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.Utilities import trim_str_response
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SignalCls:
	"""Signal commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("signal", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal:CATalog \n
		Snippet: value: List[str] = driver.source.sequencer.listPy.signal.get_catalog() \n
		Queries all available signal types. The available types depend on the ARB file pool. \n
			:return: signal_types: string Comma-separated list of strings, one string per supported signal type
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal:CATalog?')
		return Conversions.str_to_str_list(response)

	def set(self, index: int, signal: str) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal \n
		Snippet: driver.source.sequencer.listPy.signal.set(index = 1, signal = 'abc') \n
		Defines or queries the signal type for the sequencer list entry with the selected <Index>. A complete list of all
		supported strings can be queried using method RsCmwGprfGen.Source.Sequencer.ListPy.Signal.catalog. \n
			:param index: integer
			:param signal: string Signal type
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('index', index, DataType.Integer), ArgSingle('signal', signal, DataType.String))
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal {param}'.rstrip())

	def get(self, index: int) -> str:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal \n
		Snippet: value: str = driver.source.sequencer.listPy.signal.get(index = 1) \n
		Defines or queries the signal type for the sequencer list entry with the selected <Index>. A complete list of all
		supported strings can be queried using method RsCmwGprfGen.Source.Sequencer.ListPy.Signal.catalog. \n
			:param index: integer
			:return: signal: string Signal type"""
		param = Conversions.decimal_value_to_str(index)
		response = self._core.io.query_str(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal? {param}')
		return trim_str_response(response)

	def get_all(self) -> List[str]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal:ALL \n
		Snippet: value: List[str] = driver.source.sequencer.listPy.signal.get_all() \n
		Defines the signal types for all sequencer list entries. A complete list of all supported strings can be queried using
		method RsCmwGprfGen.Source.Sequencer.ListPy.Signal.catalog. \n
			:return: signal: string Comma-separated list of strings, one string per list entry
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal:ALL?')
		return Conversions.str_to_str_list(response)

	def set_all(self, signal: List[str]) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal:ALL \n
		Snippet: driver.source.sequencer.listPy.signal.set_all(signal = ['abc1', 'abc2', 'abc3']) \n
		Defines the signal types for all sequencer list entries. A complete list of all supported strings can be queried using
		method RsCmwGprfGen.Source.Sequencer.ListPy.Signal.catalog. \n
			:param signal: string Comma-separated list of strings, one string per list entry
		"""
		param = Conversions.list_to_csv_quoted_str(signal)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:SIGNal:ALL {param}')
