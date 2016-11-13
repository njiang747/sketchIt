import csv


def load_data(hitmap, filename):
    f = open(filename, 'rb')
    raw_data = list(csv.reader(f))
    for row in range(0, len(hitmap)):
        for col in range(0, len(hitmap[row])):
            for deg in range(0, len(hitmap[row][col])):
                hitmap[row][col][deg] = set(raw_data[row * len(hitmap) + col * len(hitmap[row]) + deg])
    edgel_count = raw_data[-1]
    return hitmap, edgel_count


def save_data(hitmap,edgel_count, filename):
    f = open(filename, 'wb')
    writer = csv.writer(f)
    for row in hitmap:
        for col in row:
            for deg in col:
                writer.writerow(list(deg))
    writer.writerow(edgel_count)
    f.close()

