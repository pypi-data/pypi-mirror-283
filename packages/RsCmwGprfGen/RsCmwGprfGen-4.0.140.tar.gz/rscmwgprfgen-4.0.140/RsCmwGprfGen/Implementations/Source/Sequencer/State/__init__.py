from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	def set(self, control: bool) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:STATe \n
		Snippet: driver.source.sequencer.state.set(control = False) \n
		Turns the generator on or off. \n
			:param control: ON | OFF Switch the generator ON or OFF.
		"""
		param = Conversions.bool_to_str(control)
		self._core.io.write_with_opc(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:STATe {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.GeneratorState:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:STATe \n
		Snippet: value: enums.GeneratorState = driver.source.sequencer.state.get() \n
		Turns the generator on or off. \n
			:return: generator_state: OFF | PENDing | ON | RDY OFF: generator switched off PEND: state transition ongoing ON: generator switched on, signal available RDY: generator switched off, sequencer list processing complete for 'Repetition'='Single'"""
		response = self._core.io.query_str_with_opc(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorState)

	def clone(self) -> 'StateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
