import os
import tkinter


matrix_labels = [None, 'up', 'down', 'left', 'right']


def set_matrix_labels(labels):
    global matrix_labels
    matrix_labels = labels


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
    fp.write(width.to_bytes(2, 'big', signed=False))
    last_element_count = 0
    for (ix, item) in enumerate(squashed):
        if ix == 0 or item == last_item:
            last_element_count += 1
        else:
            fp.write(last_element_count.to_bytes(3, 'little', signed=False))
            fp.write(matrix_labels.index(last_item).to_bytes(1, 'little', signed=False))
            last_element_count = 1
        last_item = item
    fp.write(last_element_count.to_bytes(3, 'little', signed=False))
    fp.write(matrix_labels.index(last_item).to_bytes(1, 'little', signed=False))


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


def embed(widget:tkinter.Widget, default_size=None, allow_new=True, allow_save=True, allow_load=True):
    from tkinter import Label, Toplevel, Frame, IntVar, Spinbox, Button
    from tkinter.messagebox import showerror
    from PIL.ImageTk import PhotoImage

    matrix = []
    buttons = []

    if default_size is None:
        instructions = """n: New Map
s: Save Map
o/l: Open Map"""
    else:
        instructions = ''
    instructions = Label(widget, text=instructions)
    instructions.pack()

    def create_new_map(width, height):
        matrix[:] = create_matrix(width, height)
        instructions.destroy()
        for old_button in buttons:
            old_button.destroy()
        buttons[:] = []
        for x in range(width):
            for y in range(height):
                # new_button = Button(widget, photoimage=)
                buttons.append()

    if allow_new:
        def new_map(event):
            dialog = Toplevel(widget)
            form = Frame(dialog)
            Label(form, text='Width:').grid(row=0, column=0)
            Label(form, text='Height:').grid(row=1, column=0)
            size = [1, 1]
            comm = (lambda ix: (lambda event=None: size.__setitem__(ix, wb.get() + (event.char if event else ''))))
            wv = IntVar(value=10)
            wb = Spinbox(form, from_=1, to=65535, command=comm(0), textvariable=wv)
            wb.bind('<Key>', comm(0))
            wb.grid(row=0, column=1)
            hv = IntVar(value=10)
            hb = Spinbox(form, from_=1, to=65535, command=comm(1), textvariable=hv)
            hb.bind('<Key>', comm(1))
            hb.grid(row=1, column=1)
            form.pack()
            dialog.transient(widget)
            dialog.grab_set()
            wb.focus_set()
            widget.wait_window(dialog)
            create_new_map(wv.get(), hv.get())
        widget.bind('n', new_map)
        widget.bind('N', new_map)

    if allow_save:
        def save_map(event):
            ...
        widget.bind('s', save_map)
        widget.bind('S', save_map)

    if allow_load:
        def load_map(event):
            ...
        widget.bind('o', load_map)
        widget.bind('l', load_map)
        widget.bind('O', load_map)
        widget.bind('L', load_map)

    import glob
    images = {x: PhotoImage(file=next(glob.iglob(os.path.join('img', str(x) + '*')))) for x in matrix_labels}
    buttons = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right', '<space>': None}


def main():
    root = tkinter.Tk()
    root.title('Map Grid')
    embed(root)
    root.mainloop()


if __name__ == '__main__': main()
    