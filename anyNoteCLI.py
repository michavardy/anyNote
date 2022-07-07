from pathlib import Path
import os
#import argparse
import time
from dataclasses import dataclass
import re

@dataclass
class Node:
    hiarchy:int
    key:str
    #text:str=None
    slice:tuple=None
class MarkdownParser:
    def __init__(self,text):
        self.text = text
        self.keyword_text = ''
        self.nodes_list =[]
        self.preProcess()
        self.parse_keywords()
        self.parse_text()
    def preProcess(self):
        # remove text blocks
        blocks = list(re.finditer("```",self.text))
        self.slices = [(blocks[i].start(),blocks[i+1].end()) for i in range(0,len(blocks),2)]
        cur = 0
        for slice in self.slices:
            self.keyword_text = self.keyword_text + self.text[cur:slice[0] - 1]
            cur = slice[1]+1
    def parse_keywords(self):
        self.index_list = list(re.finditer('#+',self.keyword_text))
        for i in range(len(self.index_list)-1):
            node = Node(
                hiarchy = len(self.index_list[i].group()),
                key = self.keyword_text[self.index_list[i].end():self.index_list[i+1].start()]
            )
            self.nodes_list.append(node)
        self.nodes_list.append(Node(
            hiarchy=len(self.index_list[-1].group()),
            key = self.keyword_text[self.index_list[-1].end():]))
    def parse_text(self):
        new_list = []
        for index,node in enumerate(self.nodes_list):
            slice = self.slices[index]
            node.slice = slice
            node.text = self.text[slice[0]:slice[1]]
            new_list.append(node)
        self.nodes_list = new_list
    def add(self,node):
        self.nodes_list.append(node)
class CLI:
    def __init__(self, com_list,options_dict=None):
        self.commands = com_list
        self.cwd = self.commands[0]
        self.options = options_dict
        self.command_case_match()
        self.options_case_match()
        self.environ_lookup()
    def environ_lookup(self):
        if 'ANY_NOTES_DIRECTORY' in os.environ:
            self.any_notes_directory = Path(os.environ['ANY_NOTES_DIRECTORY'])
        else:
            self.search()
            os.environ['ANY_NOTES_DIRECTORY'] = str(self.any_notes_directory)
        self.notes_text_file = self.any_notes_directory/'notes.md'
    def command_case_match(self):
        match self.commands:
            case [first]:
                pass
            case [first,"init"]:
                self.init_repo()
            case [first,'remote']:
                print('remote')
            case _:
                pass
    def options_case_match(self):
        if self.options['read']:
            self.read()
        if self.options['write']:
            print('write')
        if self.options['replace']:
            print('replace')
        if self.options['edit_vim']:
            print('edit_vim')
        if self.options['edit_nano']:
            print('edit_nano')
        if all([not self.options[key] for key in self.options.keys()]):
            pass
    def strip_keyword(self,keyword):
        keyword = re.sub("\"","",keyword)
        keyword = re.sub("\'","",keyword)
        return(keyword)
    def min_node_hiarchy(self,value_list):
        min_node = value_list[0]
        for node in value_list:
            if node.hiarchy < min_node.hiarchy:
                min_node = node
        return(min_node)
    def read(self):
        self.search()
        self.text = self.notes_text_file.read_text()
        parse = MarkdownParser(self.text)
        keyword = self.strip_keyword(self.options['read'])
        value_list = [node for node in parse.nodes_list if re.search(keyword,node.key,re.I)]
        if value_list:
            node = self.min_node_hiarchy(value_list)
            print(node.text)
        else:
            print('no index found')
    def init_repo(self):
        # write new .anyNotes dir, write new notes.md
        self.any_note_directory = Path(str(Path(self.cwd)/'.anyNote'))
        self.notes_text_file = self.any_notes_directory/'notes.md'
        self.any_note_directory.mkdir(parents=True,exist_ok=True)
        os.environ['ANY_NOTES_DIRECTORY'] = str(self.any_notes_directory)
        self.notes_text_file.write_text('')
    def search(self):
        self.generations = len(Path(self.cwd).parts)
        curr = self.cwd
        for gen in range(self.generations,1,-1):
            curr = Path(os.path.split(curr)[0])
            self.any_notes_dir = list(Path.rglob(curr,'.anyNote'))
            if self.any_notes_dir:
                self.any_notes_directory = self.any_notes_dir[0]
                self.notes_text_file = self.any_notes_directory/'notes.md'
                break

if __name__ == "__main__":
    commands = ['C:/Users/micha/projects/cobyServer']
    arg_dict = {'read': "'dockers_contain'", 'write': False, 'replace': False, 'edit_vim': False, 'edit_nano': False}
    a = time.time()
    cli = CLI(commands,arg_dict)
    parse = MarkdownParser(cli.text)

