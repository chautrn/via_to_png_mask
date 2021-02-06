import sys
import os
import json
from PIL import Image
from PIL import ImageDraw

def get_arg(name, index):
    try:
        if os.path.exists(sys.argv[index]):
            return sys.argv[index]
        else:
            raise FileNotFoundError
    except IndexError:
        sys.exit('Missing ' + name + ' path. Format is IMAGE_PATH ANNOTATION_PATH OUTPUT_PATH.')

def get_polygon(region):
    x_points = region['shape_attributes']['all_points_x']
    y_points = region['shape_attributes']['all_points_y']
    polygon = []

    for i in range(len(x_points)):
        polygon.append((x_points[i], y_points[i]))

    return polygon

def draw_mask(image_path, file_name, polygons, output_path):
    img = Image.open(os.path.join(image_path, file_name))
    mask = Image.new('L', img.size, color=0)
    draw = ImageDraw.Draw(mask)
    for polygon in polygons:
        draw.polygon(polygon, fill=255)
    mask.save(os.path.join(output_path, file_name[:-3] + 'png'))


def main():
    image_path = get_arg('image', 1)
    annotation_path = get_arg('annotation', 2)
    output_path = get_arg('output', 3)

    with open(annotation_path) as json_file:
        annotation_dict = json.load(json_file)

    for img_name in annotation_dict.keys():
        img = annotation_dict[img_name]
        polygons = []

        for region in img['regions']:
            polygons.append(get_polygon(region))

        draw_mask(image_path, img['filename'], polygons, output_path)


if __name__ == '__main__':
    main()

