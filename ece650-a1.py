from math import sqrt
import re
import sys
import itertools
from math import hypot

class Point(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Vertex(object):
	def __init__(self, point1, label,flag,Intflag):
		self.point1 = point1
		self.label = label
		self.flag=flag
		self.Intflag=Intflag
	def strCoor(self):
		s= "%s: (%.2f,%.2f)" % (self.label,self.point1.x,self.point1.y)
		return str(s)
	def __str__(self):
		s = "{}:({},{}){},{}".format(self.label, str(self.point1.x), str(self.point1.y), format(self.flag),format(self.Intflag))
		print s

class Street(object):
	# pointList is of type point and is a list with tuple as points
	def __init__(self, streetName, pointList):
		self.streetName = streetName
		self.pointList = pointList

def main():
	StreetList=[]
	user_input= ''
	VertexList=[]
	EdgeList={}
	Edge=[]

	def distancehypot(p1,p2):
		 return hypot(p2.x - p1.x, p2.y - p1.y)

	def addCasePoint(sname, p):
			flag = False
			for i in VertexList:
				if (i.point1.x == p.x) and (i.point1.y == p.y):
					flag = True

			if (not flag):
				v = Vertex(p, len(VertexList) + 1, True, False)
				VertexPointSet(sname, v)
				VertexList.append(v)


	def addCaseInt(sname, p):
			Intv = Vertex(p, len(VertexList) + 1, True, True)
			flag2 = False
			for j in VertexList:
				if (p.x == j.point1.x and p.y == j.point1.y):
					flag2 = True
					j.flag=True
					j.Intflag=True
					Intv = j
			if (not flag2):
				VertexList.append(Intv)
			flag5 = False
			for i in EdgeList[sname]:
				if ((i.point1.x == Intv.point1.x) and (i.point1.y == Intv.point1.y)):
					flag5 = True
			if (not flag5):
				intersectionPointSetandArrange(sname, Intv)

	def addSamePoint(sname, p):
			Intv = Vertex(p, len(VertexList) + 1, True, True)
			flag2 = False
			for j in VertexList:
				if (p.x == j.point1.x and p.y == j.point1.y):
					flag2 = True
					j.Intflag=True
					j.flag=True
					Intv = j
			if (not flag2):
				VertexList.append(Intv)
			for i in EdgeList[sname]:
				if ((i.point1.x == Intv.point1.x) and (i.point1.y == Intv.point1.y)):
					i.label = Intv.label
					i.Intflag = Intv.Intflag
					i.flag = Intv.flag

	def case0(s1name,s2name,l1,l2):

		if (l1[0].x == l2[0].x and l1[0].y == l2[0].y):
			if(distancehypot(l1[0],l1[1])>distancehypot(l2[0],l2[1])):
				addCasePoint(s1name,l1[1])
				addSamePoint(s1name,l1[0])
				addSamePoint(s2name, l2[0])
				addSamePoint(s2name, l2[1])
				addCaseInt(s1name,l2[1])
			elif (distancehypot(l1[0],l1[1])<distancehypot(l2[0],l2[1])):
				addCasePoint(s2name, l2[1])
				addSamePoint(s2name, l2[0])
				addSamePoint(s1name, l1[0])
				addSamePoint(s1name, l1[1])
				addCaseInt(s2name, l1[1])

		elif l1[0].x == l2[1].x and l1[0].y == l2[1].y:
			if (distancehypot(l1[0], l1[1]) > distancehypot(l2[0], l2[1])):
				addCasePoint(s1name, l1[1])
				addSamePoint(s1name, l1[0])
				addCaseInt(s1name, l2[0])
				addSamePoint(s2name, l2[0])
				addSamePoint(s2name, l2[1])
			elif (distancehypot(l1[0], l1[1]) < distancehypot(l2[0], l2[1])):
				addCasePoint(s2name, l2[0])
				addSamePoint(s2name, l2[1])
				addCaseInt(s2name, l1[1])
				addSamePoint(s1name, l1[0])
				addSamePoint(s1name, l1[1])
		elif l1[1].x == l2[0].x and l1[1].y == l2[0].y:
			if (distancehypot(l1[0], l1[1]) > distancehypot(l2[0], l2[1])):
				addCasePoint(s1name, l1[0])
				addSamePoint(s1name, l1[1])
				addCaseInt(s1name, l2[1])
				addSamePoint(s2name, l2[0])
				addSamePoint(s2name, l2[1])
			elif (distancehypot(l1[0], l1[1]) < distancehypot(l2[0], l2[1])):
				addCasePoint(s2name, l2[1])
				addSamePoint(s2name, l2[0])
				addCaseInt(s2name, l1[0])
				addSamePoint(s1name, l1[0])
				addSamePoint(s1name, l1[1])
		elif l1[1].x == l2[1].x and l1[1].y == l2[1].y:
			if (distancehypot(l1[0], l1[1]) > distancehypot(l2[0], l2[1])):
				addCasePoint(s1name, l1[0])
				addSamePoint(s1name, l1[1])
				addCaseInt(s1name, l2[0])
				addSamePoint(s2name, l2[0])
				addSamePoint(s2name, l2[1])
			elif (distancehypot(l1[0], l1[1]) < distancehypot(l2[0], l2[1])):
				addCasePoint(s2name, l2[0])
				addSamePoint(s2name, l2[1])
				addCaseInt(s2name, l1[0])
				addSamePoint(s1name, l1[0])
				addSamePoint(s1name, l1[1])

	def case1(s1name,s2name,l1,l2):

		if (l1[0].x == l2[0].x and l1[0].y == l2[0].y):
			addCasePoint(s1name,l1[1])
			addCasePoint(s2name,l2[1])
			addSamePoint(s1name,l1[0])
			addSamePoint(s2name,l2[0])
		elif l1[0].x == l2[1].x and l1[0].y == l2[1].y:
			addCasePoint(s1name, l1[1])
			addCasePoint(s2name, l2[0])
			addSamePoint(s1name, l1[0])
			addSamePoint(s2name, l2[1])
		elif l1[1].x == l2[0].x and l1[1].y == l2[0].y:
			addCasePoint(s1name, l1[0])
			addCasePoint(s2name, l2[1])
			addSamePoint(s1name, l1[1])
			addSamePoint(s2name, l2[0])
		elif l1[1].x == l2[1].x and l1[1].y == l2[1].y:
			addCasePoint(s1name, l1[0])
			addCasePoint(s2name, l2[0])
			addSamePoint(s1name, l1[1])
			addSamePoint(s2name, l2[1])

	def case2(s1name,s2name,l1,l2):
		# l2 is between l1
		addCasePoint(s1name, l1[0])
		addCasePoint(s1name, l1[1])
		addCaseInt(s1name, l2[0])
		addCaseInt(s1name, l2[1])
		addSamePoint(s2name,l2[0])
		addSamePoint(s2name, l2[1])

	def case3(s1name, s2name, l1, l2):
		if is_between(l1, [l2[0].x, l2[0].y]):
			if is_between(l2, [l1[1].x, l1[1].y]):
				addCasePoint(s1name, l1[0])
				addSamePoint(s1name,l1[1])
				addCaseInt(s1name,l2[0])
				addCasePoint(s2name, l2[1])
				addSamePoint(s1name, l2[0])
				addCaseInt(s2name,l1[1])
			elif is_between(l2, [l1[0].x, l1[0].y]):
				addCasePoint(s1name, l1[1])
				addSamePoint(s1name, l1[0])
				addCaseInt(s1name, l2[0])
				addCasePoint(s2name, l2[1])
				addSamePoint(s1name, l2[0])
				addCaseInt(s2name, l1[0])
		elif is_between(l1, [l2[1].x, l2[1].y]):
			if is_between(l2, [l1[1].x, l1[1].y]):
				addCasePoint(s1name, l1[0])
				addSamePoint(s1name, l1[1])
				addCaseInt(s1name, l2[1])
				addCasePoint(s2name, l2[0])
				addSamePoint(s1name, l2[1])
				addCaseInt(s2name, l1[1])
			elif is_between(l2, [l1[0].x, l1[0].y]):
				addCasePoint(s1name, l1[1])
				addSamePoint(s1name, l1[0])
				addCaseInt(s1name, l2[1])
				addCasePoint(s2name, l2[0])
				addSamePoint(s1name, l2[1])
				addCaseInt(s2name, l1[0])

	def collinear4(x1, y1, x2, y2, x3, y3,x4,y4):
		f1=abs((y1 - y2) * (x1 - x3) - (y1 - y3) * (x1 - x2)) <= 1e-9
		f2=abs((y1 - y2) * (x1 - x4) - (y1 - y4) * (x1 - x2)) <= 1e-9
		return f1 and f2

	def collinear(x1, y1, x2, y2, x3, y3):
		return abs((y1 - y2) * (x1 - x3) - (y1 - y3) * (x1 - x2)) <= 1e-9


	# Check 2 points are on the line or not
	def is_between(line, inter):
		if(collinear(line[0].x,line[0].y,line[1].x,line[1].y,inter[0],inter[1])):
			if (min(line[0].x, line[1].x) <= inter[0] <= max(line[0].x, line[1].x)) and (
							min(line[0].y, line[1].y) <= inter[1] <= max(line[0].y, line[1].y)):
				return True
			else:
				return False
		else:
			return False


	def edgeFill():
		for i in StreetList:
			EdgeList[i.streetName]=[ Vertex(j," ",False,False) for j in i.pointList]

	def intersectionPointSetandArrange(StretName,intVertex):
		ctr=0
		for i in zip(EdgeList[StretName], EdgeList[StretName][1:]):
			if(is_between([i[0].point1,i[1].point1],[intVertex.point1.x,intVertex.point1.y])):
				break
			ctr=ctr+1
		temp=EdgeList[StretName][-1]
		ctr=ctr+1
		for i in xrange(len(EdgeList[StretName])-1,ctr,-1):
			EdgeList[StretName][i]=EdgeList[StretName][i-1]
		EdgeList[StretName][ctr]=intVertex
		EdgeList[StretName].append(temp)



	def VertexPointSet(StreetName,VertexPt):
		for i in EdgeList[StreetName]:
			if(i.point1.x==VertexPt.point1.x and i.point1.y==VertexPt.point1.y):
				i.label=VertexPt.label
				i.flag=True
				i.Intflag=VertexPt.Intflag
				return

	# Check if intersection is there on line
	def line_intersection(line1, line2,streetname):
		try: # Try includes the normal case f the insection without the cllinearity cases if its not a normal case then it throw exception 
			x = ((float(line1[0].x) * line1[1].y - float(line1[0].y) * line1[1].x) * (line2[0].x - line2[1].x) - (
			line1[0].x - line1[1].x) * (line2[0].x * line2[1].y - line2[0].y * line2[1].x)) / (
				(float(line1[0].x )- line1[1].x) * (line2[0].y - line2[1].y) - (line1[0].y - line1[1].y) * (
				line2[0].x - line2[1].x))
			y = ((float(line1[0].x) * line1[1].y - line1[0].y * line1[1].x) * (line2[0].y - line2[1].y) - (
			line1[0].y - line1[1].y) * (line2[0].x * line2[1].y - line2[0].y * line2[1].x)) / (
				(float(line1[0].x) - line1[1].x) * (line2[0].y - line2[1].y) - (line1[0].y - line1[1].y) * (
				line2[0].x - line2[1].x))
		except ZeroDivisionError:
			#print "except"
			if (collinear4(line1[0].x, line1[0].y, line1[1].x, line1[1].y, line2[0].x, line2[0].y, line2[1].x, line2[1].y)): # this if is checking whether the 2 lines that is points are collinear or parllel 
				# if collinear then if condition satifies and all the cases are checked otherwise nothing happens and 3 false are return
				if ((line1[0].x == line2[0].x and line1[0].y == line2[0].y and is_between(line1,[line2[1].x,line2[1].y]))or
					(line1[0].x == line2[1].x and line1[0].y == line2[1].y and is_between(line1,[line2[0].x,line2[0].y])) or
					(line1[1].x == line2[0].x and line1[1].y == line2[0].y  and is_between(line1,[line2[1].x,line2[1].y]))or
					(line1[1].x == line2[1].x and line1[1].y == line2[1].y and is_between(line1,[line2[0].x,line2[0].y])) or
					(line1[0].x == line2[0].x and line1[0].y == line2[0].y and is_between(line2, [line1[1].x,line1[1].y])) or
					(line1[0].x == line2[1].x and line1[0].y == line2[1].y and is_between(line2, [line1[1].x,line1[1].y])) or
					(line1[1].x == line2[0].x and line1[1].y == line2[0].y and is_between(line2, [line1[0].x,line1[0].y])) or
					(line1[1].x == line2[1].x and line1[1].y == line2[1].y and is_between(line2, [line1[0].x, line1[0].y]))):
					#print "case 0"
					case0(streetname[0],streetname[1],line1,line2)

				elif ((line1[0].x == line2[0].x and line1[0].y == line2[0].y) or (line1[0].x == line2[1].x and line1[0].y == line2[1].y) or (line1[1].x == line2[0].x and line1[1].y == line2[0].y) or (line1[1].x == line2[1].x and line1[1].y == line2[1].y)):
					#print "Case1"
					case1(streetname[0],streetname[1],line1,line2)
				elif (is_between(line1, [line2[0].x,line2[0].y]) and is_between(line1, [line2[1].x,line2[1].y])):
					#print "Case 2"
					case2(streetname[0],streetname[1],line1,line2)
				elif (is_between(line2, [line1[0].x,line1[0].y]) and is_between(line2, [line1[1].x,line1[1].y])):
					#print "Case 2"
					case2(streetname[1],streetname[0],line2,line1)
				elif (is_between(line1, [line2[0].x,line2[0].y]) and (not is_between(line1, [line2[1].x,line2[1].y])) or (not is_between(line1, [line2[0].x,line2[0].y])) and is_between(line1, [line2[1].x,line2[1].y])):
					#print "Case 3a"
					case3(streetname[0],streetname[1],line1,line2)
				elif (is_between(line2, [line1[0].x,line1[0].y]) and (not is_between(line2, [line1[1].x,line1[1].y])) or (not is_between(line2, [line1[0].x,line1[0].y])) and is_between(line2, [line1[1].x,line1[1].y])):
					#print "Case 3b"
					case3(streetname[1], streetname[0], line2, line1)
			return False, False, False

		if (is_between(line1, (x, y)) and is_between(line2, (x, y))):
			return x, y, True
		else:
			return False, False, False


	def OutVertex2Lines(S1, S2):
		s1Name=S1.streetName
		s2Name=S2.streetName
		StreetC1=S1.pointList
		StreetC2=S2.pointList
		for i in StreetList:
			EdgeList[i]=[]
		for f1, s1 in zip(StreetC1, StreetC1[1:]):
			for f2, s2 in zip(StreetC2, StreetC2[1:]):
				check = line_intersection([f1, s1], [f2, s2],[s1Name,s2Name])
				if (check[2]): # checking wheather there is an intersection by checking the check list at index 2 is true or false
					##########################
					ListToBeAddedS1=[f1,s1]  # these 2 oints to be added in the Street1 
					for i in ListToBeAddedS1:
						flag1=False
						for j in VertexList:
							if(i.x==j.point1.x and i.y==j.point1.y):
								flag1= True
						if(not flag1):
							v = Vertex(i, len(VertexList)+1,True,False)
							VertexPointSet(s1Name, v)  # this function is used to put the vertex in Edgelist
							VertexList.append(v)
					#########################
					ListToBeAddedS2 = [f2, s2]  # these 2 oints to be added in the Street2
					for i in ListToBeAddedS2:
						flag3 = False
						for j in VertexList:
							if (i.x == j.point1.x and i.y == j.point1.y):
								flag3 = True
						if (not flag3):
							v = Vertex(i, len(VertexList) + 1, True,False)
							VertexPointSet(s2Name, v)
							VertexList.append(v)
					#############################
					IntersectionPt = Point(check[0], check[1])   # Making intersection Point Object
					Intv = Vertex(IntersectionPt, len(VertexList) + 1, True, True) # making intersection as a vertex object
					flag2 = False
					for j in VertexList:  # checking whether its already present in vertex list or not 
						if (IntersectionPt.x == j.point1.x and IntersectionPt.y == j.point1.y):
							flag2 = True
							j.flag = True
							j.Intflag = True
							Intv=j

					if (not flag2):
						VertexList.append(Intv)

					flag4 = False  # this function is used to put the vertex in Edgelist of street 1
					for i in EdgeList[s1Name]:
						if ((i.point1.x == Intv.point1.x) and (i.point1.y == Intv.point1.y)):
							flag4 = True
							i.flag = True
							i.Intflag = True
					if (not flag4):
						intersectionPointSetandArrange(s1Name, Intv)

					flag5 = False
					for i in EdgeList[s2Name]:  # this function is used to put the vertex in Edgelist of street 2
						if (i.point1.x == Intv.point1.x) and (i.point1.y == Intv.point1.y):
							i.flag=True
							i.Intflag=True
							flag5 = True
							if(i.label==" "):
								i.label=Intv.label
					if (not flag5):
						intersectionPointSetandArrange(s2Name, Intv)



	#Add the street to StreetList
	def CommandA():
		sName = ParsedStreetName(user_input)  # get the streetName from input
		sCorrdinateList=ParsedCoordinateList(user_input) #Get the coordinate list of input
		for i in StreetList:
			if(i.streetName.lower()==sName.lower()):
				sys.stderr.write("Error: Street Already Exists\n")
				return
		NewStreet=Street(sName, sCorrdinateList) #If street name not exist then create New street object and append to street list
		StreetList.append(NewStreet)

	def CommandC():
		sName = ParsedStreetName(user_input)  # get the streetName from input
		sCorrdinateList = ParsedCoordinateList(user_input)  # Get the coordinate list of input
		for i in StreetList:
			if (i.streetName.lower() == sName.lower()):
				i.pointList=sCorrdinateList
				return
		sys.stderr.write("Error: Street Name Not Exists\n")


	def CommandR():
		sName = ParsedStreetName(user_input)  # get the streetName from input
		for i in StreetList:
			if (i.streetName.lower() == sName.lower()):
				StreetList.remove(i)
				return
		sys.stderr.write("Error: Street Name Not Exists\n")


	def CommandG(): # Perform Generate graph everytime g is clicked
		edgeFill()
		StreetPairList=list(itertools.combinations(StreetList,2))

		for i in StreetPairList:
			OutVertex2Lines(i[0],i[1])
		##sys.stdout.write("V = {\n")
		TotalVertexs=0
		for i in VertexList:
			TotalVertexs=TotalVertexs+1
			##sys.stdout.write(i.strCoor())
			##sys.stdout.write('\n')
		##sys.stdout.write('}\n')
		print('V '+str(TotalVertexs))

		# this is to delete some erorneous street object added in edge list
		listobedel=[]
		for k,v in EdgeList.iteritems():
			if(len(v)<=0):
				listobedel.append(k)
		for i in listobedel:
			del EdgeList[i]

		for k, v in EdgeList.iteritems():
			for j in zip(v, v[1:]):
				if (j[0].flag == True and j[1].flag == True) and (j[0].Intflag == True or j[1].Intflag == True):
					s = (j[0].label, j[1].label)
					f=False
					for u in Edge:
						if((u[0]==s[0]) and (u[1]==s[1])) or ((u[1]==s[0]) and (u[0]==s[1])):
							f=True
					if(not f):  # this is to ensre that same edge such as <1,2> and <1,2> or <2,1> is not added in Edge list
						Edge.append(s)
		fora3=[]
		for i in range(0,len(Edge)):
			if(Edge[i][0]==' ' or Edge[i][1]==' '):
				continue
			#sys.stdout.write(str(Edge[i][0])+" "+str(Edge[i][1])+" ")
			w1=int(Edge[i][0])
			w2=int(Edge[i][1])
			fora3.append([w1-1,w2-1])

		sys.stdout.write("E {")   # This is to print the edges in the format given in assignment with taking care of no comma in last edge
		for i in range(0,len(fora3)):
			#s="<%s,%s>" %(str(Edge[i][0]),str(Edge[i][1]))
			#w1=Edge[i][0]-1
			#w2=Edge[i][1]-1
			if i != len(fora3) - 1:
				 sys.stdout.write("<"+str(fora3[i][0])+","+str(fora3[i][1])+">,")
				 #sys.stdout.write(s)
				 #sys.stdout.write(',')
			else:
				sys.stdout.write("<"+str(fora3[i][0])+","+str(fora3[i][1])+">")
				#sys.stdout.write(s)
				#sys.stdout.write('\n')
		#sys.stdout.write("}\n")
		print("}")
		sys.stdout.flush()
		del VertexList[:]  # Clearing all 3 data structure to be used again next time when g command is pressed
		del Edge[:]
		del fora3[:]
		EdgeList.clear()

	while(True):
			user_input = sys.stdin.readline()
			if(user_input==''): # this condition s to exit when eof line is here that is when CTRL+D is pressed
				break
			if(validate(user_input)):
				user_input.strip()

				if (user_input[0] == 'a'):
					CommandA()

				if(user_input[0] == 'c'):
					CommandC()

				elif (user_input[0] == 'r'):
					CommandR()

				elif (user_input[0] == 'g'):
					CommandG()

			else:
				sys.stderr.write("Error: Wrong Input format\n")

#For Parsing and getting the Coordinate List
def ParsedCoordinateList(command):
	Clist = []
	data = command.split('"')
	coor = re.findall(r'(\s*\(\s*[-]?\d+\s*\,\s*[-]?\d+\s*\)\s*)', data[2])
	for i in coor:
		CordinateTuple = eval(i)
		p = Point(CordinateTuple[0], CordinateTuple[1])
		Clist.append(p)
	return Clist

#For Parsing and getting the Street Name
def ParsedStreetName(command):
	data = command.split('"')
	return data[1]


#Validating user function
def validate(command):
	command.strip()
	if(command[0]=='a' or command[0]=='c' ):
		obj = re.match(r'\s*[a|c]\s*["][\s*(A-z)+\s*]+["](\s*\(\s*[-]?\d+\s*\,\s*[-]?\d+\s*\)\s*){2,}', command)
	elif(command[0]=='r'):
		obj= re.match(r'\s*[r]\s*["][\s*(A-z)+\s*]+["]\s*',command)
	elif(command[0]=='g'):
		obj=re.match(r'\s*[g]\s*',command)
	else:
		return False
	if (obj):
		if(obj.end()== len(command)):
			return True
		else:
			return False
	else:
		return False

if __name__ == '__main__':
	main()