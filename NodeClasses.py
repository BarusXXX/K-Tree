from math import cos, sin, pi
import numpy

#==============================Common Methods==========================#

def MPbearing(x0, y0, Ang, Len):
    x = Len*sin(Ang) + x0
    y = Len*cos(Ang) + y0
    return(x,y)

def PopulateNode(x0, y0, n, scale):

    if n >= 1:
        for x in range(1, n):
            return MPbearing(x0, y0, x*pi/n, Mscale*scale)
            
    else:
        pass

def tuplemassadd(arr):
    sum_x = numpy.sum(arr[:, 0])
    sum_y = numpy.sum(arr[:, 1])
    return sum_x, sum_y

#==============================Data Prep============================#

class Folder:
    def __init__(self, AbsAddress, Branch, Level):
        self.AbsAddress = AbsAddress
        self.Branch = Branch
        self.Level = Level
        self.FolderSize = 0   #kbs
        self.Name = (AbsAddress.split("\\")[-1])
        self.FolderContents = 0 #folder number of  sub folders
      

class Files:
    def __init__(self, AbsAddress, Branch):
        self.AbsAddress = AbsAddress
        self.Branch = Branch
        self.FileSize = 0   #kbs
        self.FileExt = (AbsAddress.split(".")[-1])
        self.Name = (AbsAddress.split("\\")[-1])  #Check of \\ is the right symbol

#======================================Canvas============================================#

class Type:
    def __init__(self, TypeName, MaxLength, colour):  #Add Attraction Repultion option 1, -1
        self.TypeName = TypeName
        self.MaxLength = MaxLength
        self.defaultcolour = colour

class Connection:
    def __init__(self, TypeL, Parent, Child, CanvasX):
        self.CanvasX = CanvasX
        self.Type = TypeL
        self.Parent = Parent
        self.Child = Child
        self.Colour = TypeL.defaultcolour
        self.Disp = NodeConnector(CanvasX, None, None, self.Colour)

    def Delete(self):
        self.Disp.Delete()
        #self.CanvasX.delete(self.Disp.line)

    def Refresh(self, Parent, Child):

        self.Parent = Parent
        self.Child = Child

        if self.Parent != None:
            self.Disp.Delete()
            self.Disp = self.Disp.Refresh(Parent.loc, Child.loc)

        return self
      

class Node:   #Node is both drawn and the folder
    def __init__(self, x0, y0, Folder, CanvasX, type="Kn"):
        self.level = Folder.Level
        self.CanvasX = CanvasX
        self.type = type
        self.Folder = Folder
        if (self.Folder).Name != None:
            self.name = (self.Folder).Name
        else:
            self.name = "No Address!"

        self.Parent = None  #Singular however would be interesting to investigate more then one option


        if self.type == "Kn":
            self.x = x0
            self.y = y0
            self.disp = FolderNode(self.CanvasX, None, None, self.name, (5 - self.level) / 5, self.Folder.Branch)
           
        elif self.type == "K0":
            self.x = canvasx/2
            self.y = canvasy/2
            self.disp = MasterNode(self.CanvasX, self.x, self.y, self.name)

        self.FileInterface = FileInterface(self.CanvasX, (None, None), self.Folder.Branch)
        self.loc = (self.x, self.y)
        self.north = None   #parent branch
        self.clockwise = True
        self.closestnodes = None
        self.R_Vectors = None
        self.Resultant_Vector = None
        self.velocity = 0 #stationary
        self.Connection = None
        #self.Connections = None

        self.Connections_n = 0

        if self.Connection != None:
            self.Connections_n = len(self.Connections)


    def PopulateNode(self):
        if self.Connections_n >= 1:
            for x in range(1, self.Connections_n):
                return MPbearing(self.x, self.y, x * pi / (self.Connections_n), Mscale)
        else:
            print("No Nodes to Connect")
            pass

    def Delete(self):
        self.FileInterface.Delete()
        self.disp.Delete()
        self.Connection.Delete()

    def Refresh(self):
        self.disp = FolderNode(self.CanvasX, self.x, self.y, self.name, (5 - self.level) / 5, self.Folder.Branch)
        self.FileInterface = FileInterface(self.CanvasX, (self.x, self.y), self.Folder.Branch)
        return self

    def print(self):
        print(self.name, self)

class NodeCollection:
    def __init__(self, MasterDir, CanvasX):
        self.CanvasX = CanvasX
        self.MasterDir = MasterDir
        self.TreeStructure = []
        self.refreshtree()  #loaded from tree logic
        self.Border = [(0, 0), (canvasx, canvasy)]
        self.IterationCount = 1
        self.accelaration = 1 #default acceleration of system
        self.scale_mul = ((canvasx * canvasy * 9) / (1000 * Mscale))  # Review add x level scaling * (self.Node_n + 1)
        self.MasterPop()

        if self.Nodes == None:
            self.Node_n = 0
        else:
            self.Node_n = len(self.Nodes)

    def __iter__(self):
        return iter(self.Nodes)

    def GetRelationships(self):  #Attraction(not needed) #Repultion #Connectivity #Maxlengthperconnection
        NodesInSwarm = []
        NoC = self.Structure.children_n
        for Node in self.Nodes:
            NodesInSwarm.append((Node.x, Node.y))

        #Get angles to assign
        IntAngle = []
        for NumCon in NoC:
            IntAngle.append(365/(NumCon+1))  # +1 to get the parent connector every folder has only one parent

        R_Relation = []
        for Nodexy in NodesInSwarm:  # Option to get vectors based on initial values
            templist = NodesInSwarm
            templist.remove(Nodexy)
            R_VectorList = []
            for Node in templist:
                FullLengthVector = tuple(numpy.subtract(Node, Nodexy))
                Length = 0.5*((FullLengthVector[0])**2 + (FullLengthVector[1])**2)
                UnitsizedVector = numpy.divide(FullLengthVector, Length)
                R_VectorList.append(UnitsizedVector)
            R_Relation.append(R_VectorList)
        #check
        for x in R_Relation:
            print(x)

    #When to move and how to move said node
    def MoveNode(self):
        NodeVelocityVectors = []
        for Node in self.Nodes:
            NodeVelocityVectors.append(Node.Resultant_Vector)

        t=0
        while t < self.IterationCount:
            for Node in self.Nodes:
                self.CanvasX.move(Node.Resultant_Vector)
                #Node.velocity = Node.velocity + Node.accelaration*t  #Add acceleration deceleration over time
                if Node.nodeParent != None:
                    (Node.nodeParent).loc = tuple(numpy.add((Node.nodeParent).loc, tuple(numpy.multiply((Node.Resultant_Vector),(Node.nodeParent.Connection.Type.MaxLength)))))


    def MasterPop(self):
        Templist = []
        
        for folder in self.Structure.folders:
            pass
            #print("###################")
            #print(folder[0], folder[1])
            if self.Structure.folders.index(folder) == 0:
                Templist.append(Node(canvasx/2, canvasy/2, Folder(folder[0], folder[1], folder[2]), self.CanvasX, "K0"))
            else:
                Templist.append(Node(randint(0, canvasx), randint(0, canvasy), Folder(folder[0], folder[1], folder[2]), self.CanvasX)) #Add ID or ref

        self.Nodes = Templist   # Nodes based on Tree Structure

        MyType = Type("Test", 120, "red")  # Connection Type Move this

        NodeTn = 0

        #print("Node in collection:", len(self.Nodes), len(self.Structure.parentIndex))
        for parent in self.Structure.parentIndex:
            if parent == None:
                self.Nodes[NodeTn].Parent = None
                self.Nodes[NodeTn].level = self.Structure.level[NodeTn]
            else:
                self.Nodes[NodeTn].Parent = self.Nodes[parent] #this is a list needs to be recognised with
                self.Nodes[NodeTn].level = self.Structure.level[NodeTn]


            #print("Assigned parent %s to node %s" %(self.Structure.parentIndex[NodeTn], NodeTn), self.Nodes[NodeTn].name, self.Nodes[NodeTn].Folder.AbsAddress)
            NodeTn += 1
            #print("----------------")


        for NodeX in self.Nodes:  # Connectivity is initialised here
            NodeX.Connection = Connection(MyType, NodeX.Parent, NodeX, self.CanvasX)

    def Refresh(self):
        NodeContext = []  #List of lists of X,Ys changes with each iter
        NodeParent = [] # List of X,Y and max length tuple changes with each iter
        # if length is > max length create equal and opposite vector to the line
        NodeVelocityVectors = []
        proximity_array = []
        MoveVectors = []

        cnt2 = 0
        #Get graphical relation and create a resultant vector
        for Node in self.Nodes:
            if Node.Parent == None:
                NodeParent.append(None)
            else:
                templist = []
                proximity_temp = []
                for x in range(0, len(self.Nodes)):

                    if x == cnt2:
                        pass

                    elif self.Nodes[x]== None:
                        pass

                    else:
                        prox = tuple(numpy.subtract((self.Nodes[x].x, self.Nodes[x].y), (Node.x, Node.y)))
                        templist.append((self.Nodes[x].x, self.Nodes[x].y)) #Add to Node to move to all other
                        proximity_temp.append(((prox[0] ** 2 + prox[1] ** 2) ** 0.5, prox)) # len, coordinate change Multiplier smaller for closer proximity

                cnt2 += 1
                NodeContext.append(templist)
                proximity_array.append(proximity_temp)
                NodeParent.append((Node.Parent.x, Node.Parent.y, Node.Connection.Type.MaxLength))

        cnt3 = 0
        RectifyVector = []

        """
        for x in proximity_array:
            print("Entry")
            for y in x:
                print(y)
        """
        #print(proximity_array)
        #print(len(self.Nodes[1:]), len(NodeContext), len(proximity_array), len(NodeParent[1:]))
        dtop_array = []
        mult = []
        Num = len(self.Nodes[1:])
        levels = []
        for node in self.Nodes[1:]:
            levels.append(node.level)


        #print(self.Nodes[1:])
        for l, n, x, y, p in zip(levels, self.Nodes[1:], NodeContext, proximity_array, NodeParent[1:]):

            largest_dist = max(z[0] for z in y)
            Move = ([tuple(numpy.multiply((-1 + z[0] / (largest_dist)) / (((abs(l-levels[it])+1)/0.002)), z[1])) for z , it in zip(y, range(0, Num))])
            Movethis = tuplemassadd(numpy.asarray(list(list(z) for z in Move))) #Resultant repultion scaled Vector by proximity tuple per node
            Border_R = 2
            Damping = 0

            dtop =((p[0]-n.x)**2 + (p[1]-n.y)**2)**0.5  #distance to parent
            dtop_array.append(dtop)
            m=0.028 #0.1

            if dtop > p[2]:  # if distance grater then allowed apply shrinking vector
                RectifyVector.append(((p[0] - n.x)*m, (p[1] - n.y)*m))
                #RectifyVector.append(((p[0]-n.x)*((1+(dtop-p[2])/p[2])**2),(p[1]-n.y)*((1+(dtop-p[2])/p[2])**2)))  # Vector to cancel stretching but allow swaying

            elif dtop == p[2]: # if distance equal to allowed
                RectifyVector.append(((p[0]-n.x)*m, (p[1]-n.y)*m))
                mult.append(0)

            elif dtop < p[2]: #distance to parent is larger then alowed
                RectifyVector.append((0,0))



            #print(list(list(z) for z in Move))
            #print(numpy.random.randint(0, 10, size=(10, 2)))
            #print(RectifyVector, cnt3)
            Minusthis = tuple(numpy.add(Movethis, RectifyVector[cnt3]))
            MoveVectors.append(list(Minusthis))
            cnt3 += 1

        #Refresh animation
        cnt = 0
        for Node in self.Nodes:

            #print(Node.Resultant_Vector)
            NodeVelocityVectors.append(Node.Resultant_Vector)

            if Node.type == "Kn":
                #print(cnt, MoveVectors[cnt-1])
                Node.x += MoveVectors[cnt-1][0] #numpy.multiply(-((max(proximity_array) - proximity_array[cnt])/(max(proximity_array)*iterations)), NodeContext[2])
                Node.y += MoveVectors[cnt-1][1]
                Node.loc = (Node.x, Node.y)
                Node.Delete()
                self.Nodes[cnt] = Node.Refresh()
                #self.printstat()
                self.Nodes[cnt].Parent = self.Nodes[self.Structure.parentIndex[cnt]]
                cnt += 1
                Node.Connection = Node.Connection.Refresh(Node.Parent, Node)

            elif Node.type == "K0":  #Don't Move, Do not Update
                cnt += 1
                pass

    ##
    def assignFolderstoNodes(self):   #InNodeSystemContainer. Must also figure placement of the nodes
        for x in self.Structure.folders:
            self.Node_n = self.Node_n =+ 1
            addstr = (x.split(":")[1]), (x.split(":")[2])
            self.NodeSystem.append(Node(0, 0, Folder(":".join(addstr), (((((x.split(":")[0]).split("{")[1])).split("}")[0]).split(";"))), Files(":".join(addstr), (((((x.split(":")[0]).split("{")[1])).split("}")[0]).split(";")))))

    ##
    def assignFilestoNodes(self):
        return self.Structure.files
    ##
    def refreshtree(self):
        self.Structure = RecursiveTree(self.MasterDir)

    def printstat(self):
        for Node in self.Nodes:
            print(Node.Parent, Node.name, Node.loc)
