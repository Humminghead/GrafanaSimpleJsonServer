import os


class BaseFileReader():
    def readFile(self, path):
        content = str

        if path != "":
            with open(path, 'r') as file:
                try:
                    content = file.read()
                except UnicodeDecodeError as e:
                    print(e.reason)
            file.close()

        return content

    def listDirectory(self, path):
        try:
            return os.listdir(path)
        except FileNotFoundError as e:
            print(e)

    def deleteFile(self, path):
        os.remove(path)
