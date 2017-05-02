! suppress alerts
var set var = .ocdl.suppress_alerts int = 0
	
!debug tools for joe
if c=0!( FILE_EXISTS( GETCWD()//'/adams_joe_debug.command') || FILE_EXISTS('C:/Users/Joe/Dropbox/code/scratch') )
	lib cre lib = .su
	var set var = .su.path string = "C:/kdev_que/sU"
	var set var = .su.local_dir string = "C:/kdev_que/sU"
	file com read file = (eval( (eval( .su.path )) // "/sU_setup.cmd" ))

end	

if c=(FILE_EXISTS( GETCWD()//'/adams_spoof_run.command' ))
	var set var = .ocdl.suppress_alerts int = 1

	var set var = .gui.py int= (eval(run_python_code("import time")))
	var set var = .gui.py int= (eval(run_python_code("time.sleep(5)")))
	var set var = .gui.py int= (eval(run_python_code("open('./adams_done.command','w')")))
	quit

elseif c=((FILE_EXISTS( GETCWD()//'/adams_run_single.command' )) || (FILE_EXISTS( GETCWD()//'/adams_run_full.command' )))
	var set var = .ocdl.suppress_alerts int = 1

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

	if c=(FILE_EXISTS( GETCWD()//'/adams_run_full.command' ))
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
		
	end

	quit
end

