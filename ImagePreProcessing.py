from PIL import Image
import os


CLEAR = (0, 0, 0, 0)            # 투명
WHITE = (255, 255, 255, 255)    # 흰색
BLACK = (0, 0, 0, 255)          # 검정

MAX_WIDTH = 60
TEST_NUM = 2   # 주의 : 5개밖에 없는 문자있음. Train 도 고려해야함.


class CaptchaImage:
    each_images = [None for i in range(5)]
    result_text = ""
    color_most_left_list = [999 for ii in range(5)]
    color_most_right_list = [0 for iii in range(5)]

    def __init__(self, name):
        self.origin_name = name
        self.origin_image = Image.open(self.origin_name)
        self.origin_pixel = self.origin_image.load()
        self.height = self.origin_image.height
        self.width = self.origin_image.width

    # 블러 픽셀 제거 (alpha 값이 255가 아니면 삭제)
    def blur_pixel_delete(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.origin_pixel[x, y][3] != 255:
                    self.origin_pixel[x, y] = CLEAR

    # 라인 삭제하기 (blur_pixel_delete 미리 해야함)
    def line_delete(self):
        spe_h = 0

        # 다섯가지 색상만이 존재하는 special_height 구하기
        for y in range(5, self.height):
            global color_lists
            color_lists = []
            for x in range(self.width):
                if self.origin_pixel[x, y] not in color_lists:
                    if self.origin_pixel[x, y] != CLEAR and \
                            (self.origin_pixel[x, y] == self.origin_pixel[x + 2, y]
                             or self.origin_pixel[x, y] == self.origin_pixel[x - 2, y]):
                        color_lists.append(self.origin_pixel[x, y])
            if len(color_lists) == 5:
                spe_h = y
                break

        # color_lists 에 없는 색상 삭제, 있는 색상은 각 색상 별 최소 x 위치
        for y in range(self.height):
            for x in range(self.width):
                if self.origin_pixel[x, y] not in color_lists:  # 색상 리스트에 없으면 해당 색상은 삭제
                    self.origin_pixel[x, y] = CLEAR
                else:  # 색상 리스트에 있으면 해당 위치와 각 색깔 별 최소, 최대 x위치 판별
                    for i in range(len(color_lists)):
                        if self.origin_pixel[x, y] == color_lists[i]:
                            self.color_most_left_list[i] = min(self.color_most_left_list[i], x)
                            self.color_most_right_list[i] = max(self.color_most_right_list[i], x)
        return spe_h

    def character_separate(self):
        for i in range(5):
            bbox = (self.color_most_left_list[i], 0, self.color_most_right_list[i], 45)
            new_image = self.origin_image.crop(bbox)
            new_pixel = new_image.load()
            bg_image = Image.new("RGB", (MAX_WIDTH, new_image.height), WHITE)

            # 자른 이미지 글자의 주 색상 찾기
            this_image_color = ()
            new_color_dicts = {}
            for y in range(new_image.height):
                for x in range(new_image.width - 1, 0, -1):
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
            # bg_image 에 new_image 덮어씌우기
            bg_image.paste(new_image, (0, 0, new_image.width, new_image.height))
            new_image = bg_image
            self.each_images[i] = new_image

    # 칼라 + 크기일정 + 라인유지
    def character_separate_with_line(self):
        for i in range(5):
            bbox = (self.color_most_left_list[i], 0, self.color_most_right_list[i], 45)
            new_image = self.origin_image.crop(bbox)
            new_pixel = new_image.load()
            bg_image = Image.new("RGB", (MAX_WIDTH, new_image.height), WHITE)
            for y in range(new_image.height):
                for x in range(new_image.width):
                    if new_pixel[x, y] == CLEAR or new_pixel[x, y] == BLACK:
                        new_pixel[x, y] = WHITE
            # bg_image 에 new_image 덮어씌우기
            bg_image.paste(new_image, (0, 0, new_image.width, new_image.height))
            new_image = bg_image
            self.each_images[i] = new_image

    # 칼라 + 크기일정 + 라인삭제
    def character_separate_color_no_line(self):
        for i in range(5):
            bbox = (self.color_most_left_list[i], 0, self.color_most_right_list[i], 45)
            new_image = self.origin_image.crop(bbox)
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
            self.each_images[i] = new_image

    def ImageSave(self, save_dir_name, counter):
        if not os.access(save_dir_name, os.F_OK):
            os.mkdir(save_dir_name)
        if not os.access(save_dir_name + "/train/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
            os.mkdir(save_dir_name + "/train/")
        if not os.access(save_dir_name + "/test/", os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
            os.mkdir(save_dir_name + "/test/")
        for i, char in enumerate(self.origin_name[7:12]):
            if not os.access(save_dir_name + "/train/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
                os.mkdir(save_dir_name + "/train/" + char)
            if not os.access(save_dir_name + "/test/" + char, os.F_OK):  # 해당 디렉토리가 이미 존재하는지 확인
                os.mkdir(save_dir_name + "/test/" + char)
            if counter[ord(char) - 65] == TEST_NUM:
                self.each_images[i].save(
                    save_dir_name + "/train/" + char + "/" + file_name[:5] + "_result_" + str(i) + ".png")
            else:
                self.each_images[i].save(
                    save_dir_name + "/test/" + char + "/" + file_name[:5] + "_result_" + str(i) + ".png")
                counter[ord(char) - 65] += 1


# ------------------------------------------------------------------------------------------------------------------- #
def OneImageProcessing():
    one_target_image = CaptchaImage("./testd.png")
    one_target_image.blur_pixel_delete()
    one_target_image.line_delete()
    one_target_image.character_separate()
    for i, each_image in enumerate(one_target_image.each_images):
        each_image.save("./temp/" + str(i) + ".png")


if __name__ == '__main__':
    OneImageProcessing()
    # exit()

    path_dir = "./보안문자/"     # >> 이미지 파일들이 있는 디렉토리

    Color_with_line_counter = [0 for a in range(26)]
    Color_no_line_counter = [0 for a in range(26)]
    Black_no_line_counter = [0 for a in range(26)]

    file_list = os.listdir(path_dir)
    file_list.sort()
    for file_name in file_list:
        if os.path.isdir(path_dir + file_name):  # 디렉토리일 경우 넘김
            continue
        target_image = CaptchaImage(path_dir + file_name)
        target_line_image = CaptchaImage(path_dir + file_name)

        target_image.blur_pixel_delete()
        target_line_image.blur_pixel_delete()

        target_image.line_delete()

        target_image.character_separate()
        target_image.ImageSave(path_dir + "Black no_line", Black_no_line_counter)

        target_image.character_separate_color_no_line()
        target_image.ImageSave(path_dir + "Color no_line", Color_no_line_counter)

        target_line_image.character_separate_with_line()
        target_line_image.ImageSave(path_dir + "Color with_line", Color_with_line_counter)
    print("----------------------------\nDone")
