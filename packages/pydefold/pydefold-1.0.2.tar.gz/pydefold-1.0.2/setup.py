from setuptools import setup, find_packages
import os , requests 
import subprocess

import os , glob , shutil

def step0() : 
    import os , glob , shutil

    print(os.path.dirname(__file__))
    os.system("""
    rm -r build.cache || true > /dev/null
    mkdir build.cache
    """)
    os.chdir("build.cache")
    os.system("""
    wget https://github.com/defold/defold/releases/download/1.9.0/defoldsdk.zip
    unzip defoldsdk.zip
    cp -r ./defoldsdk/ext/include/google ./defoldsdk/share/proto/ 
    mkdir ./PyDefold
    """)
    print(os.getcwd())
    protoc = "./defoldsdk/ext/bin/x86_64-linux/protoc"
    @lambda _:_()
    def proto_files() : 
        current_path = os.getcwd()
        path = "./defoldsdk/share/proto/"
        depths = ['/'.join(i*'*')+ ".proto" for i in range(1,20)]
        result = set()
        paths =  [result.update(glob.glob(os.path.join(path,i))) for i in depths]                     
        return result
    for i in proto_files:
        cmd = f"{protoc} --python_out=./PyDefold --proto_path=./defoldsdk/share/proto {i}"
        os.system(cmd)

    os.chdir(os.path.dirname(__file__))
    os.system("""
    rm -r PyDefold || true > /dev/null
    mkdir PyDefold
    """)

    os.system("""
    pwd
    rm -r build.cache/PyDefold/google
    cp -r build.cache/PyDefold/ .
    cp -r build.cache/defoldsdk/share/proto PyDefold/
    rm -r build.cache

    """)
    #    touch PyDefold/__init__.py 
    import os , glob , sys 

    directories = [d for d in glob.glob(os.path.join("PyDefold", '*')) if os.path.isdir(d)]
    directories = [folder for folder in directories if not os.path.basename(folder) in ["proto"]]
    print(directories)

step0()
######################################
from google.protobuf import descriptor_pool, descriptor
import os , importlib , inspect 

def ParseModule(root , path) : 
    import sys , os , json 
    sys.path.append(root)
    module_path = os.path.join(root,os.path.basename(path))
    sys.path.append(module_path)
    # print("+++++" , module_path)
    # print(path)
    map_exp = {
        "module_path" : module_path , 
        "files" : dict()
    }
    for file in glob.glob(os.path.join(module_path,"*.py")) : 
        # print()
        # print("----" , file)
        module = importlib.import_module(os.path.splitext(os.path.basename(file))[0])
        members = inspect.getmembers(module)

        # Print the members and their types
        messages_types = set() 
        for name, member in members:
            # Filter out private and special names
            if not name.startswith('__'):
                #print(f"Name: {name}, Type: {type(member).__name__}")
                if type(member).__name__ == "MessageMeta"  : 
                    
                    messages_types.add(name)
        if len(messages_types) > 0 : 
            map_exp['files'][os.path.splitext(os.path.basename(file))[0]] = sorted(messages_types) 
    #print(json.dumps(map_exp , indent=4))
    return map_exp


def ParseFiles(root , file ) : 
    import sys , os , json 
    sys.path.append(root)
    module_name = os.path.splitext(os.path.basename(file))[0] + "_pb2"
    map_exp = {
        module_name : list() , 
    }
    module = importlib.import_module(os.path.splitext(os.path.basename(file))[0] + "_pb2")
    members = inspect.getmembers(module)
    messages_types = set() 
    for name, member in members:
        # Filter out private and special names
        if not name.startswith('__'):
            if type(member).__name__ == "MessageMeta"  :   
                messages_types.add(name)
    map_exp = {module_name.split(".proto")[0]  : sorted(messages_types)}
    return map_exp


protofolder = "PyDefold/proto"
for f in glob.glob(os.path.join(protofolder, '*')) : 
    if os.path.isdir(f) : 
        if os.path.basename(f) != "google" : 
            print(f)
            result = ParseModule(os.path.join(protofolder,"..") , f)
            for imfile , messagetypes in result['files'].items() : 
                with open(os.path.join(result.get('module_path') , "__init__.py"),"a") as buff: 
                    buff.write(f"from .{imfile} import {','.join(messagetypes)} \n")
    else : 
        if os.path.basename(f) != "__init__.py" :
            for k , v in ParseFiles(os.path.join(protofolder,"..") , f ).items() : 
                with open("PyDefold/init.py","a") as buff  : 
                    buff.write(f"from .{k} import {','.join(v)} \n")




        






os.system("mv PyDefold/init.py PyDefold/__init__.py")








class PypiPublisher : 
    def __init__(self, start_version = "1.0.0") : 
        self.start_version = start_version
        self.name = subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True).stdout.strip().split("/")[-1].replace(".git", "")
        print(f"Project name : {self.name}")
        self.version , self.new_version = self.get_versions()
        print(f"Project version : {self.version} -> {self.new_version }")
        #######
        author= subprocess.check_output(['git', 'config', 'user.name']).decode().strip()  if not os.environ.get("GITLAB_USER_NAME",None ) else os.environ.get("GITLAB_USER_NAME",None )  
        #######
        author_email= subprocess.check_output(['git', 'config', 'user.email']).decode().strip() if not  os.environ.get("GITLAB_USER_EMAIL", None ) else os.environ.get("GITLAB_USER_EMAIL", None ) 
        ######
        url  = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip() if not os.environ.get("CI_PROJECT_URL",None ) else os.environ.get("CI_PROJECT_URL",None )
        ######
        description  = 'Python Package made by Mhadhbi Issam . ' if not os.environ.get("CI_PROJECT_DESCRIPTION",None ) else os.environ.get("CI_PROJECT_DESCRIPTION",None )
        setup(
            name= os.path.basename(os.getcwd()),
            version=self.new_version,
            packages=find_packages(),
            author= author  ,
            author_email=author_email   ,
            description= description,
            long_description=open("README.md").read(),
            long_description_content_type="text/markdown",
            url= url    ,
            install_requires=['protobuf']  ,
            classifiers=[
                'Programming Language :: Python :: 3',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
            ],
            exclude_package_data={
                '': [".vscode" , "Test" , ".gitignore" , ".gitlab-ci.yml" ,".gitpod.yml", "Dockerfile" , "Makefile","requirements.txt" , ".gitpod.yml"],  # Exclude .pyc files and 'docs' directory
            }
        )
    def get_versions(self) : 
        response = requests.get(f"https://pypi.org/pypi/{self.name}/json")
        version = self.start_version
        if response.status_code == 200 : 
            version  = response.json()["info"]["version"]

        new_version = self.upgrade_version(version)
        return version , new_version

    def upgrade_version(self,version) : 
        major , minor , patch = map(int, version.split('.'))
        newversion = str(patch + 10 * minor + 100 * major + 1)
        a , b , c =  newversion[:-2]  , newversion[-2] , newversion[-1]
        newer_version = ".".join([str(i) for i in [newversion[:-2]  , newversion[-2] , newversion[-1]]])
        if newer_version.strip().startswith(".") : 
            newer_version = "0" + newer_version.strip()
        return newer_version


if __name__ == '__main__':
    PypiPublisher()