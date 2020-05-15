import tkinter


matrix_labels = [None, 'up', 'down', 'left', 'right']


def create_matrix(width, height, default_value=matrix_labels[0]):
    matrix = []
    for y in range(height):
        matrix.append([])
        for x in range(width):
            matrix[y].append(default_value)
    return matrix


def squash_matrix(matrix):
    result = []
    for row in matrix:
        for item in row:
            result.append(item)
    return result


def unsquash_matrix(squashed, width, do_fillin=False, fillin_value=matrix_labels[0]):
    squashed_length = len(squashed)
    extra_elements = squashed_length % width
    if extra_elements:
        if do_fillin:
            squashed = squashed[:]
            squashed.extend([fillin_value] * (width - extra_elements))
        else:
            raise ValueError("%i elements left over after unsquash" % extra_elements)

    result = []
    for (ix, item) in enumerate(squashed):
        if not ix % width:
            result.append([])
        result[-1].append(item)
    return result


def save_matrix(matrix, fp):
    width = len(matrix[0])
    squashed = squash_matrix(matrix)
    fp.write(width.to_bytes(2, 'big'))
    last_element_count = 0
    for (ix, item) in enumerate(squashed):
        if ix == 0 or item == last_item:
            last_element_count += 1
        else:
            fp.write(last_element_count.to_bytes(3, 'little'))
            fp.write(matrix_labels.index(last_item).to_bytes(1, 'little'))
            last_element_count = 1
        last_item = item
    fp.write(last_element_count.to_bytes(3, 'little'))
    fp.write(matrix_labels.index(last_item).to_bytes(1, 'little'))


def load_matrix(fp, do_fillin=False, fillin_value=matrix_labels[0]):
    width = int.from_bytes(fp.read(2), 'big')
    squashed = []
    while True:
        value = fp.read(4)
        if not value: break
        element_count = int.from_bytes(value[:3], 'little')
        element = matrix_labels[value[3]]
        squashed.extend([element] * element_count)
    return unsquash_matrix(squashed, width, do_fillin, fillin_value)



if __name__ == '__main__':
    from pprint import pp

    matrix = create_matrix(5, 5)
    matrix[1][2] = 'up'
    matrix[3][2] = 'down'
    matrix[2][1] = 'left'
    matrix[2][3] = 'right'
    print('matrix:')
    pp(matrix)
    print()

    save_matrix(matrix, open('matrix.dat', 'wb'))
    loaded = load_matrix(open('matrix.dat', 'rb'))
    print('loaded:')
    pp(loaded)
    print()

    print('result:', loaded == matrix)
    