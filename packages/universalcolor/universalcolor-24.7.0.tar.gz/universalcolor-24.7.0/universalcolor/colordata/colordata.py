import colorsys
from abc import ABC, abstractmethod, abstractproperty
from typing import NamedTuple


def hsv_to_hsl(hsv: tuple[float, float, float]) -> tuple[float, float, float]:
	h, s, v = hsv
	l = v * (1 - s/2)
	s = 0 if l in (0, 1) else (v - l)/min(l, 1-l)
	return (h, s, l)


def hsl_to_hsv(hsl: tuple[float, float, float]) -> tuple[float, float, float]:
	h, s, l = hsl
	v = l + s * min(l, 1-l)
	s = 0 if v == 0 else 2*(1 - l/v)
	return (h, s, v)


# internal data containers
class RGB(NamedTuple):
	red: float
	green: float
	blue: float
	alpha: float | None = None

class HSL(NamedTuple):
	hue: float
	sat: float
	light: float
	alpha: float | None = None

class HSV(NamedTuple):
	hue: float
	sat: float
	value: float
	alpha: float | None = None

# abstract internal data interface
class Data(ABC):
	__data: tuple

	@abstractproperty
	def _data(self) -> tuple:
		raise NotImplementedError

	def __str__(self) -> str:
		return f'{self._data}'

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}({str(self)})'

	# get data as RGB and convert if needed
	@abstractmethod
	def asRGB(self) -> RGB:
		raise NotImplementedError

	# get data as HSL and convert if needed
	@abstractmethod
	def asHSL(self) -> HSL:
		raise NotImplementedError

	# get data as HSV and convert if needed
	@abstractmethod
	def asHSV(self) -> HSV:
		raise NotImplementedError

	@property
	def alpha(self) -> float | None:
		return self._data[3]

	@alpha.setter
	def alpha(self, alpha: float | None):
		if not isinstance(alpha, float | None):
			raise ValueError('invalid type of alpha argument')
		if isinstance(alpha, float) and (alpha < 0 or alpha > 1):
			raise ValueError('alpha is not in range')
		dt = type(self._data)
		self._data = dt(*self._data[:3], alpha)

# RGB data interface implementation
class RGBData(Data):
	__data: RGB

	@property
	def _data(self) -> RGB:
		return self.__data

	@_data.setter
	def _data(self, data: RGB):
		self.__data = data

	def __init__(self, color: tuple[float, float, float, float | None] | RGB) -> None:
		for c in color[:3]:
			if not isinstance(c, float) or c < 0 or c > 1:
				raise ValueError('is not rgb color')
		if len(color) == 4:
			if isinstance(color[3], float) and (color[3] < 0 or color[3] > 1):
				raise ValueError('invalid alpha')
			elif color[3] is not None and not isinstance(color[3], float):
				raise ValueError('invalid alpha')

		self.__data = RGB(*color)

	def asRGB(self) -> RGB:
		return self.__data

	def asHSL(self) -> HSL:
		ret: list[float | None] = [*colorsys.rgb_to_hls(*self.__data[:3])]
		#reorder HLS to HSL
		ret = [ret[0], ret[2], ret[1], self.__data.alpha]

		for i in range(len(ret)):
			if isinstance(ret[i], float):
				if ret[i] < 0:
					ret[i] = 0.0
				elif ret[i] > 1:
					ret[i] = 1.0
		return HSL(*ret)

	def asHSV(self) -> HSV:
		ret = [*colorsys.rgb_to_hsv(*self.__data[:3]), self.__data.alpha]

		for i in range(len(ret)):
			if isinstance(ret[i], float):
				if ret[i] < 0:
					ret[i] = 0.0
				elif ret[i] > 1:
					ret[i] = 1.0
		return HSV(*ret)


# HSL data interface implementation
class HSLData(Data):
	__data: HSL

	@property
	def _data(self) -> HSL:
		return self.__data

	@_data.setter
	def _data(self, data: HSL):
		self.__data = data

	def __init__(self, color: tuple[float, float, float, float | None] | HSL) -> None:
		for c in color[:3]:
			if not isinstance(c, float) or c < 0 or c > 1:
				raise ValueError('is not rgb color')
		if len(color) == 4:
			if isinstance(color[3], float) and (color[3] < 0 or color[3] > 1):
				raise ValueError('invalid alpha')
			elif color[3] is not None and not isinstance(color[3], float):
				raise ValueError('invalid alpha')

		self.__data = HSL(*color)

	def asRGB(self) -> RGB:
		ret = [self.__data.hue, self.__data.light, self.__data.sat]
		ret = [*colorsys.hls_to_rgb(*ret), self.__data.alpha]

		# correction of inaccuracy in colorsys
		for i in range(len(ret)):
			if isinstance(ret[i], float):
				if ret[i] < 0:
					ret[i] = 0.0
				elif ret[i] > 1:
					ret[i] = 1.0
		return RGB(*ret)

	def asHSL(self) -> HSL:
		return self.__data

	def asHSV(self) -> HSV:
		ret = [*hsl_to_hsv(self.__data[:3]), self.__data.alpha]
		# correction of inaccuracy in colorsys
		for i in range(len(ret)):
			if isinstance(ret[i], float):
				if ret[i] < 0:
					ret[i] = 0.0
				elif ret[i] > 1:
					ret[i] = 1.0
		return HSV(*ret)


# HSV data interface implementation
class HSVData(Data):
	__data: HSV

	@property
	def _data(self) -> HSV:
		return self.__data

	@_data.setter
	def _data(self, data: HSV):
		self.__data = data

	def __init__(self, color: tuple[float, float, float, float | None] | HSV) -> None:
		for c in color[:3]:
			if not isinstance(c, float) or c < 0 or c > 1:
				raise ValueError('is not rgb color')
		if len(color) == 4:
			if isinstance(color[3], float) and (color[3] < 0 or color[3] > 1):
				raise ValueError('invalid alpha')
			elif color[3] is not None and not isinstance(color[3], float):
				raise ValueError('invalid alpha')

		self.__data = HSV(*color)

	def asRGB(self) -> RGB:
		ret = [*colorsys.hsv_to_rgb(*self.__data[:3]), self.__data.alpha]

		# correction of inaccuracy in colorsys
		for i in range(len(ret)):
			if isinstance(ret[i], float):
				if ret[i] < 0:
					ret[i] = 0.0
				elif ret[i] > 1:
					ret[i] = 1.0
		return RGB(*ret)

	def asHSL(self) -> HSL:
		ret = [*hsv_to_hsl(self.__data[:3]), self.__data.alpha]
		# correction of inaccuracy in colorsys
		for i in range(len(ret)):
			if isinstance(ret[i], float):
				if ret[i] < 0:
					ret[i] = 0.0
				elif ret[i] > 1:
					ret[i] = 1.0
		return HSV(*ret)


	def asHSV(self) -> HSV:
		return self.__data


# gen Data object from RGB values
def fromRGB(red: int | float, green: int | float, blue: int | float, alpha: float | None = None):
	if isinstance(red, int):
		red /= 255
	if isinstance(green, int):
		green /= 255
	if isinstance(blue, int):
		blue /= 255

	test = [red, green, blue]
	if isinstance(alpha, float):
		test = [red, green, blue, alpha]
	if any(x < 0 or x > 1 for x in test):
		raise ValueError('invalid red, green, blue or/and alpha')

	return RGBData((red, green, blue, alpha))


# gen Data object from hex string
def fromHEX(color: str) -> Data:
	val = color.strip()
	if not val.startswith('#'):
		raise ValueError('invalid hex color')
	n = len(val)

	short = False
	if n == 4 or n == 5:
		short = True
	val = val[1:]
	if short:
		long = ''
		for v in val:
			long += v*2
		val = long

	n = len(val)
	if n != 6 and n != 8:
		raise ValueError('invalid hex color')

	return fromRGB(*tuple(int(''.join(tbyte), 16) for tbyte in zip(val[::2], val[1::2])))


# gen Data object from HSL values
def fromHSL(hue: int | float, sat: int | float, light: int | float, alpha: float | None = None):
	if isinstance(hue, int):
		hue /= 360
	if isinstance(sat, int):
		sat /= 100
	if isinstance(light, int):
		light /= 100

	test = [hue, sat, light]
	if isinstance(alpha, float):
		test = [hue, sat, light, alpha]
	if any(x < 0 or x > 1 for x in test):
		raise ValueError('invalid hue, sat, light or/and alpha')

	return HSLData((hue, sat, light, alpha))


# gen Data object from HSV values
def fromHSV(hue: int | float, sat: int | float, value: int | float, alpha: float | None = None):
	if isinstance(hue, int):
		hue /= 360
	if isinstance(sat, int):
		sat /= 100
	if isinstance(value, int):
		value /= 100

	test = [hue, sat, value]
	if isinstance(alpha, float):
		test = [hue, sat, value, alpha]
	if any(x < 0 or x > 1 for x in test):
		raise ValueError('invalid hue, sat, value or/and alpha')

	return HSVData((hue, sat, value, alpha))
