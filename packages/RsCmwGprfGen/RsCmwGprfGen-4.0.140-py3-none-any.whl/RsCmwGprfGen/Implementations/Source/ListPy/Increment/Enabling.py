from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnablingCls:
	"""Enabling commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enabling", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:INCRement:ENABling:CATalog \n
		Snippet: value: List[str] = driver.source.listPy.increment.enabling.get_catalog() \n
		Lists all initial trigger modes that can be set using method RsCmwGprfGen.Source.ListPy.Increment.Enabling.value. \n
			:return: enabling_srcs: string Comma-separated list of strings. Each string represents a supported initial trigger mode.
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:INCRement:ENABling:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:INCRement:ENABling \n
		Snippet: value: str = driver.source.listPy.increment.enabling.get_value() \n
		For an internally incremented list, this command defines the initial trigger. Internally incremented list means 'List
		Increment: GPRF Gen<i>: ... Marker ...' or 'List Increment: Dwell Time', see method RsCmwGprfGen.Source.ListPy.Increment.
		value. \n
			:return: enabling: string To generate a complete list of all supported triggers, see method RsCmwGprfGen.Source.ListPy.Increment.Enabling.catalog. 'Immediate': No initial trigger; list increment starts immediately. 'Manual': Waits until method RsCmwGprfGen.Source.ListPy.Slist.set is executed. 'meas trigger' (e.g. 'GPRF Measi: Power' or 'GSM Measi: Multi Evaluation') : Some measurement application provides the initial trigger.
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:INCRement:ENABling?')
		return trim_str_response(response)

	def set_value(self, enabling: str) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:INCRement:ENABling \n
		Snippet: driver.source.listPy.increment.enabling.set_value(enabling = 'abc') \n
		For an internally incremented list, this command defines the initial trigger. Internally incremented list means 'List
		Increment: GPRF Gen<i>: ... Marker ...' or 'List Increment: Dwell Time', see method RsCmwGprfGen.Source.ListPy.Increment.
		value. \n
			:param enabling: string To generate a complete list of all supported triggers, see method RsCmwGprfGen.Source.ListPy.Increment.Enabling.catalog. 'Immediate': No initial trigger; list increment starts immediately. 'Manual': Waits until method RsCmwGprfGen.Source.ListPy.Slist.set is executed. 'meas trigger' (e.g. 'GPRF Measi: Power' or 'GSM Measi: Multi Evaluation') : Some measurement application provides the initial trigger.
		"""
		param = Conversions.value_to_quoted_str(enabling)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:INCRement:ENABling {param}')
