from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SingleCmwCls:
	"""SingleCmw commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("singleCmw", core, parent)

	@property
	def usage(self):
		"""usage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_usage'):
			from .Usage import UsageCls
			self._usage = UsageCls(self._core, self._cmd_group)
		return self._usage

	# noinspection PyTypeChecker
	def get_cset(self) -> enums.ParameterSetMode:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:CMWS:CSET \n
		Snippet: value: enums.ParameterSetMode = driver.source.listPy.singleCmw.get_cset() \n
		No command help available \n
			:return: cmws_connector_set: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:CMWS:CSET?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_cset(self, cmws_connector_set: enums.ParameterSetMode) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:CMWS:CSET \n
		Snippet: driver.source.listPy.singleCmw.set_cset(cmws_connector_set = enums.ParameterSetMode.GLOBal) \n
		No command help available \n
			:param cmws_connector_set: No help available
		"""
		param = Conversions.enum_scalar_to_str(cmws_connector_set, enums.ParameterSetMode)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:CMWS:CSET {param}')

	def clone(self) -> 'SingleCmwCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SingleCmwCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
