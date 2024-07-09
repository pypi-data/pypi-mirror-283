from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SingleCmwCls:
	"""SingleCmw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("singleCmw", core, parent)

	# noinspection PyTypeChecker
	def get_cset(self) -> enums.ParameterSetMode:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:RFSettings:CMWS:CSET \n
		Snippet: value: enums.ParameterSetMode = driver.source.sequencer.rfSettings.singleCmw.get_cset() \n
		No command help available \n
			:return: cmws_connector_set: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:RFSettings:CMWS:CSET?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_cset(self, cmws_connector_set: enums.ParameterSetMode) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:RFSettings:CMWS:CSET \n
		Snippet: driver.source.sequencer.rfSettings.singleCmw.set_cset(cmws_connector_set = enums.ParameterSetMode.GLOBal) \n
		No command help available \n
			:param cmws_connector_set: No help available
		"""
		param = Conversions.enum_scalar_to_str(cmws_connector_set, enums.ParameterSetMode)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:RFSettings:CMWS:CSET {param}')
