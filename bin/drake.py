from io import BytesIO
from os.path import abspath, split as path_split
from random import randint

from PIL import Image, ImageDraw, ImageFont
from telegram.ext.dispatcher import run_async

from .utils.logs import log_command

bin_path = path_split(abspath(__file__))[0]
font = ImageFont.truetype(f'{bin_path}/Resources/Fonts/raleway.ttf', 32)


@run_async
def drake(update, a, b):
	m = (
		('Drake',
		'AgADBQADSqgxG389uVR-bHcoBwTVCS6b1jIABJJj5XBpGQAB92oPAgABAg'),
		('Drake',
		'AgADBQADSqgxG389uVR-bHcoBwTVCS6b1jIABJJj5XBpGQAB92oPAgABAg'),
		('Robbie', 'AgADBQADS6gxG389uVT6Q3H5BIllKdWp1jIABDMXCOcwpqnScQ0CAAEC'),
		('Babushka',
		'AgADBQADTKgxG389uVRAb8NE7vNARc2w1jIABGAXUUGUqUG5zRMCAAEC')
	)[randint(0, 3)]

	bio = BytesIO()
	img = Image.open(f'{bin_path}/Resources/Drake/%s.png' % m[0])
	draw = ImageDraw.Draw(img)

	if not __draw_text(draw, a, 129) or not __draw_text(draw, b, 387):
		update.message.reply_photo(m[1], quote=True)

	img.save(bio, 'PNG')
	bio.seek(0)
	update.message.reply_photo(bio, quote=True)
	log_command(update, 'DRAKE')


# @jit(fastmath=True)
def __get_lines(t):
	w, _ = font.getsize(t)
	if w <= 320:
		return [t]
	t = t.split()
	for i in range(len(t), -1, -1):
		w, _ = font.getsize(' '.join(t[:i]))
		if w <= 320:
			return [" ".join(t[:i])] + __get_lines(" ".join(t[i:]))

	raise ValueError


# for i in range(len(t[0]), -1, -1):
# 	w, _ = font.getsize("".join(t[:i]))
# 	if w <= 320:
# 		return (
# 			["".join(t[0][:i])] +
# 			__get_lines(" ".join(["".join(t[0][i:])] + t[1:]))
# 		)


def __draw_text(draw, t, y):
	t = t.strip()
	w, h = font.getsize(t)

	if w <= 320:
		draw.text((480 - (w / 2), y - (h / 2)), t, (255, 255, 255), font=font)
		return True

	try:
		lines = __get_lines(t)
	except ValueError:
		return False
	num_lines = len(lines)
	dims = [font.getsize(x) for x in lines]
	ws, hs = [x[0] for x in dims], [x[1] for x in dims]
	total = sum(hs)

	if total > 258:
		return False

	h = y - (total / 2)
	for i in range(num_lines):
		draw.text((480 - (ws[i] / 2), h), lines[i], (255, 255, 255), font=font)
		h += hs[i]

	return True
