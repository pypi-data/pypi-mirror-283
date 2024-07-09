from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MsegmentCls:
	"""Msegment commands group definition. 7 total commands, 0 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("msegment", core, parent)

	def get_name(self) -> List[str]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:NAME \n
		Snippet: value: List[str] = driver.source.arb.msegment.get_name() \n
		Queries the names of all segments in the loaded multi-segment waveform file. \n
			:return: name: string Comma-separated list of names, one string per segment
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:NAME?')
		return Conversions.str_to_str_list(response)

	def get_poffset(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:POFFset \n
		Snippet: value: List[float] = driver.source.arb.msegment.get_poffset() \n
		Queries the peak offset of all segments in the loaded multi-segment waveform file. \n
			:return: peak_offset: float Comma-separated list of peak offset values, one value per segment Unit: dB
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:POFFset?')
		return response

	def get_par(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:PAR \n
		Snippet: value: List[float] = driver.source.arb.msegment.get_par() \n
		Queries the level offset (peak to average ratio, PAR) of all segments in the loaded multi-segment waveform file. The PAR
		is equal to the absolute value of the difference between the 'RMS Offset' and the 'Peak Offset' defined in WinIQSIM2
		(crest factor) . \n
			:return: par: float Comma-separated list of PAR values, one value per segment Unit: dB
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:PAR?')
		return response

	def get_duration(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:DURation \n
		Snippet: value: List[float] = driver.source.arb.msegment.get_duration() \n
		Queries the durations (processing times) of all segments in the loaded multi-segment waveform file. The duration is given
		by the number of samples divided by the clock rate. \n
			:return: duration: float Comma-separated list of durations, one value per segment Unit: s
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:DURation?')
		return response

	def get_samples(self) -> List[int]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:SAMPles \n
		Snippet: value: List[int] = driver.source.arb.msegment.get_samples() \n
		Queries the number of samples in all segments in the loaded multi-segment waveform file. \n
			:return: samples: decimal Comma-separated list of sample values, one value per segment
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:SAMPles?')
		return response

	def get_crate(self) -> List[float]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:CRATe \n
		Snippet: value: List[float] = driver.source.arb.msegment.get_crate() \n
		Queries the clock rates of all segments in the loaded multi-segment waveform file. The clock rates of waveform files
		created with R&S WinIQSIM2 are compatible with the R&S CMW. \n
			:return: clock_rate: float Comma-separated list of clock rates, one value per segment Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:CRATe?')
		return response

	def get_number(self) -> List[int]:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:NUMBer \n
		Snippet: value: List[int] = driver.source.arb.msegment.get_number() \n
		Queries the segment numbers of all segments in the loaded multi-segment waveform file. \n
			:return: seg_number: decimal Comma-separated list of segment numbers, one value per segment
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SOURce:GPRF:GENerator<Instance>:ARB:MSEGment:NUMBer?')
		return response
