#!/usr/bin/env python

import os, sys
import ConfigParser

class FileParser:
    '''
    return dict (or list if it default)
    '''
    def __init__(self,inifile, section):
        self.inifile = inifile
        self.section = section
    def parseFile(self,default = False):
        parser = ConfigParser.ConfigParser()
        parser.read(self.inifile)
        if default:
            result =  parser.items(self.section)
        else:
            result = dict(parser.items(self.section))
        return result

class FileParserToList(FileParser):
    def parseFile(self, default=True):
        res=[]
        parser = ConfigParser.ConfigParser()
        parser.read(self.inifile)
        defaultres =  parser.items(self.section)
        for item in defaultres:
            res.append(item[1])
        return res