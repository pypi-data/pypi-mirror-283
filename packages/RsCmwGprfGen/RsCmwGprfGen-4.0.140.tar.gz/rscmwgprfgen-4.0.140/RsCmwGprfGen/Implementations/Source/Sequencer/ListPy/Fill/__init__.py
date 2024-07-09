from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FillCls:
	"""Fill commands group definition. 12 total commands, 4 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fill", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def lrms(self):
		"""lrms commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lrms'):
			from .Lrms import LrmsCls
			self._lrms = LrmsCls(self._core, self._cmd_group)
		return self._lrms

	@property
	def dgain(self):
		"""dgain commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_dgain'):
			from .Dgain import DgainCls
			self._dgain = DgainCls(self._core, self._cmd_group)
		return self._dgain

	def get_sindex(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:SINDex \n
		Snippet: value: int = driver.source.sequencer.listPy.fill.get_sindex() \n
		Selects the first index of the sequence to be filled. The maximum value is limited by the index of the highest existing
		entry plus 1. \n
			:return: start_index: integer Range: 0 to 1999
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:SINDex?')
		return Conversions.str_to_int(response)

	def set_sindex(self, start_index: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:SINDex \n
		Snippet: driver.source.sequencer.listPy.fill.set_sindex(start_index = 1) \n
		Selects the first index of the sequence to be filled. The maximum value is limited by the index of the highest existing
		entry plus 1. \n
			:param start_index: integer Range: 0 to 1999
		"""
		param = Conversions.decimal_value_to_str(start_index)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:SINDex {param}')

	def get_range(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:RANGe \n
		Snippet: value: int = driver.source.sequencer.listPy.fill.get_range() \n
		Specifies the number of entries to be filled. The maximum is limited by 2000 minus the start index of the sequence. \n
			:return: range_py: integer Range: 1 to 2000
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:RANGe?')
		return Conversions.str_to_int(response)

	def set_range(self, range_py: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:RANGe \n
		Snippet: driver.source.sequencer.listPy.fill.set_range(range_py = 1) \n
		Specifies the number of entries to be filled. The maximum is limited by 2000 minus the start index of the sequence. \n
			:param range_py: integer Range: 1 to 2000
		"""
		param = Conversions.decimal_value_to_str(range_py)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:SEQuencer:LIST:FILL:RANGe {param}')

	def clone(self) -> 'FillCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FillCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
