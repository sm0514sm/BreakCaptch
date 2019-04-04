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
    for y in range(5, image.height):
        global color_lists
        color_lists = []
        for x in range(image.width):
            if pixel[x, y] not in color_lists:
                if pixel[x, y] != CLEAR and\
                        (pixel[x, y] == pixel[x+2, y] or pixel[x, y] == pixel[x-2, y]):
                    color_lists.append(pixel[x, y])
                    print("x, y = ", x, y)
                    print("해당 좌표 색 = ", pixel[x, y])
        if len(color_lists) == 5:
            spe_h = y
            if "XCCGN" in file_name:
                print("XCCGN Test")
                print("special_height : %d" % y)
                print(color_lists)
            break

    # color_lists 에 없는 색상 삭제, 있는 색상은 각 색상 별 최소 x 위치
    for y in range(image.height):
        for x in range(image.width):
            if px[x, y] not in color_lists:     # 색상 리스트에 없으면 해당 색상은 삭제
                px[x, y] = CLEAR
            else:                               # 색상 리스트에 있으면 해당 위치와 각 색깔 별 최소, 최대 x위치 판별
                for i in range(len(color_lists)):
                    if px[x, y] == color_lists[i]:
                        color_most_left_list[i] = min(color_most_left_list[i], x)
                        color_most_right_list[i] = max(color_most_right_list[i], x)
    im.save(save_dir + "/" + file_name[:5] + "_1_line_delete.png")

    return spe_h


# 문자 색상별로 5개로 나누기
# bbox = (x, y, width+x, height+y)
# spe_h = special_height
def character_separate(image, bbox, naming, char):
    new_image = image.crop(bbox)
    new_pixel = new_image.load()

    # TODO bbox 범위 초과시 에러 출력 종료

    # 자른 이미지 글자의 주 색상 찾기
    this_image_color = ()
    new_color_dicts = {}
    for y in range(new_image.height):
        for x in range(new_image.width-1, 0, -1):
            if new_pixel[x, y] != CLEAR:
                if new_pixel[x, y] not in new_color_dicts.keys():
                    new_color_dicts[new_pixel[x, y]] = 1
                else:
                    new_color_dicts[new_pixel[x, y]] += 1
    max_value = max(new_color_dicts.values())
    for color_dict in new_color_dicts:
        if new_color_dicts[color_dict] == max_value:
            this_image_color = color_dict
            break

    # for x in range(new_image.width):
    #     if new_pixel[x, spe_h] is not CLEAR:
    #         this_image_color = new_pixel[x, spe_h]  # TODO XCCGN
    #         print(naming, "색상 :", this_image_color)
    #         break

    # 해당 색상은 검정색으로, 나머지는 흰색으로
    for y in range(new_image.height):
        for x in range(new_image.width):
            if new_pixel[x, y] != this_image_color:
                new_pixel[x, y] = WHITE
            else:
                new_pixel[x, y] = BLACK

    new_image.save(save_dir + "/" + file_name[:5] + "_result_" + naming + ".png")
    # print(save_dir + "/" + file_name[:5] + "_result_" + naming + ".png" + " >> 생성")
    if not os.access(path_dir + "train", os.F_OK):
        os.mkdir(path_dir + "train")
    if not os.access(path_dir + "train/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + "train/" + char)
    new_image.save(path_dir + "train/" + char + "/" + file_name[:5] + "_result_" + naming + ".png")
    # print(path_dir + "train/" + char + "/" + file_name[:5] + "_result_" + naming + ".png" + " >> 생성")


# ------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    path_dir = "./보안문자/"    # >> 이미지 파일이 있는 디렉토리
    save_dir = ""               # >> 수정금지
    error_count = 0

    file_list = os.listdir(path_dir)
    file_list.sort()
    image_count = 0
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
        color_most_right_list = [0 for i in range(5)]

        blur_pixel_delete(im, px)
        special_height = line_delete(im, px)

        num = 0
        for num in range(5):
            character_separate(im, (color_most_left_list[num], 0, color_most_right_list[num], 45),
                               str(num), file_name[num])
            num += 1

        if len(color_lists) != 5:
            error_count += 1
        image_count += 1

    print("""
    ----------------------------
    Test Image Files Count = %d
    Error Count            = %2d""" % (image_count, error_count))
