from cv2 import cv2
from rubik_solver import utils

def get_single_layer_codes(img):
    white, red, orange, blue, green, yellow, x, y = (0,)*8

    prev_y = y
    width_of_single_box = int(len(img[0])/3)
    height_of_single_box = int(len(img)/3)
    x_endpoint = width_of_single_box
    y_endpoint = height_of_single_box
    blockNo = 0
    block_color_str = ''
    while blockNo < 9:
        while x < x_endpoint:
            y = prev_y
            while y < y_endpoint:
                # white red orange blue green yellow
                rgb = img[y, x]
                if rgb[0] > 141 and rgb[0] < 256 and rgb[1] > 141 and rgb[1] < 256 and rgb[2] > 141 and rgb[2] < 256 :
                    white += 1
                elif rgb[0] > 0 and rgb[0] < 30 and rgb[1] > 0 and rgb[1] < 30 and rgb[2] > 100 and rgb[2] < 220 :
                    red += 1
                elif rgb[0] > 20 and rgb[0] < 110 and rgb[1] > 22 and rgb[1] < 150 and rgb[2] > 160 and rgb[2] < 256 :
                    orange += 1
                elif rgb[0] > 130 and rgb[0] < 250 and rgb[1] > 85 and rgb[1] < 180 and rgb[2] > 0 and rgb[2] < 30 :
                    blue += 1
                elif rgb[0] > 0 and rgb[0] < 65 and rgb[1] > 115 and rgb[1] < 200 and rgb[2] > 0 and rgb[2] < 12 :
                    green += 1
                y += 10
            x += 10
        blockNo += 1
        maxx = max([white, red, orange, blue, green, yellow])
        threshold = 100
        # print(white, red, orange, blue, green, yellow)
        if(white == maxx and white > threshold):
            block_color_str += 'W '
        elif red == maxx and red > threshold:
            block_color_str += "R "
        elif orange == maxx and orange > threshold:
            block_color_str += "O "
        elif blue == maxx and blue > threshold:
            block_color_str += "B "
        elif green == maxx and green > threshold:
            block_color_str += "G "
        else:
            block_color_str += "Y "
        
        # print(white, red, orange, blue, green, yellow)
        white, red, orange, blue, green, yellow = (0,)*6
        if x >= (width_of_single_box*3)-3:
            block_color_str += '\n'
            x = 0
            prev_y = y
            y_endpoint += height_of_single_box
            x_endpoint = width_of_single_box
        else:
            x_endpoint += width_of_single_box
    # print(block_color_str)
    return block_color_str


if __name__ == "__main__":
    # cube = 'oyyoyygyybbyrbbybbrbbrrrrrrrggggggggoowooyooowwwwwwbww'
    # print(utils.solve(cube, 'Kociemba'))
    cube = ''
    for i in range(6):
        img = cv2.imread(f'Photos/{i+1}-min.jpg')
        single_layer = get_single_layer_codes(img)
        print(single_layer)
        # single_layer = single_layer.replace(' ', '')
        # single_layer = single_layer.replace('\n', '')
        # layer rearrangement should be done.
        # cube += single_layer
        img = None
    # print(utils.solve(cube, 'Kociemba'))