from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExecuteCls:
	"""Execute commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MANual:EXECute \n
		Snippet: driver.trigger.arb.segments.manual.execute.set() \n
		Generates a trigger event for the ARB segment trigger. The segment trigger causes the generator to step to the beginning
		of the next segment in the multi-segment file. \n
		"""
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MANual:EXECute')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MANual:EXECute \n
		Snippet: driver.trigger.arb.segments.manual.execute.set_with_opc() \n
		Generates a trigger event for the ARB segment trigger. The segment trigger causes the generator to step to the beginning
		of the next segment in the multi-segment file. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwGprfGen.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'TRIGger:GPRF:GENerator<Instance>:ARB:SEGMents:MANual:EXECute', opc_timeout_ms)
