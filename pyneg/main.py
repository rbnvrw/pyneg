import click
import numpy as np
from imageio import imread
import matplotlib.pyplot as plt
from PIL import Image

try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

@click.command()
@click.argument('inputfile', required=False, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True))
def main(inputfile):
    print('Processing file "%s"' % inputfile)

    image = imread(inputfile)

    edge_color = np.mean(np.percentile(image, 99.5, axis=0), axis=0)

    # divide entire image by edge color
    image = np.divide(image, edge_color)

    min_px = np.percentile(image, 0.7)
    image = image - min_px
    image[image<0] = 0
    max_px = np.percentile(image, 99.7)
    image /= max_px
    image[image>1] = 1
    image = 1 - image

    # image corrections
    image[:, :, 0] /= 0.6
    image[:, :, 1] /= 0.8
    image[:, :, 2] /= 0.9

    # auto gamma correction
    x = np.mean(image)
    gamma = np.log(1/2)/np.log(x)
    image = image**gamma

    min_px = np.percentile(image, 0.7)
    image = image - min_px
    image[image<0] = 0
    max_px = np.percentile(image, 99.7)
    image /= max_px
    image[image>1] = 1

    plt.imshow(image)
    plt.show(block=True)

if __name__ == '__main__':
    main()
