from .colordata.colordata import (
			Data, RGBData, HSLData, HSVData,
			fromHEX, fromRGB, fromHSL, fromHSV
		)
from .colordata.colornames import colornames
import re

class Color:
	__data: Data

	def __init__(self, *args, **kwargs):
		def testAlpha() -> float | None:
			alpha = None
			if 'alpha' in kwargs:
				alpha = kwargs['alpha']
				if not isinstance(alpha, float | None):
					raise ValueError('invalid alpha')
				if isinstance(alpha, float) and (alpha < 0 or alpha > 1):
					raise ValueError('alpha argument is not in allowed range')
			return alpha

		# default constructor (from string)
		if len(args):
			if len(args) > 1 or not isinstance(args[0], str):
				raise ValueError('default constructor allow only one string argument')
			color = args[0].strip().lower()

			# hex string
			if color.startswith('#'):
				self.__data = fromHEX(color)

			# string contains color name
			elif color in colornames:
				self.__data = fromHEX(colornames[color])

			# string looks like CSS RGB Value
			elif color.startswith('rgb'):
				alpha = None
				color = re.sub(r'(\(|\)|r|g|b|a|\s)', '', color).split(',')

				if 'alpha' in kwargs:
					alpha = testAlpha()
				else:
					if len(color) == 4:
						try:
							alpha = float(color[3])
						except Exception:
							raise ValueError('invalid alpha')
					if isinstance(alpha, float) and (alpha < 0 or alpha > 1):
						raise ValueError('invalid alpha')

				if len(color) < 3 or len(color) > 4:
					raise ValueError('invalid CSS RGB string')
				if any(not x.isdigit() for x in color[:3]):
					raise ValueError('invalid CSS RGB string')
				color = tuple(map(lambda x: int(x), color[:3]))
				if any(x < 0 or x > 255 for x in color):
					raise ValueError('invalid CSS RGB string')

				self.__data = RGBData((*map(lambda x: x/255, color), alpha))

			# string looks like CSS HSL Value
			elif color.startswith('hsl'):
				alpha = None
				color = re.sub(r'(\(|\)|h|s|l|a|\s)', '', color).split(',')

				if 'alpha' in kwargs:
					alpha = testAlpha()
				else:
					if len(color) == 4:
						try:
							alpha = float(color[3])
						except Exception:
							raise ValueError('invalid alpha')
					if isinstance(alpha, float) and (alpha < 0 or alpha > 1):
						raise ValueError('invalid alpha')

				if len(color) < 3 or len(color) > 4:
					raise ValueError('invalid CSS HSL string')
				if not color[0].isdigit():
					raise ValueError('invalid CSS HSL string')
				hue = int(color[0])
				if hue < 0 or hue > 360:
					raise ValueError('invalid CSS HSL string')
				if not color[1].endswith('%'):
					raise ValueError('invalid CSS HSL string')
				sat = int(color[1][:-1])
				if sat < 0 or sat > 100:
					raise ValueError('invalid CSS HSL string')
				if not color[2].endswith('%'):
					raise ValueError('invalid CSS HSL string')
				light = int(color[2][:-1])
				if light < 0 or light > 100:
					raise ValueError('invalid CSS HSL string')

				self.__data = HSLData((hue/360, sat/100, light/100, alpha))

			# string looks like LSL color
			elif color.startswith('<') and color.endswith('>'):
				alpha = testAlpha()
				color = re.sub(r'(^\<|\>$|\s)', '', color).split(',')

				if len(color) != 3:
					raise ValueError('invalid LSL color string')
				try:
					color = tuple(map(lambda x: float(x), color))
				except Exception:
					raise ValueError('invalid LSL color string')
				if any(x < 0 or x > 1 for x in color):
					raise ValueError('invalid LSL color string')

				self.__data = RGBData((*color, alpha))

			# unknown input string
			else:
				raise ValueError('invalid color string given to default constructor')

		# by red, green or/and blue constructor
		elif any(x in ('red', 'green', 'blue') for x in kwargs):
		# red, green or blue in kwargs
			red, green, blue, alpha = 0, 0, 0, testAlpha()
			if 'red' in kwargs:
				red = kwargs['red']
			if 'green' in kwargs:
				green = kwargs['green']
			if 'blue' in kwargs:
				blue = kwargs['blue']

			if any(not isinstance(x, int | float) for x in (red, green, blue)):
				raise ValueError('invalid argument given to red, green or/and blue constructor')

			self.__data = fromRGB(red, green, blue, alpha)

		# by hue, sat or/and light HSL constructor
		elif any(x in ('hslHue', 'hslSat', 'hslLight') for x in kwargs):
			hue, sat, light, alpha = 0.0, 1.0, 0.5, testAlpha()
			if 'hslHue' in kwargs:
				hue = kwargs['hslHue']
			if 'hslSat' in kwargs:
				sat = kwargs['hslSat']
			if 'hslLight' in kwargs:
				light = kwargs['hslLight']

			if any(not isinstance(x, int | float) for x in (hue, sat, light)):
				raise ValueError('invalid argument given to hue, sat or/and light HSL constructor')

			self.__data = fromHSL(hue, sat, light, alpha)

		# by hue, sat or/and value HSV constructor
		elif any(x in ('hsvHue', 'hsvSat', 'hsvValue') for x in kwargs):
			hue, sat, value, alpha = 0.0, 1.0, 1.0, testAlpha()
			if 'hsvHue' in kwargs:
				hue = kwargs['hsvHue']
			if 'hsvSat' in kwargs:
				sat = kwargs['hsvSat']
			if 'hsvLight' in kwargs:
				value = kwargs['hsvValue']

			if any(not isinstance(x, int | float) for x in (hue, sat, value)):
				raise ValueError('invalid argument given to hue, sat or/and value HSV constructor')

			self.__data = fromHSV(hue, sat, value, alpha)

		# input data not found in arguments
		else:
			raise ValueError('invalid arguments')

	def __str__(self) -> str:
		try:
			return f'{self.__class__.__name__}({self.__data})'
		except AttributeError:
			return f'{self.__class__.__name__}()'

	def __repr__(self) -> str:
		return str(self)

	@property
	def _data(self) -> Data:
		return self.__data

	@property
	def alpha(self) -> float | None:
		return self.__data.alpha

	@alpha.setter
	def alpha(self, alpha: float | None = None):
		if not isinstance(alpha, float | None):
			raise ValueError('invalid type of alpha argument')
		self.__data.alpha = alpha

	# attributes as RGB
	@property
	def red(self) -> int:
		return round(self.__data.asRGB().red * 255)

	@red.setter
	def red(self, red: int):
		if red < 0 or red > 255:
			raise ValueError('invalid value')
		rgb = list(self.__data.asRGB())
		rgb[0] = red/255
		self.__data = RGBData(rgb)

	@property
	def green(self) -> int:
		return round(self.__data.asRGB().green * 255)

	@green.setter
	def green(self, green: int):
		if green < 0 or green > 255:
			raise ValueError('invalid value')
		rgb = list(self.__data.asRGB())
		rgb[1] = green/255
		self.__data = RGBData(rgb)

	@property
	def blue(self) -> int:
		return round(self.__data.asRGB().blue * 255)

	@blue.setter
	def blue(self, blue: int):
		if blue < 0 or blue > 255:
			raise ValueError('invalid value')
		rgb = list(self.__data.asRGB())
		rgb[2] = blue/255
		self.__data = RGBData(rgb)
	
	@property
	def rgb(self) -> tuple[int, int, int]:
		return tuple(map(lambda num: round(num * 255), self.__data.asRGB()[:3]))

	@rgb.setter
	def rgb(self, rgb: tuple[int, int, int]):
		if any(x > 255 for x in rgb) or any(x < 0 for x in rgb):
			raise ValueError('invalid value')
		val = list(map(lambda num: num / 255, rgb))
		val.append(self.alpha)
		self.__data = RGBData(tuple(val))

	# attributes as HSL
	@property
	def hslHue(self) -> int:
		return round(self.__data.asHSL().hue * 360)

	@hslHue.setter
	def hslHue(self, hslHue: int):
		if hslHue < 0 or hslHue > 360:
			raise ValueError('invalid value')
		hsl = list(self.__data.asHSL())
		hsl[0] = hslHue/360
		self.__data = HSLData(hsl)

	@property
	def hslSat(self) -> int:
		return round(self.__data.asHSL().sat * 100)

	@hslSat.setter
	def hslSat(self, hslSat: int):
		if hslSat < 0 or hslSat > 100:
			raise ValueError('invalid value')
		hsl = list(self.__data.asHSL())
		hsl[1] = hslSat/100
		self.__data = HSLData(hsl)

	@property
	def hslLight(self) -> int:
		return round(self.__data.asHSL().light * 100)

	@hslLight.setter
	def hslLight(self, hslLight: int):
		if hslLight < 0 or hslLight > 100:
			raise ValueError('invalid value')
		hsl = list(self.__data.asHSL())
		hsl[2] = hslLight/100
		self.__data = HSLData(hsl)

	# attributes as HSV
	@property
	def hsvHue(self) -> int:
		return round(self.__data.asHSV().hue * 360)

	@hsvHue.setter
	def hsvHue(self, hsvHue: int):
		if hsvHue < 0 or hsvHue > 360:
			raise ValueError('invalid value')
		hsv = list(self.__data.asHSV())
		hsv[0] = hsvHue/360
		self.__data = HSVData(hsv)

	@property
	def hsvSat(self) -> int:
		return round(self.__data.asHSV().sat * 100)

	@hsvSat.setter
	def hsvSat(self, hsvSat: int):
		if hsvSat < 0 or hsvSat > 100:
			raise ValueError('invalid value')
		hsv = list(self.__data.asHSV())
		hsv[1] = hsvSat/100
		self.__data = HSVData(hsv)

	@property
	def hsvValue(self) -> int:
		return round(self.__data.asHSV().value * 100)

	@hsvValue.setter
	def hsvValue(self, hsvValue: int):
		if hsvValue < 0 or hsvValue > 100:
			raise ValueError('invalid value')
		hsv = list(self.__data.asHSV())
		hsv[2] = hsvValue/100
		self.__data = HSVData(hsv)

	# represent as hex string
	def asHEX(self, dropAlpha = False) -> str:
		ret = '#' + ''.join(tuple(map(lambda h: f'{h:02x}', self.rgb)))
		if not dropAlpha and isinstance(self.alpha, float):
			ret += f'{round(self.alpha * 255):02x}'
		return ret

	# get name of color if exist
	def asName(self) -> str | None:
		try:
			return list(filter(lambda x: colornames[x] == self.asHEX(True), colornames))[0]
		except IndexError:
			return None
	
	# represent as LSL color vector
	def asLSL(self) -> str:
		return str(self.__data.asRGB()[:3]).replace('(', '<').replace(')', '>')

	#represent as CSS RGB value
	def asCSSRGB(self, dropAlpha = False) -> str:
		rgb = 'rgb'
		ret: list[int | float] = list(self.rgb)
		if not dropAlpha and isinstance(self.alpha, float):
			ret.append(self.alpha)
			rgb += 'a'
		return f'{rgb}{tuple(ret)}'

	#represent as CSS HSL value
	def asCSSHSL(self, dropAlpha = False) -> str:
		hsl = 'hsl'
		ret: list[int | str | float] = list()
		ret.append(round(self.__data.asHSL().hue * 360))
		ret.append(f'{round(self.__data.asHSL().sat * 100)}%')
		ret.append(f'{round(self.__data.asHSL().light * 100)}%')
		if not dropAlpha and isinstance(self.alpha, float):
			ret.append(self.alpha)
			hsl += 'a'
		return f'{hsl}{tuple(ret)}'.replace("'", '')

	def asRGB(self, dropAlpha = False)\
				-> tuple[float, float, float] | tuple[float, float, float, float | None]:
		if dropAlpha:
			return self.__data.asRGB()[:3]
		return self.__data.asRGB()

	def asHSL(self, dropAlpha = False)\
				-> tuple[float, float, float] | tuple[float, float, float, float | None]:
		if dropAlpha:
			return self.__data.asHSL()[:3]
		return self.__data.asHSL()

	def asHSV(self, dropAlpha = False)\
				-> tuple[float, float, float] | tuple[float, float, float, float | None]:
		if dropAlpha:
			return self.__data.asHSV()[:3]
		return self.__data.asHSV()
