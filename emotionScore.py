# pylint: disable=no-member
import os
leftImages = []
det = []
tangle = []
pangle = []
rangle = []

def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/ahmad/Downloads/GraduationProject/API/Key.json"

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    flag = 0
    # Iterating over faces in image (should only be executed once as there should only be one face in each image)
    for face in faces:
        flag = 1
        d = face.detection_confidence
        a = likelihood_name[face.anger_likelihood]
        j = likelihood_name[face.joy_likelihood]
        su = likelihood_name[face.surprise_likelihood]
        so = likelihood_name[face.sorrow_likelihood]
        h = likelihood_name[face.headwear_likelihood]
        b = likelihood_name[face.blurred_likelihood]
        u = likelihood_name[face.under_exposed_likelihood]
        t = face.tilt_angle
        p = face.pan_angle
        r = face.roll_angle

        print('Detection confidence:{}'.format(d))
        print('anger: {}'.format(a))
        print('joy: {}'.format(j))
        print('surprise: {}'.format(su))
        print('sorrow: {}'.format(so))
        print('headwear: {}'.format(h))
        print('blurred: {}'.format(b))
        print('under exposed: {}'.format(u))
        print('tilt angle: {}'.format(t))
        print('pan angle: {}'.format(p))
        print('roll angle: {}'.format(r))

        # Appending values to lists
        det.append(d)
        tangle.append(t)
        pangle.append(p)
        rangle.append(r)

        # Checking if the image meets the critira
        if d > 0.5 and a == 'VERY_UNLIKELY' and j == 'VERY_UNLIKELY' and su == 'VERY_UNLIKELY' and so == 'VERY_UNLIKELY' and h == 'VERY_UNLIKELY' and b == 'VERY_UNLIKELY' and u == 'VERY_UNLIKELY' and  t < 5 and t > -5 and p < 5 and p > -5 and r < 5 and r > -5:
            leftImages.append('1')
        else:
            leftImages.append('0')

        # Face bounds are not needed, but just in case ¯\_(ツ)_/¯
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        print('face bounds: {}'.format(','.join(vertices)))

    # A flag to mark finding at least one face; because some images are so distorted that no face can be detected
    if flag == 0:
        # Appending zero for distorted image; in order not to mess the list ordering
        leftImages.append('0')
    
    # Error Handling
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

import sys
# Change to the path of the directory containing the images
path = '/home/ahmad/Downloads/GraduationProject/API/Images/'
images = os.listdir(path)
# Redirecting stdout to output to the text file
sys.stdout = open('Output.txt', 'w')
names = []
fullPath = []
# Converting Images names to integer to sort
for image in images:
    names.append(int(image.replace('.jpg','')))
# For some reason it has to be sorted
names.sort()
# For each image, calling the API and indexing each image with its number
for n in names:
    print(n)
    image = path + str(n) + '.jpg'
    fullPath.append(image)
    detect_faces(image)
    print('\n')
# Printing the boolean values as backup for excel
print(leftImages)
sys.stdout.close()

import xlsxwriter
outWorkbook = xlsxwriter.Workbook('Output.xlsx')
outSheet = outWorkbook.add_worksheet()

# Exporting the path, boolean value, Detection confidence, and angles of each image, to be used for deletion
outSheet.write('A1','Path')
outSheet.write('B1','Bool')
outSheet.write('C1','Detection confidence')
outSheet.write('D1','Tilt')
outSheet.write('E1','Pan')
outSheet.write('F1','Roll')

for item in range(len(fullPath)):
    outSheet.write(item + 1, 0, fullPath[item])
    outSheet.write(item + 1, 1, leftImages[item])
    outSheet.write(item + 1, 2, det[item])
    outSheet.write(item + 1, 3, tangle[item])
    outSheet.write(item + 1, 4, pangle[item])
    outSheet.write(item + 1, 5, rangle[item])

outWorkbook.close()
