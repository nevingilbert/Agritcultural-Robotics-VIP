from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
import random

def plotPoints(paths: list, title, sizes=None):
    ax = plt.axes(projection="3d")
    for path in paths:
        r, g, b = random.randint(0, 99) / 100.0, random.randint(0, 99) / 100, random.randint(0,99) / 100.0
        color = (r, g, b)
        path_x = [p.x for p in path]
        path_y = [p.y for p in path]
        path_z = [p.z for p in path]
        # if sizes is None:
        ax.scatter3D(path_x, path_y, path_z)
        # else:
        #     ax.scatter3D(path_x, path_y, color=color, s=sizes[paths.index(path)])
        plt.title(title)

    plt.show()

def plotPointsLine(paths: list, title, sizes=None):
    ax = plt.axes(projection="3d")
    for path in paths:
        r, g, b = random.randint(0, 99) / 100.0, random.randint(0, 99) / 100, random.randint(0,99) / 100.0
        color = (r, g, b)
        path_x = [p.x for p in path]
        path_y = [p.y for p in path]
        path_z = [p.z for p in path]
        # if sizes is None:
        ax.plot3D(path_x, path_y, path_z)
        # else:
        #     ax.scatter3D(path_x, path_y, color=color, s=sizes[paths.index(path)])
        plt.title(title)

    plt.show()