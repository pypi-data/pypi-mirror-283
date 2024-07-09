from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ArbCls:
	"""Arb commands group definition. 28 total commands, 6 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("arb", core, parent)

	@property
	def samples(self):
		"""samples commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_samples'):
			from .Samples import SamplesCls
			self._samples = SamplesCls(self._core, self._cmd_group)
		return self._samples

	@property
	def udMarker(self):
		"""udMarker commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_udMarker'):
			from .UdMarker import UdMarkerCls
			self._udMarker = UdMarkerCls(self._core, self._cmd_group)
		return self._udMarker

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def msegment(self):
		"""msegment commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_msegment'):
			from .Msegment import MsegmentCls
			self._msegment = MsegmentCls(self._core, self._cmd_group)
		return self._msegment

	@property
	def marker(self):
		"""marker commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def segments(self):
		"""segments commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_segments'):
			from .Segments import SegmentsCls
			self._segments = SegmentsCls(self._core, self._cmd_group)
		return self._segments

	def get_foffset(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:FOFFset \n
		Snippet: value: float = driver.source.arb.get_foffset() \n
		Sets the frequency offset to be imposed at the baseband during ARB generation. \n
			:return: frequency_offset: numeric Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, frequency_offset: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:FOFFset \n
		Snippet: driver.source.arb.set_foffset(frequency_offset = 1.0) \n
		Sets the frequency offset to be imposed at the baseband during ARB generation. \n
			:param frequency_offset: numeric Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency_offset)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:FOFFset {param}')

	# noinspection PyTypeChecker
	class ScountStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Sample_Count_Time: float: No parameter help available
			- Sample_Count: List[int]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Sample_Count_Time'),
			ArgStruct('Sample_Count', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sample_Count_Time: float = None
			self.Sample_Count: List[int] = None

	def get_scount(self) -> ScountStruct:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:SCOunt \n
		Snippet: value: ScountStruct = driver.source.arb.get_scount() \n
		Queries the progress of ARB file processing. You can use the command to check in single-shot mode whether ARB file
		processing is complete. As long as the ARB file is processed, the command returns 0,0,0. In continuous mode, the command
		always returns 0,0,0. If ARB file processing is complete, the command returns results for the previous ARB file
		processing. \n
			:return: structure: for return value, see the help for ScountStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:GPRF:GENerator<Instance>:ARB:SCOunt?', self.__class__.ScountStruct())

	def get_asamples(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:ASAMples \n
		Snippet: value: int = driver.source.arb.get_asamples() \n
		Extends the processing time of a waveform file by the specified number of samples. The additional samples are valid in
		single-shot repetition mode only, see method RsCmwGprfGen.Source.Arb.repetition. \n
			:return: add_samples: numeric Range: 0 to max. (depending on waveform file)
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:ASAMples?')
		return Conversions.str_to_int(response)

	def set_asamples(self, add_samples: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:ASAMples \n
		Snippet: driver.source.arb.set_asamples(add_samples = 1) \n
		Extends the processing time of a waveform file by the specified number of samples. The additional samples are valid in
		single-shot repetition mode only, see method RsCmwGprfGen.Source.Arb.repetition. \n
			:param add_samples: numeric Range: 0 to max. (depending on waveform file)
		"""
		param = Conversions.decimal_value_to_str(add_samples)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:ASAMples {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.RepeatMode:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:REPetition \n
		Snippet: value: enums.RepeatMode = driver.source.arb.get_repetition() \n
		Defines how often the ARB file is processed. \n
			:return: repetition: CONTinuous | SINGle CONTinuous: unlimited, cyclic processing SINGle: The file is processed n times, where n is the number of cycles, see method RsCmwGprfGen.Source.Arb.cycles.
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_repetition(self, repetition: enums.RepeatMode) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:REPetition \n
		Snippet: driver.source.arb.set_repetition(repetition = enums.RepeatMode.CONTinuous) \n
		Defines how often the ARB file is processed. \n
			:param repetition: CONTinuous | SINGle CONTinuous: unlimited, cyclic processing SINGle: The file is processed n times, where n is the number of cycles, see method RsCmwGprfGen.Source.Arb.cycles.
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.RepeatMode)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:REPetition {param}')

	def get_cycles(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CYCLes \n
		Snippet: value: int = driver.source.arb.get_cycles() \n
		Defines how often the ARB file is processed. The ARB cycles are relevant in single-shot repetition mode only, see method
		RsCmwGprfGen.Source.Arb.repetition. \n
			:return: cycles: numeric Range: 1 to 10000
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:CYCLes?')
		return Conversions.str_to_int(response)

	def set_cycles(self, cycles: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CYCLes \n
		Snippet: driver.source.arb.set_cycles(cycles = 1) \n
		Defines how often the ARB file is processed. The ARB cycles are relevant in single-shot repetition mode only, see method
		RsCmwGprfGen.Source.Arb.repetition. \n
			:param cycles: numeric Range: 1 to 10000
		"""
		param = Conversions.decimal_value_to_str(cycles)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:CYCLes {param}')

	def get_poffset(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:POFFset \n
		Snippet: value: float = driver.source.arb.get_poffset() \n
		Queries the peak offset of the loaded waveform file. Note: If a multi-segment waveform file is loaded, this command
		returns the peak offset of the last segment. Use method RsCmwGprfGen.Source.Arb.Msegment.poffset to query the peak offset
		values of the individual segments. \n
			:return: peak_offset: float Unit: dB
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:POFFset?')
		return Conversions.str_to_float(response)

	def get_crate(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CRATe \n
		Snippet: value: float = driver.source.arb.get_crate() \n
		Queries the clock rate of the loaded waveform file. Note: If a multi-segment waveform file is loaded, this command
		returns the clock rate of the last segment. Use method RsCmwGprfGen.Source.Arb.Msegment.crate to query the clock rates of
		the individual segments. \n
			:return: clock_rate: float Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:CRATe?')
		return Conversions.str_to_float(response)

	def get_loffset(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:LOFFset \n
		Snippet: value: float = driver.source.arb.get_loffset() \n
		Queries the level offset (peak to average ratio, PAR) of the loaded waveform file. The PAR is equal to the absolute value
		of the difference between the 'RMS Offset' and the 'Peak Offset' (crest factor) . Note: If a multi-segment waveform file
		is loaded, this command returns the PAR of the last segment. Use method RsCmwGprfGen.Source.Arb.Msegment.par to query the
		PAR values of the individual segments. \n
			:return: level_offset: float Unit: dB
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:LOFFset?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_crc_protect(self) -> enums.YesNoStatus:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CRCProtect \n
		Snippet: value: enums.YesNoStatus = driver.source.arb.get_crc_protect() \n
		Indicates whether the loaded ARB file contains a CRC checksum. To get a valid result, the related ARB file must be loaded
		into the memory. That means, the baseband mode must be ARB and the generator state must be ON. Otherwise, NAV is returned. \n
			:return: crc_protection: NO | YES
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:CRCProtect?')
		return Conversions.str_to_scalar_enum(response, enums.YesNoStatus)

	def get_status(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:STATus \n
		Snippet: value: int = driver.source.arb.get_status() \n
		Queries the number of the currently processed segment. Even for the repetition 'Continuous Seamless', the currently
		processed segment is returned, independent of whether a trigger event for the next segment has already been received or
		not. \n
			:return: arb_segment_no: decimal NAV is returned if no file is loaded.
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:STATus?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'ArbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ArbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
