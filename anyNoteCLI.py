from cgitb import text
from pathlib import Path
import os
import argparse
import time
from dataclasses import dataclass
import re
from autoComplete import auto_complete

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
    def __init__(self, commands,options=None):
        self.commands = commands
        self.cwd = self.commands[0]
        self.options = options
        self.command_case_match()
        self.environ_lookup()
        self.parse_notes()
        self.options_case_match()
    def __repr__(self):
        return(f"commands={self.commands}, options={self.options}")
    def environ_lookup(self):
        if 'ANY_NOTES_DIRECTORY' in os.environ:
            self.any_notes_directory = Path(os.environ['ANY_NOTES_DIRECTORY'])
        else:
            self.search()
            os.environ['ANY_NOTES_DIRECTORY'] = str(self.any_notes_directory)
        self.notes_text_file = self.any_notes_directory/'notes.md'
    def parse_notes(self):
        #self.search()
        self.text = self.notes_text_file.read_text()
        self.parse = MarkdownParser(self.text)
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
        if self.options['traverse']:
            self.traverse()
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
        self.keyword = self.strip_keyword(self.options['read'])
        self.value_list = [node for node in self.parse.nodes_list if re.search(self.keyword,node.key,re.I)]
        if self.value_list:
            node = self.min_node_hiarchy(self.value_list)
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
    def traverse(self):
        self.traverse_selected = ''
        self.root_nodes = [node for node in self.parse.nodes_list]
        self.root_nodes_keys = [node.key.strip() for node in self.root_nodes]
        print([node.key.strip() for node in self.root_nodes if node.hiarchy==1])
        print('please select note index, press esc to exit')
        self.traverse_selected = auto_complete(self.root_nodes_keys)
        self.options['read']=self.traverse_selected
        self.read()
        
if __name__ == "__main__":
    commands = ['C:/Users/micha/projects/cobyServer']
    arg_dict = {"read":None, "traverse":True}
    a = time.time()
    cli = CLI(commands,arg_dict)
    parse = MarkdownParser(cli.text)

