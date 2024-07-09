from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RlistCls:
	"""Rlist commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rlist", core, parent)

	def set(self) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:RLISt \n
		Snippet: driver.source.listPy.rlist.set() \n
		Restarts the list generator at the first frequency/level step. This command provides a fast alternative to a complete
		restart of the list generator (turn generator off and on again) . The active list index can be queried using method
		RsCmwGprfGen.Source.ListPy.aindex. \n
		"""
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:RLISt')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:RLISt \n
		Snippet: driver.source.listPy.rlist.set_with_opc() \n
		Restarts the list generator at the first frequency/level step. This command provides a fast alternative to a complete
		restart of the list generator (turn generator off and on again) . The active list index can be queried using method
		RsCmwGprfGen.Source.ListPy.aindex. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwGprfGen.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce:GPRF:GENerator<Instance>:LIST:RLISt', opc_timeout_ms)
