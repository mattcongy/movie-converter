class MovieFile(object):
    moviesCount = 0

    def __init__(self,name,path,md5):
        super(MovieFile,self).__init__()
        self.name = name
        self.path = path
        self.md5  = md5
        MovieFile.moviesCount += 1
