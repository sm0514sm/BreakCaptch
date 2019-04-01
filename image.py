from PIL import Image, ImageFilter
# TODO 코드 리팩토링

file_name = "CurrentImage (10)"
lists = []
im = Image.open(file_name + '.png')
print("width : %d, height : %d" % (im.width, im.height))
color_most_left_list = [im.width, im.width, im.width, im.width, im.width]
px = im.load()
for i in range(im.height):
    for j in range(im.width):
        if px[j, i][3] != 255:
            px[j, i] = (0, 0, 0, 0,)
# 블러 이미지 삭제
im.save("./image_test/" + file_name + "_0_blur_delete.png")

# 라인 삭제하기
seth = 0
for tmp_h in range(im.height):
    tmp_lists = []
    for tmp_w in range(im.width):
        if px[tmp_w, tmp_h] not in tmp_lists:
            if px[tmp_w, tmp_h] != (0, 0, 0, 0) and\
                    (px[tmp_w, tmp_h] == px[tmp_w+2, tmp_h] or px[tmp_w, tmp_h] == px[tmp_w-2, tmp_h]):
                tmp_lists.append(px[tmp_w, tmp_h])
    if len(tmp_lists) == 5:
        print("set height : %d" % tmp_h)
        print(tmp_lists)
        seth = tmp_h
        lists = tmp_lists
        break

for i in range(im.height):
    for j in range(im.width):
        if px[j, i] not in lists:   # 색상 리스트에 없으면 해당 색상은 삭제
            px[j, i] = (0, 0, 0, 0)
        else:                       # 색상 리스트에 있으면 해당 위치와 각 색깔 별 최소 x위치 판별
            for k in range(len(lists)):
                if px[j, i] == lists[k]:
                    color_most_left_list[k] = min(color_most_left_list[k], j)
im.save("./image_test/" + file_name + "_1_line_delete.png")
print(color_most_left_list)

# color_most_left_list 기준으로 숫자들 나누기
new0im = im.crop((color_most_left_list[0], 0, color_most_left_list[0] + 45, 45))
px0 = new0im.load()
new1im = im.crop((color_most_left_list[1], 0, color_most_left_list[1] + 45, 45))
px1 = new1im.load()
new2im = im.crop((color_most_left_list[2], 0, color_most_left_list[2] + 45, 45))
px2 = new2im.load()
new3im = im.crop((color_most_left_list[3], 0, color_most_left_list[3] + 45, 45))
px3 = new3im.load()
new4im = im.crop((color_most_left_list[4], 0, color_most_left_list[4] + 45, 45))
px4 = new4im.load()

this_image_color = ()
for j in range(45):
    if px0[j, seth] != (0, 0, 0, 0):
        this_image_color = px0[j, seth]  # 지금 이 방식 문제 있음, 가장 많은 색을 추출하는 식으로 해야할듯 # 반례 CurrentImage (8)
        print(this_image_color)
        break
for i in range(45):
    for j in range(45):
        if px0[j, i] != this_image_color:
            px0[j, i] = (255, 255, 255, 255)
        else:
            px0[j, i] = (0, 0, 0, 255)


this_image_color = ()
for j in range(45):
    if px1[j, seth] != (0, 0, 0, 0):
        this_image_color = px1[j, seth]
        print(this_image_color)
        break
for i in range(45):
    for j in range(45):
        if px1[j, i] != this_image_color:
            px1[j, i] = (255, 255, 255, 255)
        else:
            px1[j, i] = (0, 0, 0, 255)

this_image_color = ()
for j in range(45):
    if px2[j, seth] != (0, 0, 0, 0):
        this_image_color = px2[j, seth]
        print(this_image_color)
        break
for i in range(45):
    for j in range(45):
        if px2[j, i] != this_image_color:
            px2[j, i] = (255, 255, 255, 255)
        else:
            px2[j, i] = (0, 0, 0, 255)

this_image_color = ()
for j in range(45):
    if px3[j, seth] != (0, 0, 0, 0):
        this_image_color = px3[j, seth]
        print(this_image_color)
        break
for i in range(45):
    for j in range(45):
        if px3[j, i] != this_image_color:
            px3[j, i] = (255, 255, 255, 255)
        else:
            px3[j, i] = (0, 0, 0, 255)

this_image_color = ()
for j in range(45):
    if px4[j, seth] != (0, 0, 0, 0):
        this_image_color = px4[j, seth]
        break
for i in range(45):
    for j in range(45):
        if px4[j, i] != this_image_color:
            px4[j, i] = (255, 255, 255, 255)
        else:
            px4[j, i] = (0, 0, 0, 255)


# 이미지 흑백으로 변경
for i in range(im.height):
    for j in range(im.width):
        if px[j, i] == (0, 0, 0, 0):
            px[j, i] = (255, 255, 255, 255)

for i in range(im.height):
    for j in range(im.width):
        if px[j, i] != (255, 255, 255, 255):
            px[j, i] = (0, 0, 0, 255)

im.save("./image_test/" + file_name + "_2_make_blackwhite.png")
if len(lists) != 5:
    print("비정상 작동")

new0im.save("./image_test/" + file_name + "_result_0.png")
new1im.save("./image_test/" + file_name + "_result_1.png")
new2im.save("./image_test/" + file_name + "_result_2.png")
new3im.save("./image_test/" + file_name + "_result_3.png")
new4im.save("./image_test/" + file_name + "_result_4.png")