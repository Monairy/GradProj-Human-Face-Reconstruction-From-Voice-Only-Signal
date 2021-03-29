import os, sys, xlsxwriter, itertools 
d = []
a = []
j = []
su = []
so = []
h = []
b = []
u = []
t = []
p = []
r = []
leftImages = []

outWorkbook = xlsxwriter.Workbook('Output.xlsx')
outSheet = outWorkbook.add_worksheet()
# Exporting the path, boolean value, Detection confidence, and angles of each image, to be used for deletion
outSheet.write('A1','Path')
outSheet.write('B1','Bool')
outSheet.write('C1','Detection confidence')
outSheet.write('D1','Tilt')
outSheet.write('E1','Pan')
outSheet.write('F1','Roll')

fullPath = []

with open('Output.txt', 'r') as searchfile:
    for line in searchfile:
        if '../input/human-faces-dataset/' in line:
            fullPath.append(line[29:].strip())
        elif 'Detection confidence:' in line:
            d.append(float(line[21:].strip()))
        elif 'anger: ' in line:
            a.append(line[7:].strip())
        elif 'joy: ' in line:
            j.append(line[5:].strip())
        elif 'surprise: ' in line:
            su.append(line[9:].strip())
        elif 'sorrow: ' in line:
            so.append(line[8:].strip())
        elif 'headwear: ' in line:
            h.append(line[10:].strip())
        elif 'blurred: ' in line:
            b.append(line[9:].strip())
        elif 'under exposed: ' in line:
            u.append(line[15:].strip())
        elif 'tilt angle: ' in line:
            t.append(float(line[12:].strip()))
        elif 'pan angle: ' in line:
            p.append(float(line[11:].strip()))
        elif 'roll angle: ' in line:
            r.append(float(line[12:].strip()))
i = 0
for i in range(len(fullPath)):
    outSheet.write(i + 1, 0, fullPath[i])
    outSheet.write(i + 1, 2, d[i])
    outSheet.write(i + 1, 3, t[i])
    outSheet.write(i + 1, 4, p[i])
    outSheet.write(i + 1, 5, r[i])

for (d, a, j, su, so, h, b, u, t, p, r) in itertools.zip_longest(d, a, j, su, so, h, b, u, t, p, r):
    if d > 0.5 and a == 'VERY_UNLIKELY' and j == 'VERY_UNLIKELY' and su == 'VERY_UNLIKELY' and so == 'VERY_UNLIKELY' and h == 'VERY_UNLIKELY' and b == 'VERY_UNLIKELY' and u == 'VERY_UNLIKELY' and  t < 5 and t > -5 and p < 5 and p > -5 and r < 5 and r > -5:
        leftImages.append('1')
    else:
        leftImages.append('0')
j = 0
for j in range(len(fullPath)):
    outSheet.write(j + 1, 1, leftImages[j])
outWorkbook.close()