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
    text:str=None
class MarkdownParser:
    def __init__(self,text):
        self.text = text
        self.find_headers()
        self.parse_headers()
    def find_headers(self):
        # code block slices
        self.blocks = list(re.finditer("```",self.text))
        self.slices =  [(self.blocks[i].start(),self.blocks[i+1].end()) for i in range(0,len(self.blocks),2)]
        # headers
        self.headers = list(re.finditer("#+.*\n",self.text))
        self.headers = [head for head in self.headers  \
            if not any([(head.start() > slc[0] and head.end() < slc[1]) for slc in self.slices])]
    def parse_headers(self):
        self.nodes_list = []
        for header_index in range(len(self.headers)):
            # remove \n from header
            raw_text = self.headers[header_index].group()
            raw_text = re.sub('\n','',raw_text)
            # count hash tags for hiarchy
            hiarchy = raw_text.count('#')
            # sub and strip # to get key
            key = re.sub('#+','',raw_text)
            key = key.strip()
            if header_index < len(self.headers)-1:
                node = Node(
                    hiarchy=hiarchy,
                    key=key,
                    text=self.text[self.headers[header_index].end():self.headers[header_index+1].start()]
                )
            else:
                node = Node(
                    hiarchy=hiarchy,
                    key=key,
                    text=self.text[self.headers[header_index].end():]
                )
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
    arg_dict = {"read":"'Dockers'", "traverse":False}
    #a = time.time()
    cli = CLI(commands,arg_dict)
    parse = MarkdownParser(cli.text)
   

