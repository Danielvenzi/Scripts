import os
import sys

def DiskScan():

	#results = str(os.popen("fdisk -l | grep 'Disk /' | grep -Ev '/dev/mapper' | grep -Po '\K/dev/.+:'").read())
	DiskFile = open("disk.name","w")
	results = str(os.popen("fdisk -l | grep 'Disk /' | grep -Po '\K/dev/.+\D:'").read())
	DiskFile.write(results)
	#results = results.strip(':\n')
	DiskFile.close()

def DiskStrip():

	disks=[]
	DiskFile = open("disk.name","r")
	for disk in DiskFile:
		disk = disk.strip(':\n')
		disks.append(disk)
	DiskFile.close()
	#os.system("rm -f disk.name")
	
	return disks

def DiskWrite(DiskArray):
	
	os.system("rm -f disk.name")
	DiskFile = open("disk.name","w")	
	for disk in DiskArray:
		DiskFile.write(disk+"\n")
	DiskFile.close()
		

def PrintArray(ArrayName):
	
	DiskString=""
	i=0
	while i <= len(ArrayName)-1:
		#print(ArrayName[i]) 
		
		if i == len(ArrayName)-1:
			DiskString = DiskString+ArrayName[i]
		else:
			DiskString = DiskString+ArrayName[i]+"\n"
		i += 1
	
	print(DiskString)

def DiskAnalysis(DiskArray):

	for disk in DiskArray:
		DiskLine = str(os.popen("df -h | grep {0}".format(disk)).read())
		DiskLine = DiskLine.strip("\n")
		DiskLine = DiskLine.strip("\n")
		#print(DiskLine)

		DiskName = disk
		DiskSize = str(os.popen("df -h | grep '{0} ' | cut -c25-29".format(disk)).read())
		DiskUsage = str(os.popen("df -h | grep '{0} ' | cut -c32-35".format(disk)).read())
		DiskAvai = str(os.popen("df -h | grep '{0} ' | cut -c38-41".format(disk)).read())
		DiskPercent = str(os.popen("df -h | grep '{0} ' | cut -c43-46".format(disk)).read())
		DiskMount = str(os.popen("df -h | grep '{0} ' | cut -c48-60".format(disk)).read())
		
		DiskName = DiskName.strip("\n")
		DiskSize = DiskSize.strip("\n")
		DiskUsage = DiskUsage.strip("\n")
		DiskAvai = DiskAvai.strip("\n")
		DiskPercent = DiskPercent.strip("\n")
		DiskMount = DiskMount.strip("\n")		
		
		if DiskSize == "":
                         
                                continue

		elif DiskSize != "":

			#print(DiskName)	
			#print(DiskSize)
			#print(DiskUsage)
			#print(DiskAvai)
			#print(DiskPercent)
			#print(DiskMount)
			
			Result="""
		DISK Query Results:

		Disk Name: """+DiskName+"""
		Disk Size: """+DiskSize+"""
		Disk Usage: """+DiskUsage+"""
		Available: """+DiskAvai+"""
		Used Percentual: """+DiskPercent+"""
		Mountpoint: """+DiskMount+"""
		
"""
			print(Result)


def DiskAnalysisPart(DiskArray):
	
	i=0
	while i <= len(DiskArray)-1: 
		
		disk = DiskArray[i]
		DiskAnalysisPart2(disk)
		#print(disk)
		i += 1
		

def DiskAnalysisPart2(disk):

		i=1
		disk_name = disk
		while i <= 10 :
			
			disk = disk+str(i)
			
	                DiskLine = str(os.popen("df -h | grep {0}".format(disk)).read())
	                DiskLine = DiskLine.strip("\n")
	                DiskLine = DiskLine.strip("\n")
	                #print(DiskLine)
			
	                DiskName = disk
	                DiskSize = str(os.popen("df -h | grep '{0}' | cut -c17-22".format(disk)).read())
	                DiskUsage = str(os.popen("df -h | grep '{0}' | cut -c22-27".format(disk)).read())
	                DiskAvai = str(os.popen("df -h | grep '{0}' | cut -c28-33".format(disk)).read())
	                DiskPercent = str(os.popen("df -h | grep '{0}' | cut -c34-38".format(disk)).read())
	                DiskMount = str(os.popen("df -h | grep '{0}' | cut -c39-100".format(disk)).read())
			#print("df -h | grep '/dev/xvda'"+i+" | cut -c25-29")
	
	                DiskName = DiskName.strip("\n")
	                DiskSize = DiskSize.strip("\n")
	                DiskUsage = DiskUsage.strip("\n")
	                DiskAvai = DiskAvai.strip("\n")
	                DiskPercent = DiskPercent.strip("\n")
       		        DiskMount = DiskMount.strip("\n")
			
			if DiskSize == "":
				i += 1 
				continue
		
			elif DiskSize != "":
        	        	#print(DiskName)
        	        	#print(DiskSize)
        	        	#print(DiskUsage)
        	        	#print(DiskAvai)
        	        	#print(DiskPercent)
        	        	#print(DiskMount)
	
	                	Result="""
        	  	DISK Query Results:
	
	                Disk Name: """+DiskName+"""
	                Disk Size: """+DiskSize+"""
	                Disk Usage: """+DiskUsage+"""
	                Available: """+DiskAvai+"""
	                Used Percentual: """+DiskPercent+"""
	                Mountpoint: """+DiskMount+"""
	
	"""
				disk = disk_name
				i += 1
	                	print(Result)
			
	
	
DiskScan()
#PrintArray(DiskStrip())
#DiskWrite(DiskStrip())		
DiskAnalysis(DiskStrip())
DiskAnalysisPart(DiskStrip())
