import os

class Utils:
    def __init__(self) -> None:
        pass

    def write_txt_file(self, path, document):
        file = open(path, 'w')
        for line in document:
            file.write(line + os.linesep)
        file.close()