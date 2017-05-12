import os
from copy import deepcopy

class RecursiveTree:
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.files = []
        self.folders = [] #Tuple Absolute address, branch, level
        self.branches = []
        self.children_n = []
        self.currentlevel = 0
        self.level=[] #len(self.branches)
        self.level.append(0)

        self.folder_n = len(self.folders)
        self.parentIndex = []
        self.parentbranch = []
        self.iterator = 0
        self.reversead = 0

        self.parentIndex.append(None)
        self.branches.append([0])
        self.folders.append((dir_name, "{0}", 0))

        RecursiveTree.get_immediate_subdirectories(self, self.dir_name, 0)
        self.level_max = max(self.level)



    def Branch(self):
        pass

    def PrintTree(self):
        print("#Folders#")
        for x in self.folders:
            print(x)
        print("#Branches#")
        for x in self.branches:
            print(x)
        print("#Parent Branches#")
        for x in self.parentbranch:
            print(x)
        print("#Files#")
        for x in self.files:
            print(x)

    def subdir(self):
        return self.folders

    def filedir(self):
        return self.files

    def sortedbranches(self):
        STree = []
        CountX = 0
        for x in self.branches:
            STree.append([])
            for y in x:
                STree[CountX].append(int(y))
            CountX += 1

        SSum = []
        CountX = 0
        TTree = deepcopy(STree)

        for x in TTree:
            CountY = 0
            for y in x:
                TTree[CountX][CountY] = y + 1
                CountY += 1
            CountX += 1
            SSum.append(sum(x))

        SortedTree = [x for y, x in sorted(list(zip(SSum, STree)))]

    def get_immediate_subdirectories(self, a_dir, curadd):
        nextadd = 0
        relocator = 0
        cancleNo = self.reversead

        for name in os.listdir(a_dir):

            if os.path.isdir(os.path.join(a_dir, name)):
                curaddstr = str(curadd) + ";" + str(nextadd)
                relocator += 1
                self.iterator += 1
                self.currentlevel += 1

                ContainsSub = False
                ContainsNo = 0

                for x in os.listdir(a_dir + "/" + name):
                    if os.path.isdir(a_dir + "/" + name + "/" + x):
                        ContainsSub = True
                        ContainsNo += 1
                self.children_n.append(ContainsNo)

                PathConstructor = "{" + str(curadd) + ";" + str(nextadd) + "}" + ":" + os.path.join(a_dir, name)
                AbsAddressConstructor = (PathConstructor.split(":")[1]), (PathConstructor.split(":")[2])

                self.folders.append((":".join(AbsAddressConstructor), PathConstructor.split(":")[0], self.currentlevel))
                self.branches.append((((((PathConstructor.split(":")[0]).split("{")[1])).split("}")[0]).split(";")))
                self.parentbranch.append(str(curadd).split(";"))
                self.level.append(self.currentlevel)

                self.parentIndex.append(self.iterator - relocator - self.reversead + cancleNo)  #Cannot negate 1

                RecursiveTree.get_immediate_subdirectories(self, (a_dir + "/" + name), curaddstr)

                self.currentlevel -= 1

                if ContainsSub == True:
                    self.reversead += ContainsNo
                nextadd += 1

            else:
                self.files.append((self.iterator - relocator - self.reversead + cancleNo, os.path.join(a_dir, name))) #index of parent, direct links to file
                #print("file found:", self.iterator - relocator - self.reversead + cancleNo, name)
                #print("{"+str(curadd) + ";" + str(nextadd) + "}" + ":" + os.path.join(a_dir, name))








