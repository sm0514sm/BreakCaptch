from PIL import Image
import os


CLEAR = (0, 0, 0, 0)            # 투명
WHITE = (255, 255, 255, 255)    # 흰색
BLACK = (0, 0, 0, 255)          # 검정

MAX_WIDTH = 60
TEST_NUM = 2   # 주의 : 5개밖에 없는 문자있음. Train 도 고려해야함.


# 블러 픽셀 제거 (alpha 값이 255가 아니면 삭제)
def blur_pixel_delete(image, pixel):
    for y in range(image.height):
        for x in range(image.width):
            if pixel[x, y][3] != 255:
                pixel[x, y] = CLEAR


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
        if len(color_lists) == 5:
            spe_h = y
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
    return spe_h


# 흑백 + 크기일정 + 라인삭제
# bbox = (x, y, width+x, height+y)
# spe_h = special_height
# save_dir_name = 최종적으로 생성될 폴더명 --> ./보안문자/save_dir_name/A..Z/ABCDE.jpg
def character_separate(image, bbox, naming, char, save_dir_name):
    new_image = image.crop(bbox)
    new_pixel = new_image.load()
    bg_image = Image.new("RGB", (MAX_WIDTH, new_image.height), WHITE)

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

    # 해당 색상은 검정색으로, 나머지는 흰색으로
    for y in range(new_image.height):
        for x in range(new_image.width):
            if new_pixel[x, y] != this_image_color:
                new_pixel[x, y] = WHITE
            else:
                new_pixel[x, y] = BLACK
    bg_image.paste(new_image, (0, 0, new_image.width, new_image.height))
    new_image = bg_image
    if not os.access(path_dir + save_dir_name, os.F_OK):
        os.mkdir(path_dir + save_dir_name)
    if not os.access(path_dir + save_dir_name + "/train/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/train/")
    if not os.access(path_dir + save_dir_name + "/test/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/test/")
    if not os.access(path_dir + save_dir_name + "/train/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/train/" + char)
    if not os.access(path_dir + save_dir_name + "/test/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/test/" + char)
    if Black_no_line_counter[ord(char)-65] == TEST_NUM:
        new_image.save(path_dir + save_dir_name + "/train/" + char + "/" + file_name[:5] + "_result_" + naming + ".png")
    else:
        new_image.save(path_dir + save_dir_name + "/test/" + char + "/" + file_name[:5] + "_result_" + naming + ".png")
        Black_no_line_counter[ord(char) - 65] += 1


# 칼라 + 크기일정 + 라인유지
def character_separate_with_line(image, bbox, naming, char, save_dir_name):
    new_image = image.crop(bbox)
    new_pixel = new_image.load()
    bg_image = Image.new("RGB", (MAX_WIDTH, new_image.height), WHITE)
    for y in range(new_image.height):
        for x in range(new_image.width):
            if new_pixel[x, y] == CLEAR or new_pixel[x, y] == BLACK:
                new_pixel[x, y] = WHITE

    # bg_image 에 new_image 덮어씌우기
    bg_image.paste(new_image, (0, 0, new_image.width, new_image.height))
    new_image = bg_image

    if not os.access(path_dir + save_dir_name, os.F_OK):
        os.mkdir(path_dir + save_dir_name)
    if not os.access(path_dir + save_dir_name + "/train/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/train/")
    if not os.access(path_dir + save_dir_name + "/test/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/test/")
    if not os.access(path_dir + save_dir_name + "/train/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/train/" + char)
    if not os.access(path_dir + save_dir_name + "/test/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/test/" + char)
    if Color_with_line_counter[ord(char) - 65] == TEST_NUM:
        new_image.save(path_dir + save_dir_name + "/train/" + char + "/" + file_name[:5] + "_result_" + naming + ".png")
    else:
        new_image.save(path_dir + save_dir_name + "/test/" + char + "/" + file_name[:5] + "_result_" + naming + ".png")
        Color_with_line_counter[ord(char) - 65] += 1


# 칼라 + 크기일정 + 라인삭제
def character_separate_color_no_line(image, bbox, naming, char, save_dir_name):
    new_image = image.crop(bbox)
    new_pixel = new_image.load()
    bg_image = Image.new("RGB", (MAX_WIDTH, new_image.height), WHITE)
    new_color_dicts = {}
    this_image_color = ()
    for y in range(new_image.height):
        for x in range(new_image.width):
            if new_pixel[x, y] == CLEAR or new_pixel[x, y] == BLACK:
                new_pixel[x, y] = WHITE
            if new_pixel[x, y] != CLEAR and new_pixel[x, y] != BLACK and new_pixel[x, y] != WHITE:
                if new_pixel[x, y] not in new_color_dicts.keys():
                    new_color_dicts[new_pixel[x, y]] = 1
                else:
                    new_color_dicts[new_pixel[x, y]] += 1
    max_value = max(new_color_dicts.values())
    for color_dict in new_color_dicts:
        if new_color_dicts[color_dict] == max_value:
            this_image_color = color_dict
            break

    # 해당 색상은 그대로, 나머지는 흰색으로
    for y in range(new_image.height):
        for x in range(new_image.width):
            if new_pixel[x, y] != this_image_color:
                new_pixel[x, y] = WHITE

    # bg_image 에 new_image 덮어씌우기
    bg_image.paste(new_image, (0, 0, new_image.width, new_image.height))
    new_image = bg_image

    if not os.access(path_dir + save_dir_name, os.F_OK):
        os.mkdir(path_dir + save_dir_name)
    if not os.access(path_dir + save_dir_name + "/train/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/train/")
    if not os.access(path_dir + save_dir_name + "/test/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/test/")
    if not os.access(path_dir + save_dir_name + "/train/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/train/" + char)
    if not os.access(path_dir + save_dir_name + "/test/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
        os.mkdir(path_dir + save_dir_name + "/test/" + char)
    if Color_no_line_counter[ord(char) - 65] == TEST_NUM:
        new_image.save(path_dir + save_dir_name + "/train/" + char + "/" + file_name[:5] + "_result_" + naming + ".png")
    else:
        new_image.save(path_dir + save_dir_name + "/test/" + char + "/" + file_name[:5] + "_result_" + naming + ".png")
        Color_no_line_counter[ord(char) - 65] += 1


# ------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    path_dir = "./보안문자/"     # >> 이미지 파일들이 있는 디렉토리
    save_dir = ""               # >> 수정금지

    Color_with_line_counter = [0 for a in range(26)]
    Color_no_line_counter = [0 for a in range(26)]
    Black_no_line_counter = [0 for a in range(26)]

    file_list = os.listdir(path_dir)
    file_list.sort()
    for file_name in file_list:
        color_most_left_list = [999 for i in range(5)]
        color_most_right_list = [0 for i in range(5)]
        color_lists = []    # 해당 이미지의 5가지 문자 각각의 색 (R, G, B, A) 리스트

        if os.path.isdir(path_dir + file_name):  # 디렉토리일 경우 넘김
            continue
        im = Image.open(path_dir + file_name)

        line_im = Image.open(path_dir + file_name)
        px = im.load()

        blur_pixel_delete(im, px)
        im.save("./임시/" + file_name[:5] + ".png")
        blur_pixel_delete(line_im, px)
        special_height = line_delete(im, px)
        im.save("./임시/" + file_name[:5] + "noline.png")
        num = 0
        for num in range(5):
            character_separate_with_line(line_im, (color_most_left_list[num], 0, color_most_right_list[num], 45),
                                         str(num), file_name[num], "Color with_line")
            character_separate_color_no_line(im, (color_most_left_list[num], 0, color_most_right_list[num], 45),
                                             str(num), file_name[num], "Color no_line")
            character_separate(im, (color_most_left_list[num], 0, color_most_right_list[num], 45),
                               str(num), file_name[num], "Black no_line")
            num += 1
    print("""
    ----------------------------
    Done""")
