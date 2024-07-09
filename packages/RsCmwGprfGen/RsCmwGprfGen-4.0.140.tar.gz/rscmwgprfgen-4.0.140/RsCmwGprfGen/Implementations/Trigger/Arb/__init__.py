from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ArbCls:
	"""Arb commands group definition. 9 total commands, 3 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("arb", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	@property
	def manual(self):
		"""manual commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_manual'):
			from .Manual import ManualCls
			self._manual = ManualCls(self._core, self._cmd_group)
		return self._manual

	@property
	def segments(self):
		"""segments commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_segments'):
			from .Segments import SegmentsCls
			self._segments = SegmentsCls(self._core, self._cmd_group)
		return self._segments

	def get_source(self) -> str:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SOURce \n
		Snippet: value: str = driver.trigger.arb.get_source() \n
		Selects the source of the trigger events. The supported values depend on the installed options. You can query a list of
		all supported values via method RsCmwGprfGen.Trigger.Arb.Catalog.source. \n
			:return: source: string
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SOURce \n
		Snippet: driver.trigger.arb.set_source(source = 'abc') \n
		Selects the source of the trigger events. The supported values depend on the installed options. You can query a list of
		all supported values via method RsCmwGprfGen.Trigger.Arb.Catalog.source. \n
			:param source: string
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:SOURce {param}')

	def get_delay(self) -> float:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:DELay \n
		Snippet: value: float = driver.trigger.arb.get_delay() \n
		Sets the trigger delay. The delay does not apply to manual execution (see method RsCmwGprfGen.Trigger.Arb.Segments.Manual.
		Execute.set) . \n
			:return: delay: numeric Range: 0 s to 100 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:DELay \n
		Snippet: driver.trigger.arb.set_delay(delay = 1.0) \n
		Sets the trigger delay. The delay does not apply to manual execution (see method RsCmwGprfGen.Trigger.Arb.Segments.Manual.
		Execute.set) . \n
			:param delay: numeric Range: 0 s to 100 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:DELay {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.arb.get_slope() \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. \n
			:return: slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe \n
		Snippet: driver.trigger.arb.set_slope(slope = enums.SignalSlope.FEDGe) \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. \n
			:param slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:SLOPe {param}')

	def get_retrigger(self) -> bool:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger \n
		Snippet: value: bool = driver.trigger.arb.get_retrigger() \n
		Enables or disables the trigger system for waveform files. \n
			:return: retrigger: OFF | ON Trigger system disabled or enabled
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger?')
		return Conversions.str_to_bool(response)

	def set_retrigger(self, retrigger: bool) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger \n
		Snippet: driver.trigger.arb.set_retrigger(retrigger = False) \n
		Enables or disables the trigger system for waveform files. \n
			:param retrigger: OFF | ON Trigger system disabled or enabled
		"""
		param = Conversions.bool_to_str(retrigger)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:RETRigger {param}')

	def get_autostart(self) -> bool:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart \n
		Snippet: value: bool = driver.trigger.arb.get_autostart() \n
		Enables or disables the automatic download of the selected (and loaded) waveform file whenever the generator is turned on. \n
			:return: autostart: OFF | ON Autostart is disabled or enabled.
		"""
		response = self._core.io.query_str('TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart?')
		return Conversions.str_to_bool(response)

	def set_autostart(self, autostart: bool) -> None:
		"""SCPI: TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart \n
		Snippet: driver.trigger.arb.set_autostart(autostart = False) \n
		Enables or disables the automatic download of the selected (and loaded) waveform file whenever the generator is turned on. \n
			:param autostart: OFF | ON Autostart is disabled or enabled.
		"""
		param = Conversions.bool_to_str(autostart)
		self._core.io.write(f'TRIGger:GPRF:GENerator<Instance>:ARB:AUTostart {param}')

	def clone(self) -> 'ArbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ArbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
