from PIL import Image


CLEAR = (0, 0, 0, 0)            # 투명
WHITE = (255, 255, 255, 255)    # 흰색
BLACK = (0, 0, 0, 255)          # 검정


# TODO 각 함수별로 에러처리 필요


# 블러 픽셀 제거 (alpha 값이 255가 아니면 삭제)
def blur_pixel_delete(image, pixel):
    for y in range(image.height):
        for x in range(image.width):
            if pixel[x, y][3] != 255:
                pixel[x, y] = CLEAR
    image.save("./image_test/" + file_name + "_0_blur_delete.png")


# 라인 삭제하기 (blur_pixel_delete 미리 해야함)
def line_delete(image, pixel):
    spe_h = 0

    # 다섯가지 색상만이 존재하는 special_height 구하기
    for y in range(image.height):
        global color_lists
        color_lists = []
        for x in range(image.width):
            if pixel[x, y] not in color_lists:
                if pixel[x, y] != CLEAR and\
                        (pixel[x, y] == pixel[x+2, y] or pixel[x, y] == pixel[x-2, y]):
                    color_lists.append(pixel[x, y])
        if len(color_lists) == 5:
            spe_h = y
            print("special_height : %d" % y)
            break

    # color_lists에 없는 색상 삭제, 있는 색상은 각 색상 별 최소 x 위치
    for y in range(image.height):
        for x in range(image.width):
            if px[x, y] not in color_lists:     # 색상 리스트에 없으면 해당 색상은 삭제
                px[x, y] = CLEAR
            else:                               # 색상 리스트에 있으면 해당 위치와 각 색깔 별 최소 x위치 판별
                for i in range(len(color_lists)):
                    if px[x, y] == color_lists[i]:
                        color_most_left_list[i] = min(color_most_left_list[i], x)
    im.save("./image_test/" + file_name + "_1_line_delete.png")

    return spe_h


# 문자 색상별로 5개로 나누기
# bbox = (x, y, width+x, height+y)
# spe_h = special_height
def character_separate(image, bbox, spe_h, naming):
    new_image = image.crop(bbox)
    new_pixel = new_image.load()

    # TODO bbox 범위 초과시 에러 출력 종료

    # 자른 이미지 글자의 주 색상 찾기
    this_image_color = ()
    for x in range(new_image.width):
        if new_pixel[x, spe_h] != CLEAR:
            this_image_color = new_pixel[x, spe_h]  # TODO 지금 이 방식 문제 있음, 가장 많은 색을 추출하는 식으로 해야할듯, 반례 CurrentImage (8)
            print(naming, "색상 :", this_image_color)
            break

    # 해당 색상은 검정색으로, 나머지는 흰색으로
    for y in range(new_image.height):
        for x in range(new_image.width):
            if new_pixel[x, y] != this_image_color:
                new_pixel[x, y] = WHITE
            else:
                new_pixel[x, y] = BLACK

    new_image.save("./image_test/" + file_name + "_result_" + naming + ".png")


# ------------------------------------------------------------------------------------------------------------------- #


file_name = "CurrentImage (7)"
color_lists = []
im = Image.open(file_name + '.png')
print("width  : %d\nheight : %3d" % (im.width, im.height))
color_most_left_list = [im.width, im.width, im.width, im.width, im.width]
px = im.load()

blur_pixel_delete(im, px)

special_height = line_delete(im, px)
print("색상 별 최소 x값 : ", color_most_left_list)

num = 0
for most_left in color_most_left_list:
    character_separate(im, (most_left, 0, most_left + 60, 45), special_height, str(num))
    num += 1

if len(color_lists) != 5:
    print("비정상 작동")

