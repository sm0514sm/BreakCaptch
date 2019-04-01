from PIL import Image, ImageFilter
lists = []
im = Image.open('CurrentImage.png')
px = im.load()
for i in range(im.height):
    for j in range(im.width):
        if px[j, i][3] != 255:
            px[j, i] = (0, 0, 0, 0,)
im.save("pixel_result0.png")
for i in range(im.height):
    for j in range(im.width):
        if len(lists) == 5:
            if px[j, i] not in lists:
                px[j, i] = (0, 0, 0, 0)
        else:
            if px[j, i] not in lists:
                if px[j, i] != px[218, i]:
                    lists.append(px[j, i])
im.save("pixel_result1.png")
for i in range(im.height):
    for j in range(im.width):
        if px[j, i] == (0, 0, 0, 0):
            px[j, i] = (255, 255, 255, 255)

for i in range(im.height):
    for j in range(im.width):
        print(px[j,i])
        if px[j, i] != (255, 255, 255, 255):
            px[j, i] = (0, 0, 0, 255)

print(im.width)
im.save("pixel_result2.png")
print(lists)
print(len(lists))