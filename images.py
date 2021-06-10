from PIL import Image

def binarize_color(image : Image, r, g, b, threshold=30):
    width, height = image.size
    img_matrix = [[True for x in range(height)] for y in range(width)]
    obstacles = []
    for x in range(width):
        for y in range(height):
            rim,gim,bim = image.getpixel((x,y))
            isObstacle = abs(rim - r) < threshold and abs(gim - g) < threshold and abs(bim - b) < threshold
            if isObstacle:
                img_matrix[x][y] = False
                obstacles.append(Point(x, y))

    return img_matrix, obstacles

def binarize_depth(image, depth):
    pass