
var set var=.OCDreleaseNumber         str="1.5"
var set var=.OCDreleaseDate           str="22-Sep-2015"

if c=(eval( FILE_EXISTS('C:/Users/Joe/Dropbox/code/scratch/sU_temp_static')))    ! local build (for joe)

	var set var=.OCDdir                   str="C:/Users/Joe/Dropbox/code/projects/queuer/"
	var set var=.OCDdir_local             str="C:/Users/Joe/Dropbox/code/projects/queuer/","C:/Users/Joe/Dropbox/code/projects/queuer/"
	var set var=.Implant_Library_Hip_dir  str="C:/OO_Production/Implant_Library_Hip/"
	var set var=.Implant_Library_Knee_dir str="C:/OO_Production/Implant_Library_Knee/"

else																			! normal production build

	var set var=.OCDdir                   str="//DATASERVER/kdev_que_1/"
	var set var=.OCDdir_local             str="//DATASERVER/kdev_que_1/","U:/"
	var set var=.Implant_Library_Hip_dir  str="//DATASERVER/OO_Production/Implant_Library_Hip/"
	var set var=.Implant_Library_Knee_dir str="//DATASERVER/OO_Production/Implant_Library_Knee/"
	
end

var set var=.LocalTempFolder		  str="C:/Temp/"
var set var=.ffmepgFile 			  str="C:/ffmpeg.exe"

file command read file=(eval( .OCDdir // "source_KNEE/macros/OCDL_Load.cmd" ))
model cre mod=.MOD
ocd disp panel=runModel

! suppress alerts
var set var = .ocdl.suppress_alerts int = 1
	
!debug tools for joe
if c=0!( FILE_EXISTS( GETCWD()//'/adams_joe_debug.command') || FILE_EXISTS('C:/Users/Joe/Dropbox/code/scratch') )
	lib cre lib = .su
	var set var = .su.path string = "C:/kdev_que/sU"
	var set var = .su.local_dir string = "C:/kdev_que/sU"
	file com read file = (eval( (eval( .su.path )) // "/sU_setup.cmd" ))

end	

if c=(FILE_EXISTS( GETCWD()//'/adams_spoof_run.command' ))

	var set var = .gui.py int= (eval(run_python_code("import time")))
	var set var = .gui.py int= (eval(run_python_code("time.sleep(10)")))
	var set var = .gui.py int= (eval(run_python_code("open('./adams_done.command','w')")))
	quit

elseif c=(FILE_EXISTS( GETCWD()//'/adams_run_que.command' ))

	var set var = .gui.py int= (eval(run_python_code("import glob, os, aview_main")))
	var set var = .gui.py int= (eval(run_python_code("fIn=open('ocdjoblist.csv').read()")))
	var set var = .gui.py int= (eval(run_python_code("print fIn")))
	var set var = .gui.py int= (eval(run_python_code("pat = fIn.split('1,')[1].split('2,')[0].rstrip()")))
	var set var = .gui.py int= (eval(run_python_code("print pat")))
	var set var = .gui.py int= (eval(run_python_code("fl = os.path.abspath(glob.glob('./'+pat+'*')[0]).replace('\\\\','/')")))
	var set var = .gui.py int= (eval(run_python_code("print fl")))
	
	var set var = .gui.py int= (eval(run_python_code("aview_main.execute_cmd('var set var = .mod.path str = %s%s%s' % (chr(39), fl ,chr(39)))")))
	
	int fie set fie = .gui.msg_box.message act = append str = '', (eval( 'Reading ' // .mod.path // '/PatientData.csv..' ))
	int fie set fie = dbox_runModel.field_fileName str = (eval( .mod.path // "/PatientData.csv"))
	int pus exe pus = dbox_runModel.toggle_compplace
	
	
	var set var = .gui.py int= (eval(run_python_code("import glob, os, aview_main")))
	var set var = .gui.py int= (eval(run_python_code("fIn=open('ocdjoblist.csv').read()")))
	var set var = .gui.py int= (eval(run_python_code("print fIn")))
	var set var = .gui.py int= (eval(run_python_code("pat = fIn.split('1,')[1].split('2,')[0].rstrip()")))
	var set var = .gui.py int= (eval(run_python_code("print pat")))
	var set var = .gui.py int= (eval(run_python_code("fl = os.path.abspath(glob.glob('./'+pat+'*')[0]).replace('\\\\','/')")))
	var set var = .gui.py int= (eval(run_python_code("print fl")))
	var set var = .gui.py int= (eval(run_python_code("aview_main.execute_cmd('var set var = .mod.path str = %s%s%s' % (chr(39), fl ,chr(39)))")))
	
	
	int fie set fie = .gui.msg_box.message act = append str = '', (eval(  'Exporting ' // .mod.path // '/ComponentPlacement.csv..' ))
	int fie set fie = dbox_compplacement.field_fileName str = (eval( .mod.path // "/ComponentPlacement.csv"))
	int pus exe pus = dbox_compplacement.button_export

	
	var set var = .gui.py int= (eval(run_python_code("import glob, os, aview_main")))
	var set var = .gui.py int= (eval(run_python_code("fIn=open('ocdjoblist.csv').read()")))
	var set var = .gui.py int= (eval(run_python_code("print fIn")))
	var set var = .gui.py int= (eval(run_python_code("pat = fIn.split('1,')[1].split('2,')[0].rstrip()")))
	var set var = .gui.py int= (eval(run_python_code("print pat")))
	var set var = .gui.py int= (eval(run_python_code("fl = os.path.abspath(glob.glob('./'+pat+'*')[0]).replace('\\\\','/')")))
	var set var = .gui.py int= (eval(run_python_code("print fl")))
	var set var = .gui.py int= (eval(run_python_code("aview_main.execute_cmd('var set var = .mod.path str = %s%s%s' % (chr(39), fl ,chr(39)))")))
	
	int fie set fie = .gui.msg_box.message act = append str = '', (eval( 'Running ' // .mod.path // '/PatientData.csv Single Run..' ))
	int tog mod tog=.OCDL.dbox_runModel.toggle_RandD state=off
	int pus exe pus = .OCDL.dbox_runModel.button_apply

	
	var set var = .gui.py int= (eval(run_python_code("import glob, os, aview_main")))
	var set var = .gui.py int= (eval(run_python_code("fIn=open('ocdjoblist.csv').read()")))
	var set var = .gui.py int= (eval(run_python_code("print fIn")))
	var set var = .gui.py int= (eval(run_python_code("pat = fIn.split('1,')[1].split('2,')[0].rstrip()")))
	var set var = .gui.py int= (eval(run_python_code("print pat")))
	var set var = .gui.py int= (eval(run_python_code("fl = os.path.abspath(glob.glob('./'+pat+'*')[0]).replace('\\\\','/')")))
	var set var = .gui.py int= (eval(run_python_code("print fl")))
	var set var = .gui.py int= (eval(run_python_code("aview_main.execute_cmd('var set var = .mod.path str = %s%s%s' % (chr(39), fl ,chr(39)))")))
	
	int fie set fie = .gui.msg_box.message act = append str = '', (eval( 'Running ' // .mod.path // '/PatientData.csv Beta..' ))
	int tog mod tog=.OCDL.dbox_runModel.toggle_RandD state=on
	int pus exe pus = .OCDL.dbox_runModel.button_apply

	quit
end

