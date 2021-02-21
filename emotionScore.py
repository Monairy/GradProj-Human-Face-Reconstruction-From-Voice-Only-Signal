# pylint: disable=no-member
def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io, os

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/ahmad/Downloads/GraduationProject/API/Key.json"

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    #print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
        print('headwear: {}'.format(likelihood_name[face.headwear_likelihood]))
        print('blurred: {}'.format(likelihood_name[face.blurred_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

import sys, glob
images = glob.glob('/home/ahmad/Downloads/GraduationProject/API/Images/*.jpg')
sys.stdout = open('Output.txt', 'w')
for image in images:
    print(image[51])
    detect_faces(image)
    print('\n')
