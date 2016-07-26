#!/usr/bin/python2.7
#！-*- coding: utf-8 -*-

# If true, runs rbt in debug mode and outputs its diff
DEBUG = True

POSTREVIEW_PATH = "/usr/local/bin"
REPOSITORY_URL = 'http://192.16.150.109/'
REPOSITORY = "truck"
BRANCH = "main branch"
USERNAME = 'xieqiang'
PASSWORD = 'root1234'
TARGET_GROUPS='reviewers'
TARGET_PEOPLE='xieqiang,caoyi' 


from Tkinter import *
import sys
import os
import subprocess
import re
from rbtools.clients.svn import SVNClient, SVNRepositoryInfo
from rbtools.api.client import RBClient

def execute(command, env=None,  split_lines=False, ignore_errors=False):
    """
    Utility function to execute a command and return the output.
    Derived from Review Board's rbt script.
    """
    if env:
        env.update(os.environ)
    else:
        env = os.environ

    if sys.platform.startswith('win'):
        p = subprocess.Popen(command,
                         stdin = subprocess.PIPE,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.STDOUT,
                         shell = False,
                         universal_newlines = True,
                         env = env)
    else:
         p = subprocess.Popen(command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=False,
                             close_fds=True,
                             universal_newlines= True,
                             env=env)
    if split_lines:
        data = p.stdout.readlines()
    else:
        data = p.stdout.read()

    rc = p.wait()
    if rc and not ignore_errors:
        sys.stderr.write('Failed to execute command: %s\n%s\n' % (command, data))
        sys.exit(1)

    return data

class Review(object):
    def __init__(self):
        top = Tk()
        top.geometry('680x520+100+100')
        top.title("review tool")

        self.svnRepositoryInfo = self.svnRepositoryInfo()

        label_svn_url = Label(top, text="SVN URL")
        entry_svn_url = Entry(top, width=60)
        entry_svn_url.insert(0, self.svnRepositoryInfo.path + self.svnRepositoryInfo.base_path)
        
        label_review_id = Label(top, text="review id")
        self.entry_review_id= Entry(top, width=60)
    
        label_review_people = Label(top, text="reviewer")
        self.entry_review_people = Entry(top, width=60)
        self.entry_review_people.insert(0, TARGET_PEOPLE)
     
        label_summary = Label(top, text="summary")
        self.entry_summary = Entry(top, width=60)
    
        label_desc = Label(top, text="description")
        self.txt_desc = Text(top, width=80,height=10)
        
        frame = Frame(top)
        label_modified = Label(top, text="modified files")
        scl_modfied = Scrollbar(frame, orient=VERTICAL)
        scl_modfied.pack(side=RIGHT, fill=Y)
        self.lst_modified = Listbox(frame, width=60, selectmode=MULTIPLE,yscrollcommand=scl_modfied.set)
        self.lst_modified.pack(side=LEFT,fill=Y)
        self.commit_files = self.parseDiff()
        self.commit_files += ['1','2','3','4','5','6','7','8','9']
        for i, v in enumerate(self.commit_files):
            self.lst_modified.insert(i,v)

        scl_modfied.config(command=self.lst_modified.yview)
            
        btn_submit = Button(top, text='submit', command=self.submit)
    
        label_svn_url.grid(row=0)
        entry_svn_url.grid(row=0, column=1)
        
        label_review_id.grid(row=1,column=0)
        self.entry_review_id.grid(row=1,column=1,sticky=W)
    
        label_review_people.grid(row=2,column=0)
        self.entry_review_people.grid(row=2,column=1,sticky=W)
    
        label_summary.grid(row=3,column=0)
        self.entry_summary.grid(row=3, column=1,sticky=W)
    
        label_desc.grid(row=4,column=0)
        self.txt_desc.grid(row=4,column=1)
        
        label_modified.grid(row = 5)
        frame.grid(row=5, column=1)

        btn_submit.grid(row=6, sticky=NSEW) 
        top.mainloop()
        
    def rbReposityInfo(self):
        client = RBClient('http://192.16.150.109',
            username='xieqiang', 
            password='root1234')
        root = client.get_root()
        return root.get_repositories()
    
    def postReview(self):
        debug = ''
        if DEBUG:
            debug='--debug'
        reviewboard_url='--server=' + REPOSITORY_URL
        repository= '--repository=' + REPOSITORY
        branch="--branch=" + BRANCH
        username= 'username=' + USERNAME
        password= 'password=' + PASSWORD
        target_groups='--target-groups=' + TARGET_GROUPS
        target_people= '--target-people=' + TARGET_PEOPLE
        #repository_url='--repository-url=http://192.16.150.215/slsvn/SLNew/'
        basedir='--basedir=/trunk/ShanLinCaiFu/App/IOS'
        diff_file="--diff-filename=diff.txt"
        publish=''
        reviewid=''
        rev = self.entry_review_id.get()
        if rev:
            reviewid='--review-request-id=' + rev
        
        include_files = []
        for i,v in enumerate(self.commit_files):
            if(self.lst_modified.selection_includes(i) == 1):
                #v = v[1 : len(v)]
                include_file="--include=" + v
                include_files+=[include_file]
            

        args = [debug, reviewid, reviewboard_url, repository,diff_file, branch, target_groups, target_people, publish] # + include_files
        # filter out any potentially blank args, which will confuse rbt
        args = [i for i in args if len(i) > 1]
        sum = self.entry_summary.get()
        if sum:
            summary = "--summary="+sum
            args += [summary];
        
        desc = self.txt_desc.get(1.0, "end-1c")
        if desc:
            description = '--description='+desc
            args += [description]
        
        
        # Run Review Board rbt script
        data = execute([os.path.join(POSTREVIEW_PATH, 'rbt'), 'post'] + args,
                   env = {'LANG': 'en_US.UTF-8'})

        if DEBUG:
            print data
    
    def parseDiff(self):
        #diff file
        debug = ''
        if DEBUG:
            debug='--debug'
        reviewboard_url='--server=' + REPOSITORY_URL
        repository= '--repository=' + REPOSITORY
        branch="--branch=" + BRANCH
        username= 'username=' + USERNAME
        password= 'password=' + PASSWORD
        target_groups='--target-groups=' + TARGET_GROUPS
        target_people= '--target-people=' + TARGET_PEOPLE
        repository_url='--repository-url=http://192.16.150.215/slsvn/SLNew/'
        args = [reviewboard_url, repository, repository_url]
        #self.diff_contents = execute([os.path.join(POSTREVIEW_PATH, 'rbt'), 'diff'] + args,
        #         env = {'LANG': 'zh_CN.UTF-8'})
        self.diff_contents = execute(['svn', 'diff'])
        s = re.findall(r'^Index: (.*)', self.diff_contents, re.M);
        try:
            fp = open('diff.txt', 'w+')
            fp.write(self.diff_contents)
        finally:
            if fp:
                fp.close()
        return s

    def svnRepositoryInfo(self):
        svn = SVNClient(options={"repository-url":"http://192.16.150.215/slsvn/SLNew/"})
        return svn.get_repository_info()
    
    def submit(self):
        self.postReview()
        #self.post_request()
        pass
    

def main():
    Review()
    

if __name__ == '__main__':
    main()