import csv


def load_data(hitmap, filename):
    f = open(filename, 'rb')
    raw_data = list(csv.reader(f))
    for row in range(0, len(hitmap)):
        for col in range(0, len(hitmap[row])):
            for deg in range(0, len(hitmap[row][col])):
                x = row*len(hitmap[row][col])*len(hitmap) + col*len(hitmap[row][col]) + deg
                hitmap[row][col][deg] = set(map(int,raw_data[x]))
    edgel_count = map(float, raw_data[-1])
    return edgel_count


def save_data(hitmap, edgel_count, filename):
    f = open(filename, 'wb')
    writer = csv.writer(f)
    for row in hitmap:
        for col in row:
            for deg in col:
                writer.writerow(list(deg))
    writer.writerow(edgel_count)
    f.close()

