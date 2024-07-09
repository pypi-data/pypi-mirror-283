from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxCls:
	"""Tx commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tx", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	def set(self, tx_connector: enums.TxConnectorCmws, usage: bool) -> None:
		"""SCPI: CONFigure:GPRF:GENerator<Instance>:CMWS:USAGe:TX \n
		Snippet: driver.configure.singleCmw.usage.tx.set(tx_connector = enums.TxConnectorCmws.R11, usage = False) \n
		No command help available \n
			:param tx_connector: No help available
			:param usage: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('tx_connector', tx_connector, DataType.Enum, enums.TxConnectorCmws), ArgSingle('usage', usage, DataType.Boolean))
		self._core.io.write(f'CONFigure:GPRF:GENerator<Instance>:CMWS:USAGe:TX {param}'.rstrip())

	def get(self, tx_connector: enums.TxConnectorCmws) -> bool:
		"""SCPI: CONFigure:GPRF:GENerator<Instance>:CMWS:USAGe:TX \n
		Snippet: value: bool = driver.configure.singleCmw.usage.tx.get(tx_connector = enums.TxConnectorCmws.R11) \n
		No command help available \n
			:param tx_connector: No help available
			:return: usage: No help available"""
		param = Conversions.enum_scalar_to_str(tx_connector, enums.TxConnectorCmws)
		response = self._core.io.query_str(f'CONFigure:GPRF:GENerator<Instance>:CMWS:USAGe:TX? {param}')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'TxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
