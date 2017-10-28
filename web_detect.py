import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
import exifread
from datetime import datetime

def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    # if annotations.pages_with_matching_images:
    #     print('\n{} Pages with matching images retrieved'.format(
    #         len(annotations.pages_with_matching_images)))
    #
    #     for page in annotations.pages_with_matching_images:
    #         print('Url   : {}'.format(page.url))
    #
    # if annotations.full_matching_images:
    #     print ('\n{} Full Matches found: '.format(
    #            len(annotations.full_matching_images)))
    #
    #     for image in annotations.full_matching_images:
    #         print('Url  : {}'.format(image.url))
    # #
    # if annotations.partial_matching_images:
    #     print ('\n{} Partial Matches found: '.format(
    #            len(annotations.partial_matching_images)))
    #
    #     for image in annotations.partial_matching_images:
    #         print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        # print ('\n{} Web entities found: '.format(
        #     len(annotations.web_entities)))

        for entity in annotations.web_entities[:1]:
            f = open(args.image_url,'rb')
            tags = exifread.process_file(f, strict=True)
            try:
                tlat = tags['GPS GPSLatitude'].values
                tlon = tags['GPS GPSLongitude'].values
                lon = tlon[0].num/tlon[0].den + tlon[1].num/tlon[1].den/60.0 + tlon[2].num/tlon[2].den/3600.0
                lat = tlat[0].num/tlat[0].den + tlat[1].num/tlat[1].den/60.0 + tlat[2].num/tlat[2].den/3600.0
                h, m, s =  tags["GPS GPSTimeStamp"].values
                datum = "{} {}:{}:{}".format(tags["GPS GPSDate"],str(h), str(m),str(s))
            # timestamp = datetime.strptime(datum[:-4], '%Y:%m:%d %I:%M:%S')
            except:
                lon = 'nan'
                lat = 'nan'
                datum='nan____'

            f.close()
            with open('annotations.csv','a') as my_file:
                my_file.write(','.join([datum[:-4], args.image_url.split('/')[-1], str(lat), str(lon),(entity.description),str(entity.score)[:4]+'\n']))
            my_file.close()
            print(','.join([datum[:-4], args.image_url.split('/')[-1], str(lat), str(lon), (entity.description),str(entity.score)[:4]]))
            # print('Score      : {}'.format(entity.score))
            # print('Description: {}'.format(entity.description))
    print('')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('image_url', help=path_help)
    args = parser.parse_args()

    report(annotate(args.image_url))
