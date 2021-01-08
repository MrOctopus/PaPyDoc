def sanitize_line(line):
    start_index = 0

    while True:
        index = line.find(';', start_index) 

        if index == -1:
            break

        if line[index - 1] != '\\':
            line = line[:index].strip()
            break

        start_index = index + 1

    return line

def read_until(file, is_true):
    prev_line = ""

    while True:
        line = file.readline()

        if not line:
            raise EOFError()

        line = line.strip()

        if not line:
            continue

        if not is_true(line):
            prev_line = line
        else:
            return prev_line, line