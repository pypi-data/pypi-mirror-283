from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPyCls:
	"""ListPy commands group definition. 32 total commands, 13 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("listPy", core, parent)

	@property
	def singleCmw(self):
		"""singleCmw commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_singleCmw'):
			from .SingleCmw import SingleCmwCls
			self._singleCmw = SingleCmwCls(self._core, self._cmd_group)
		return self._singleCmw

	@property
	def slist(self):
		"""slist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slist'):
			from .Slist import SlistCls
			self._slist = SlistCls(self._core, self._cmd_group)
		return self._slist

	@property
	def esingle(self):
		"""esingle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_esingle'):
			from .Esingle import EsingleCls
			self._esingle = EsingleCls(self._core, self._cmd_group)
		return self._esingle

	@property
	def rlist(self):
		"""rlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rlist'):
			from .Rlist import RlistCls
			self._rlist = RlistCls(self._core, self._cmd_group)
		return self._rlist

	@property
	def increment(self):
		"""increment commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_increment'):
			from .Increment import IncrementCls
			self._increment = IncrementCls(self._core, self._cmd_group)
		return self._increment

	@property
	def sstop(self):
		"""sstop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sstop'):
			from .Sstop import SstopCls
			self._sstop = SstopCls(self._core, self._cmd_group)
		return self._sstop

	@property
	def rfLevel(self):
		"""rfLevel commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfLevel'):
			from .RfLevel import RfLevelCls
			self._rfLevel = RfLevelCls(self._core, self._cmd_group)
		return self._rfLevel

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def irepetition(self):
		"""irepetition commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_irepetition'):
			from .Irepetition import IrepetitionCls
			self._irepetition = IrepetitionCls(self._core, self._cmd_group)
		return self._irepetition

	@property
	def dgain(self):
		"""dgain commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dgain'):
			from .Dgain import DgainCls
			self._dgain = DgainCls(self._core, self._cmd_group)
		return self._dgain

	@property
	def dtime(self):
		"""dtime commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dtime'):
			from .Dtime import DtimeCls
			self._dtime = DtimeCls(self._core, self._cmd_group)
		return self._dtime

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def reenabling(self):
		"""reenabling commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_reenabling'):
			from .Reenabling import ReenablingCls
			self._reenabling = ReenablingCls(self._core, self._cmd_group)
		return self._reenabling

	def get_aindex(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:AINDex \n
		Snippet: value: int = driver.source.listPy.get_aindex() \n
		Returns the currently active list index. \n
			:return: active_index: decimal Range: 0 to 19
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:AINDex?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	class FillStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Start_Index: float: numeric The start index of the list segment to be 'filled'. Range: 0 to 1999
			- Range_Py: float: numeric The range (length) of the list segment to be 'filled'. Range: 1 to 2000
			- Index_Repetition: int: integer The constant 'Index Repetition' within this list segment. Range: 1 to 10000
			- Start_Frequency: float: numeric The frequency of list item StartIndex. For the supported frequency range, see 'Frequency ranges'. Unit: Hz
			- Freq_Increment: float: numeric The frequency increment within this list segment. Range: -282.45 MHz to 1.20005 GHz , Unit: Hz
			- Start_Power: float: numeric The RMS level of list item StartIndex. Range: Depends on the instrument model, the connector and other settings; please notice the ranges quoted in the data sheet , Unit: dBm
			- Power_Increment: float: numeric The power increment within this list segment. Range: -29.5 dBm to 3 dBm , Unit: dBm
			- Start_Dwell_Time: float: Optional setting parameter. numeric The constant dwell time within this list segment. Range: 2.0E-4 s to 20 s , Unit: s
			- Reenable: bool: Optional setting parameter. OFF | ON The constant 'Reenable' property within this list segment.
			- Modulation: bool: Optional setting parameter. OFF | ON The constant 'Modulation ON|OFF' property within this list segment.
			- Start_Gain: float: Optional setting parameter. numeric The digital gain of list item StartIndex. Range: -30 dB to 0 dB , Unit: dB
			- Gain_Increment: float: Optional setting parameter. numeric The digital gain increment within this list segment. Range: -7.5 dB to 0 dB , Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Start_Index'),
			ArgStruct.scalar_float('Range_Py'),
			ArgStruct.scalar_int('Index_Repetition'),
			ArgStruct.scalar_float('Start_Frequency'),
			ArgStruct.scalar_float('Freq_Increment'),
			ArgStruct.scalar_float('Start_Power'),
			ArgStruct.scalar_float('Power_Increment'),
			ArgStruct.scalar_float_optional('Start_Dwell_Time'),
			ArgStruct.scalar_bool_optional('Reenable'),
			ArgStruct.scalar_bool_optional('Modulation'),
			ArgStruct.scalar_float_optional('Start_Gain'),
			ArgStruct.scalar_float_optional('Gain_Increment')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Start_Index: float = None
			self.Range_Py: float = None
			self.Index_Repetition: int = None
			self.Start_Frequency: float = None
			self.Freq_Increment: float = None
			self.Start_Power: float = None
			self.Power_Increment: float = None
			self.Start_Dwell_Time: float = None
			self.Reenable: bool = None
			self.Modulation: bool = None
			self.Start_Gain: float = None
			self.Gain_Increment: float = None

	def set_fill(self, value: FillStruct) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:FILL \n
		Snippet with structure: \n
		structure = driver.source.listPy.FillStruct() \n
		structure.Start_Index: float = 1.0 \n
		structure.Range_Py: float = 1.0 \n
		structure.Index_Repetition: int = 1 \n
		structure.Start_Frequency: float = 1.0 \n
		structure.Freq_Increment: float = 1.0 \n
		structure.Start_Power: float = 1.0 \n
		structure.Power_Increment: float = 1.0 \n
		structure.Start_Dwell_Time: float = 1.0 \n
		structure.Reenable: bool = False \n
		structure.Modulation: bool = False \n
		structure.Start_Gain: float = 1.0 \n
		structure.Gain_Increment: float = 1.0 \n
		driver.source.listPy.set_fill(value = structure) \n
		Convenience command to simplify the configuration of the frequency/level list. Within a list segment determined by its
		start index and range (length) , the frequency, power and (optionally) the digital gain are incremented by configurable
		step sizes. The other list item settings are fixed. \n
			:param value: see the help for FillStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce:GPRF:GENerator<Instance>:LIST:FILL', value)

	def get_goto(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:GOTO \n
		Snippet: value: int = driver.source.listPy.get_goto() \n
		Defines the start index for the second and all following generator cycles in continuous mode (method RsCmwGprfGen.Source.
		ListPy.repetition) . The index must be in the selected list section (method RsCmwGprfGen.Source.ListPy.Sstop.set) . \n
			:return: goto_index: numeric Range: 1 to 2000
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:GOTO?')
		return Conversions.str_to_int(response)

	def set_goto(self, goto_index: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:GOTO \n
		Snippet: driver.source.listPy.set_goto(goto_index = 1) \n
		Defines the start index for the second and all following generator cycles in continuous mode (method RsCmwGprfGen.Source.
		ListPy.repetition) . The index must be in the selected list section (method RsCmwGprfGen.Source.ListPy.Sstop.set) . \n
			:param goto_index: numeric Range: 1 to 2000
		"""
		param = Conversions.decimal_value_to_str(goto_index)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:GOTO {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.RepeatMode:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:REPetition \n
		Snippet: value: enums.RepeatMode = driver.source.listPy.get_repetition() \n
		Defines how often the RF generator runs through the list. \n
			:return: repetition: CONTinuous | SINGle CONTinuous: The generator cycles through the list. SINGle: The generator runs through the list for a single time. The sequence is triggered via method RsCmwGprfGen.Source.ListPy.Esingle.set.
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_repetition(self, repetition: enums.RepeatMode) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:REPetition \n
		Snippet: driver.source.listPy.set_repetition(repetition = enums.RepeatMode.CONTinuous) \n
		Defines how often the RF generator runs through the list. \n
			:param repetition: CONTinuous | SINGle CONTinuous: The generator cycles through the list. SINGle: The generator runs through the list for a single time. The sequence is triggered via method RsCmwGprfGen.Source.ListPy.Esingle.set.
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.RepeatMode)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:REPetition {param}')

	def get_start(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:STARt \n
		Snippet: value: int = driver.source.listPy.get_start() \n
		Defines the number of the first measured frequency/level step in the list. The start index must not be larger than the
		stop index (see method RsCmwGprfGen.Source.ListPy.stop) . \n
			:return: start_index: numeric Range: 0 to 1999
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:STARt?')
		return Conversions.str_to_int(response)

	def set_start(self, start_index: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:STARt \n
		Snippet: driver.source.listPy.set_start(start_index = 1) \n
		Defines the number of the first measured frequency/level step in the list. The start index must not be larger than the
		stop index (see method RsCmwGprfGen.Source.ListPy.stop) . \n
			:param start_index: numeric Range: 0 to 1999
		"""
		param = Conversions.decimal_value_to_str(start_index)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:STARt {param}')

	def get_stop(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:STOP \n
		Snippet: value: int = driver.source.listPy.get_stop() \n
		Defines the number of the last measured frequency/level step in the list. The stop index must not be smaller than the
		start index (see method RsCmwGprfGen.Source.ListPy.start) . \n
			:return: stop_index: numeric Range: 0 to 1999
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:STOP?')
		return Conversions.str_to_int(response)

	def set_stop(self, stop_index: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:STOP \n
		Snippet: driver.source.listPy.set_stop(stop_index = 1) \n
		Defines the number of the last measured frequency/level step in the list. The stop index must not be smaller than the
		start index (see method RsCmwGprfGen.Source.ListPy.start) . \n
			:param stop_index: numeric Range: 0 to 1999
		"""
		param = Conversions.decimal_value_to_str(stop_index)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST:STOP {param}')

	def get_count(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST:COUNt \n
		Snippet: value: int = driver.source.listPy.get_count() \n
		Queries the number of frequency/level steps of the RF generator in list mode. \n
			:return: list_count: decimal Number of frequency/level steps in list mode Range: 1 to 2000
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST:COUNt?')
		return Conversions.str_to_int(response)

	def get_value(self) -> bool:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST \n
		Snippet: value: bool = driver.source.listPy.get_value() \n
		Enables or disables the list mode of the RF generator. \n
			:return: enable_list_mode: ON | OFF ON: List mode enabled OFF: List mode disabled (constant-frequency generator)
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:LIST?')
		return Conversions.str_to_bool(response)

	def set_value(self, enable_list_mode: bool) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:LIST \n
		Snippet: driver.source.listPy.set_value(enable_list_mode = False) \n
		Enables or disables the list mode of the RF generator. \n
			:param enable_list_mode: ON | OFF ON: List mode enabled OFF: List mode disabled (constant-frequency generator)
		"""
		param = Conversions.bool_to_str(enable_list_mode)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:LIST {param}')

	def clone(self) -> 'ListPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
