from enum import Enum


# noinspection SpellCheckingInspection
class ArbFile(Enum):
	"""3 Members, ABSPath ... TRUTh"""
	ABSPath = 0
	DEF = 1
	TRUTh = 2


# noinspection SpellCheckingInspection
class ArbSegmentsMode(Enum):
	"""3 Members, AUTO ... CSEamless"""
	AUTO = 0
	CONTinuous = 1
	CSEamless = 2


# noinspection SpellCheckingInspection
class BasebandMode(Enum):
	"""3 Members, ARB ... DTONe"""
	ARB = 0
	CW = 1
	DTONe = 2


# noinspection SpellCheckingInspection
class GeneratorState(Enum):
	"""8 Members, ADJusted ... RDY"""
	ADJusted = 0
	AUTonomous = 1
	COUPled = 2
	INValid = 3
	OFF = 4
	ON = 5
	PENDing = 6
	RDY = 7


# noinspection SpellCheckingInspection
class IncTransition(Enum):
	"""6 Members, IMMediate ... WMA4"""
	IMMediate = 0
	RMARker = 1
	WMA1 = 2
	WMA2 = 3
	WMA3 = 4
	WMA4 = 5


# noinspection SpellCheckingInspection
class InstrumentType(Enum):
	"""2 Members, PROTocol ... SIGNaling"""
	PROTocol = 0
	SIGNaling = 1


# noinspection SpellCheckingInspection
class ListIncrement(Enum):
	"""5 Members, ACYCles ... USER"""
	ACYCles = 0
	DTIMe = 1
	MEASurement = 2
	TRIGger = 3
	USER = 4


# noinspection SpellCheckingInspection
class ParameterSetMode(Enum):
	"""2 Members, GLOBal ... LIST"""
	GLOBal = 0
	LIST = 1


# noinspection SpellCheckingInspection
class Range(Enum):
	"""2 Members, FULL ... SUB"""
	FULL = 0
	SUB = 1


# noinspection SpellCheckingInspection
class RepeatMode(Enum):
	"""2 Members, CONTinuous ... SINGle"""
	CONTinuous = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class Scenario(Enum):
	"""3 Members, IQOut ... SALone"""
	IQOut = 0
	NAV = 1
	SALone = 2


# noinspection SpellCheckingInspection
class SignalSlope(Enum):
	"""2 Members, FEDGe ... REDGe"""
	FEDGe = 0
	REDGe = 1


# noinspection SpellCheckingInspection
class TargetMainState(Enum):
	"""3 Members, OFF ... STOP"""
	OFF = 0
	RUN = 1
	STOP = 2


# noinspection SpellCheckingInspection
class TargetSyncState(Enum):
	"""2 Members, ADJusted ... PENDing"""
	ADJusted = 0
	PENDing = 1


# noinspection SpellCheckingInspection
class TransferMode(Enum):
	"""2 Members, ENABlemode ... REQuestmode"""
	ENABlemode = 0
	REQuestmode = 1


# noinspection SpellCheckingInspection
class TxConnector(Enum):
	"""86 Members, I12O ... RH18"""
	I12O = 0
	I14O = 1
	I16O = 2
	I18O = 3
	I22O = 4
	I24O = 5
	I26O = 6
	I28O = 7
	I32O = 8
	I34O = 9
	I36O = 10
	I38O = 11
	I42O = 12
	I44O = 13
	I46O = 14
	I48O = 15
	IFO1 = 16
	IFO2 = 17
	IFO3 = 18
	IFO4 = 19
	IFO5 = 20
	IFO6 = 21
	IQ2O = 22
	IQ4O = 23
	IQ6O = 24
	IQ8O = 25
	R10D = 26
	R118 = 27
	R1183 = 28
	R1184 = 29
	R11C = 30
	R11D = 31
	R11O = 32
	R11O3 = 33
	R11O4 = 34
	R12C = 35
	R12D = 36
	R13C = 37
	R13O = 38
	R14C = 39
	R214 = 40
	R218 = 41
	R21C = 42
	R21O = 43
	R22C = 44
	R23C = 45
	R23O = 46
	R24C = 47
	R258 = 48
	R318 = 49
	R31C = 50
	R31O = 51
	R32C = 52
	R33C = 53
	R33O = 54
	R34C = 55
	R418 = 56
	R41C = 57
	R41O = 58
	R42C = 59
	R43C = 60
	R43O = 61
	R44C = 62
	RA18 = 63
	RB14 = 64
	RB18 = 65
	RC18 = 66
	RD18 = 67
	RE18 = 68
	RF18 = 69
	RF1C = 70
	RF1O = 71
	RF2C = 72
	RF3C = 73
	RF3O = 74
	RF4C = 75
	RF5C = 76
	RF6C = 77
	RF7C = 78
	RF8C = 79
	RF9C = 80
	RFAC = 81
	RFAO = 82
	RFBC = 83
	RG18 = 84
	RH18 = 85


# noinspection SpellCheckingInspection
class TxConnectorBench(Enum):
	"""15 Members, R118 ... RH18"""
	R118 = 0
	R214 = 1
	R218 = 2
	R258 = 3
	R318 = 4
	R418 = 5
	RA18 = 6
	RB14 = 7
	RB18 = 8
	RC18 = 9
	RD18 = 10
	RE18 = 11
	RF18 = 12
	RG18 = 13
	RH18 = 14


# noinspection SpellCheckingInspection
class TxConnectorCmws(Enum):
	"""96 Members, R11 ... RH8"""
	R11 = 0
	R12 = 1
	R13 = 2
	R14 = 3
	R15 = 4
	R16 = 5
	R17 = 6
	R18 = 7
	R21 = 8
	R22 = 9
	R23 = 10
	R24 = 11
	R25 = 12
	R26 = 13
	R27 = 14
	R28 = 15
	R31 = 16
	R32 = 17
	R33 = 18
	R34 = 19
	R35 = 20
	R36 = 21
	R37 = 22
	R38 = 23
	R41 = 24
	R42 = 25
	R43 = 26
	R44 = 27
	R45 = 28
	R46 = 29
	R47 = 30
	R48 = 31
	RA1 = 32
	RA2 = 33
	RA3 = 34
	RA4 = 35
	RA5 = 36
	RA6 = 37
	RA7 = 38
	RA8 = 39
	RB1 = 40
	RB2 = 41
	RB3 = 42
	RB4 = 43
	RB5 = 44
	RB6 = 45
	RB7 = 46
	RB8 = 47
	RC1 = 48
	RC2 = 49
	RC3 = 50
	RC4 = 51
	RC5 = 52
	RC6 = 53
	RC7 = 54
	RC8 = 55
	RD1 = 56
	RD2 = 57
	RD3 = 58
	RD4 = 59
	RD5 = 60
	RD6 = 61
	RD7 = 62
	RD8 = 63
	RE1 = 64
	RE2 = 65
	RE3 = 66
	RE4 = 67
	RE5 = 68
	RE6 = 69
	RE7 = 70
	RE8 = 71
	RF1 = 72
	RF2 = 73
	RF3 = 74
	RF4 = 75
	RF5 = 76
	RF6 = 77
	RF7 = 78
	RF8 = 79
	RG1 = 80
	RG2 = 81
	RG3 = 82
	RG4 = 83
	RG5 = 84
	RG6 = 85
	RG7 = 86
	RG8 = 87
	RH1 = 88
	RH2 = 89
	RH3 = 90
	RH4 = 91
	RH5 = 92
	RH6 = 93
	RH7 = 94
	RH8 = 95


# noinspection SpellCheckingInspection
class TxConverter(Enum):
	"""40 Members, ITX1 ... TX44"""
	ITX1 = 0
	ITX11 = 1
	ITX12 = 2
	ITX13 = 3
	ITX14 = 4
	ITX2 = 5
	ITX21 = 6
	ITX22 = 7
	ITX23 = 8
	ITX24 = 9
	ITX3 = 10
	ITX31 = 11
	ITX32 = 12
	ITX33 = 13
	ITX34 = 14
	ITX4 = 15
	ITX41 = 16
	ITX42 = 17
	ITX43 = 18
	ITX44 = 19
	TX1 = 20
	TX11 = 21
	TX12 = 22
	TX13 = 23
	TX14 = 24
	TX2 = 25
	TX21 = 26
	TX22 = 27
	TX23 = 28
	TX24 = 29
	TX3 = 30
	TX31 = 31
	TX32 = 32
	TX33 = 33
	TX34 = 34
	TX4 = 35
	TX41 = 36
	TX42 = 37
	TX43 = 38
	TX44 = 39


# noinspection SpellCheckingInspection
class YesNoStatus(Enum):
	"""2 Members, NO ... YES"""
	NO = 0
	YES = 1
