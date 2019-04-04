from PIL import Image
import os


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
    image.save(save_dir + "/" + file_name[:5] + "_0_blur_delete.png")


# TODO XCCGN 에서 라인이 정상적으로 삭제되지 않음
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
    im.save(save_dir + "/" + file_name[:5] + "_1_line_delete.png")

    return spe_h


# 문자 색상별로 5개로 나누기
# bbox = (x, y, width+x, height+y)
# spe_h = special_height
def character_separate(image, bbox, spe_h, naming):
    new_image = image.crop(bbox)
    new_pixel = new_image.load()

    # TODO bbox 범위 초과시 에러 출력 종료

    # 자른 이미지 글자의 주 색상 찾기
    # TODO 지금 이 방식 문제 있음, 가장 많은 색을 추출하는 식으로 해야할듯,
    this_image_color = ()
    for x in range(new_image.width):
        if new_pixel[x, spe_h] != CLEAR:
            this_image_color = new_pixel[x, spe_h]  # TODO XCCGN, XMGYO, YLLHJ
            print(naming, "색상 :", this_image_color)
            break

    # 해당 색상은 검정색으로, 나머지는 흰색으로
    for y in range(new_image.height):
        for x in range(new_image.width):
            if new_pixel[x, y] != this_image_color:
                new_pixel[x, y] = WHITE
            else:
                new_pixel[x, y] = BLACK

    new_image.save(save_dir + "/" + file_name[:5] + "_result_" + naming + ".png")
    print(save_dir + "/" + file_name[:5] + "_result_" + naming + ".png" + ">> 생성")


# ------------------------------------------------------------------------------------------------------------------- #


path_dir = "./보안문자/"    # >> 이미지 파일이 있는 디렉토리
save_dir = ""               # >> 수정금지

error_count = 0

file_list = os.listdir(path_dir)
file_list.sort()

for file_name in file_list:
    color_lists = []    # 해당 이미지의 5가지 문자 각각의 색 (R, G, B, A) 리스트

    if os.path.isdir(path_dir + file_name):  # 디렉토리일 경우 넘김
        continue
    im = Image.open(path_dir + file_name)
    px = im.load()
    save_dir = path_dir + file_name[:5]      # ex) ./보안문자/ABCDE
    if not os.access(save_dir, os.F_OK):     # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(save_dir)

    color_most_left_list = [im.width for i in range(5)]

    blur_pixel_delete(im, px)
    special_height = line_delete(im, px)

    num = 0
    for most_left in color_most_left_list:
        character_separate(im, (most_left, 0, most_left + 60, 45), special_height, str(num))
        num += 1

    if len(color_lists) != 5:
        error_count += 1
    print()


print("""
Test Image Files Count = %d
Error Count            = %3d""" % (len(file_list), error_count))
