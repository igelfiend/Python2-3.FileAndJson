from sys import stdin
from os.path import normcase, join, isfile
from os import listdir
from sys import version_info
import codecs
import json

class Worker:
    _prevPath = ""
    _path = ""
    _files = []
    _fError = False
    _pyVersion = version_info[ 0 ]

    def prevPath(self):
        return self._prevPath
    def path(self):
        return self._path
    def isError(self):
        return self._fError
    def __init__(self):
        if self._pyVersion == 2:
            codecs.getreader( "utf-8" )( stdin )

        self.loadPreviousPath()

    def loadPreviousPath(self):
        try:
            with open( "config.ini", "r" ) as file:
                self._prevPath = json.load( file )
        except:
            self._prevPath = ""

    def readNewPath(self):
        # read path
        print( "Please enter the track foulder path:" )
        self._path = stdin.readline()[:-1]

        if self._pyVersion == 2:
            self._path = self._path.decode(stdin.encoding )
        self._path = normcase( self._path )

        # save path
        with open( "config.ini", "w" ) as file:
            json.dump( self._path, file )

        try:
            self._files = [ f for f in listdir( self._path ) if isfile(join( self._path, f) ) ]
        except:
           self._fError = True
           self._files = []

    def showDifference(self):
        if (self._path != self._prevPath):
            return

        with codecs.open( "files.data", "r", encoding='utf-8' ) as listFile:
            prevFiles = json.load( listFile )

        deletedFiles   = []
        recreatedFiles = []

        for el in prevFiles:
            if el not in self._files:
                deletedFiles.append( el )
            else:
                recreatedFiles.append( el )

        print( "deleted elements: " )
        print( u'%s' % ", ".join( deletedFiles ) )

        print( "recreated elements: " )
        print( u'%s' % ", ".join( recreatedFiles ) )

    def saveData(self):
        with codecs.open( "files.data", "w", encoding="utf-8" ) as listFile:
            json.dump( self._files, listFile, ensure_ascii=False )


def main():
    worker = Worker()
    worker.readNewPath()
    if worker.isError():
        print( "Path is uncorrect!" )
        return

    worker.showDifference()
    worker.saveData()

if __name__ == "__main__":
    main()
