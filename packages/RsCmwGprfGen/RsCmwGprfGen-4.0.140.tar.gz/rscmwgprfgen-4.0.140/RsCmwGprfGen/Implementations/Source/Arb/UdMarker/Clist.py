from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ClistCls:
	"""Clist commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("clist", core, parent)

	def set(self) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:UDMarker:CLISt \n
		Snippet: driver.source.arb.udMarker.clist.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:UDMarker:CLISt')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:UDMarker:CLISt \n
		Snippet: driver.source.arb.udMarker.clist.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwGprfGen.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce:GPRF:GENerator<Instance>:ARB:UDMarker:CLISt', opc_timeout_ms)
