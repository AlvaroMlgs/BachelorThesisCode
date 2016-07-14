import Tkinter
import ttk
import subprocess


window = Tkinter.Tk()
window.title("DroneKit Launcher")
try:
	window.iconbitmap('C:\\Users\\Usuario\\Documents\\GitHub\\quadcopters-tfg-lvaro\\Dronekit\\favicon.ico')
except:
	pass
window.resizable(0,0)

mainFrame=Tkinter.LabelFrame(window,relief=Tkinter.RIDGE)
mainFrame.grid(sticky=Tkinter.NS)

#### PLATFORM ####


platform=Tkinter.LabelFrame(mainFrame,text="Platform")
platform.grid(row=0,rowspan=2,column=0,padx=5,pady=5,ipadx=5,ipady=5,sticky=Tkinter.NS)


def changeSelection(*args):
	if str(platformValue.get())=="SITL":
		platformSITLlaunch.configure(state=Tkinter.NORMAL)
		mvpyPortText.configure(text="Port")
		mvpyAddress.set("tcp:127.0.0.1")
		mvpyPort.set("5760")
	elif str(platformValue.get())=="UAV":
		platformSITLlaunch.configure(state=Tkinter.DISABLED)
		mvpyPortText.configure(text="Baud rate")
		if str(platformUAVselect.get())=="USB":
			mvpyAddress.set("com6")
			mvpyPort.set("115200")
		elif str(platformUAVselect.get())=="Telemetry":
			mvpyAddress.set("com4")
			mvpyPort.set("57600")
		else:
			mvpyAddress.set("")
			mvpyPort.set("")

def launchSitl():
	openCMD='START CMD /K '
	sitlRoute='"C:\\Users\\Usuario\\Google Drive\\TFG Alvaro Melgosa Pascual\\WinPython-64bit-2.7.10.3\\python-2.7.10.amd64\\Scripts\\dronekit-sitl.exe" '
	sitlArgs='copter-v3.2.1 --model x --home=40.333266, -3.765728,620,0'
	subprocess.call(openCMD + sitlRoute + sitlArgs, shell=True)


platformValue=Tkinter.StringVar()

platformSITL=Tkinter.Radiobutton(platform,text="SITL",variable=platformValue,value="SITL",command=changeSelection)
platformSITL.grid(row=0,column=0,padx=5,pady=5)

platformSITLlaunch=Tkinter.Button(platform,text="Launch",command=launchSitl,width=8)
platformSITLlaunch.grid(row=0,column=1,padx=5,pady=5)

platformUAV=Tkinter.Radiobutton(platform,text="UAV",variable=platformValue,value="UAV",command=changeSelection)
platformUAV.grid(row=1,column=0,padx=5,pady=5)

platformUAVconnect=Tkinter.StringVar()
platformUAVselect=ttk.Combobox(platform,width=7,textvariable=platformUAVconnect)
platformUAVselect['values']=("USB","Telemetry")
platformUAVselect.bind("<<ComboboxSelected>>",changeSelection)
platformUAVselect.grid(row=1,column=1,padx=5,pady=5)


#### MAVPROXY ####

mvpy=Tkinter.LabelFrame(mainFrame,text="MAVProxy",relief=Tkinter.GROOVE)
mvpy.grid(row=0,rowspan=2,column=1,padx=5,pady=5,ipadx=5,ipady=5,sticky=Tkinter.NS)


def launchMavproxy(address,port):
	openCMD='START CMD /K '
	mavproxyRoute='"C:\\Users\\Usuario\\Google Drive\\TFG Alvaro Melgosa Pascual\\MAVProxy\\mavproxy.exe" '
	if address[0:3]=="com":
		mavproxyArgs=' --master=' + address + ' --baud=' + port + ' --out=127.0.0.1:14550 --out=127.0.0.1:14551'
	else: 
		mavproxyArgs=' --master=' + address + ':' + port + ' --out=127.0.0.1:14550 --out=127.0.0.1:14551'
	subprocess.call(openCMD + mavproxyRoute + mavproxyArgs, shell=True)

mvpyAddressText=Tkinter.Label(mvpy,text="Address")
mvpyAddressText.grid(row=0,column=0,padx=5,pady=5,sticky=Tkinter.E)

mvpyAddress=Tkinter.StringVar()
mvpyAddressValue=Tkinter.Entry(mvpy,textvariable=mvpyAddress,width=12)
mvpyAddressValue.grid(row=0,column=1,padx=5,pady=5)

mvpyPortText=Tkinter.Label(mvpy,text="Baud rate")
mvpyPortText.grid(row=1,column=0,padx=5,pady=5,sticky=Tkinter.E)

mvpyPort=Tkinter.StringVar()
mvpyPortValue=Tkinter.Entry(mvpy,textvariable=mvpyPort,width=12)
mvpyPortValue.grid(row=1,column=1,padx=5,pady=5)

mvpyConnect=Tkinter.Button(mvpy,text="Connect",command=lambda:launchMavproxy(str(mvpyAddress.get()),str(mvpyPort.get())))
mvpyConnect.grid(row=2,column=1,padx=5,pady=5,sticky=Tkinter.E)


#### SCRIPT ####

script=Tkinter.LabelFrame(mainFrame,text="Script",relief=Tkinter.GROOVE)
script.grid(row=0,column=2,padx=5,pady=5,ipadx=5,ipady=5)

def runScript(route):
	openCMD='START CMD /K '
	scriptRoute='"C:\\Users\\Usuario\\Documents\\GitHub\\quadcopters-tfg-lvaro\\Dronekit\\"' + route
	subprocess.call(openCMD + scriptRoute, shell=True)

scriptLabel=Tkinter.Label(script,text="File location")
scriptLabel.grid(row=0,column=0,padx=5,pady=5)

scriptFileLocation=Tkinter.StringVar()
scriptFile=Tkinter.Entry(script,textvariable=scriptFileLocation,width=15)
scriptFile.grid(row=1,column=0,padx=5)

scriptRun=Tkinter.Button(script,text="Run script",command=lambda:runScript(str(scriptFileLocation.get())))
scriptRun.grid(row=1,column=1,padx=5,pady=5)


#### MISSION PLANNER ####

def launchPlanner():
	openCMD='START CMD /K '
	plannerRoute='"C:\\Program Files (x86)\\Mission Planner\\MissionPlanner.exe"'
	subprocess.call(openCMD + plannerRoute, shell=True)

planner=Tkinter.Button(mainFrame,text="Launch Mission Planner",command=launchPlanner)
planner.grid(column=2,row=1,padx=5,pady=5)




window.mainloop()


