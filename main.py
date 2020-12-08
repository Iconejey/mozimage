from os import listdir, system
from PIL import Image as im, ImageDraw as imdrw
from random import choice, randint as rd

REF_PATH = 'gitans.jpg'
PATH = 'D:/gitans/'
EXTENTIONS = ['png', 'jpg', 'jpeg', 'gif']
SCALE = 50 # Taille des carrés
DIVS = 200  # Nombre d'images en hauteur
BACKGROUND = False
MOSAIC = True
RANGE = 10
DOTS = False

if __name__ == "__main__":
	system('cls')

	files = listdir(PATH)
	print(f'Loading \033[35m{len(files)}\033[0m images from \033[35m{PATH}\033[0m...')
	
	ignored_ext = set()
	images = {}
	for i, file in enumerate(files):
		ext = file.split('.')[-1]
		print(f'Computing \033[32m{i + 1}\033[35m/{len(files)}\033[0m [\033[35m{100 * (i + 1) // len(files)}%\033[0m] images and got \033[32m{len(images)}\033[0m colors with \033[32m{sum(len(l) for k, l in images.items())}\033[0m images...', end = ' ' * 20 + '\r')

		if MOSAIC and ext in EXTENTIONS:
			imgb = im.open(PATH + file)
			imgr =  im.new('RGB', (SCALE, SCALE))
			cW, cH = imgb.size
			moy = 0
			for x in range(SCALE):
				for y in range(SCALE):
					size = min(cH, cW)
					coords = int(x/SCALE * size), int(y/SCALE*size)
					p = imgb.getpixel(coords)

					if type(p) == tuple:
						c = sum(p) // 3
					else:
						# print(f'\n\033[31mNot RGB file: {file}', p, '\033[0m\n')
						c = p

					imgr.putpixel((x, y), (c, c, c))
					moy += c

			moy = moy//SCALE**2

			if not moy in images:
				images[moy] = []
			images[moy].append(imgr)
		else:
			ignored_ext.add(ext)
		
	print(f'\n\033[30;1mIgnored \033[31m{len(ignored_ext)}\033[30;1m extentions:', *ignored_ext, '\033[0m\n')

	try:
		ref = im.open(REF_PATH)
	except FileNotFoundError:
		print(f'\033[31mCould not open {REF_PATH}\033[0m\n')
		exit()


	refW, refH = ref.size
	W, H = DIVS * refW // refH, DIVS
	res = im.new('RGB', (W * SCALE, H * SCALE), (255, 255, 255))
	print(res.size, '\n')

	ctx = imdrw.Draw(res)
	for x in range(W):
		print(f'Drawing... \033[35m{100 * x // W}%\033[0m ({sum(len(l) for k, l in images.items())} images)', end = ' '*20 + '\r')
		for y in range(H):
			coords = int(x / W * refW), int(y / H * refH)
			
			c = sum(ref.getpixel(coords))//3
			
			x1 = x * SCALE
			y1 = y * SCALE

			if BACKGROUND:
				x2 = (x+1) * SCALE
				y2 = (y+1) * SCALE
				ctx.rectangle([x1, y1, x2, y2], fill = (c, c, c), width = 0)

			if MOSAIC and len(images):
				dist, key = 255, 0
				for k in images:
					if abs(c - k) < dist:
						dist = abs(c - k)
						key = k

				res.paste(choice(images[key]), (x1, y1))

			if DOTS:
				c = 255 - c
				for i in range(int((c + 1) / 255 * SCALE * SCALE)):
					px = x1 + rd(0, SCALE)
					py = y1 + rd(0, SCALE)
					p = rd(0, 16)
					ctx.rectangle([px, py, px, py], fill = (p, p, p), width = 0)

	print(f'\nSaving res.png...')
	res.save('D:/res.png')

	print(f'Opening res.png...\n')
	system('D:/res.png')