from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EsingleCls:
	"""Esingle commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("esingle", core, parent)

	def set(self) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:ESINgle \n
		Snippet: driver.source.listPy.esingle.set() \n
		Starts a single generator cycle through the frequency/level list.
			INTRO_CMD_HELP: This command is available only if: \n
			- The list mode is enabled (see method RsCmwGprfGen.Source.ListPy.value) .
			- And the 'Single' list mode is set (method RsCmwGprfGen.Source.ListPy.repetition) .
			- And the increment 'Dwell Time' is set (method RsCmwGprfGen.Source.ListPy.Increment.value) . \n
		"""
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:ESINgle')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:ESINgle \n
		Snippet: driver.source.listPy.esingle.set_with_opc() \n
		Starts a single generator cycle through the frequency/level list.
			INTRO_CMD_HELP: This command is available only if: \n
			- The list mode is enabled (see method RsCmwGprfGen.Source.ListPy.value) .
			- And the 'Single' list mode is set (method RsCmwGprfGen.Source.ListPy.repetition) .
			- And the increment 'Dwell Time' is set (method RsCmwGprfGen.Source.ListPy.Increment.value) . \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwGprfGen.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce:GPRF:GENerator<Instance>:LIST:ESINgle', opc_timeout_ms)
