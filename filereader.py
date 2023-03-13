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
        # print(path)
        return os.listdir(path)

    def deleteFile(self, path):
        os.remove(path)
