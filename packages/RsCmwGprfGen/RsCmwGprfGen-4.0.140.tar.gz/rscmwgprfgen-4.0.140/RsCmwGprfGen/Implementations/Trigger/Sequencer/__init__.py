from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SequencerCls:
	"""Sequencer commands group definition. 6 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sequencer", core, parent)

	@property
	def isMeas(self):
		"""isMeas commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_isMeas'):
			from .IsMeas import IsMeasCls
			self._isMeas = IsMeasCls(self._core, self._cmd_group)
		return self._isMeas

	@property
	def isTrigger(self):
		"""isTrigger commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_isTrigger'):
			from .IsTrigger import IsTriggerCls
			self._isTrigger = IsTriggerCls(self._core, self._cmd_group)
		return self._isTrigger

	@property
	def manual(self):
		"""manual commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_manual'):
			from .Manual import ManualCls
			self._manual = ManualCls(self._core, self._cmd_group)
		return self._manual

	def get_timeout(self) -> float or bool:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:SEQuencer:TOUT \n
		Snippet: value: float or bool = driver.trigger.sequencer.get_timeout() \n
		Sets a timeout for waiting for a trigger event for 'List Increment' = 'MEASUREMENT' and 'TRIGGER'. \n
			:return: timeout: (float or boolean) float | ON | OFF Range: 0.01 s to 300 s, Unit: s ON | OFF enables or disables the timeout check.
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:SEQuencer:TOUT?')
		return Conversions.str_to_float_or_bool(response)

	def set_timeout(self, timeout: float or bool) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:SEQuencer:TOUT \n
		Snippet: driver.trigger.sequencer.set_timeout(timeout = 1.0) \n
		Sets a timeout for waiting for a trigger event for 'List Increment' = 'MEASUREMENT' and 'TRIGGER'. \n
			:param timeout: (float or boolean) float | ON | OFF Range: 0.01 s to 300 s, Unit: s ON | OFF enables or disables the timeout check.
		"""
		param = Conversions.decimal_or_bool_value_to_str(timeout)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:SEQuencer:TOUT {param}')

	def clone(self) -> 'SequencerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SequencerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
