! suppress alerts
var set var = .ocdl.suppress_alerts int = 0
	
	
int push cre push =  .gui.main.mmenu_menu.mbar_refresh.tools.ocd_run label = "OCD Run Model::Ctrl+F6" com = 'fil com rea fil = "adams_run_current.command"'
	 
	 
!debug tools for joe
if c=0!( FILE_EXISTS( GETCWD()//'/adams_joe_debug.command') || FILE_EXISTS('C:/Users/Joe/Dropbox/code/scratch') )
	lib cre lib = .su
	var set var = .su.path string = "C:/kdev_que/sU"
	var set var = .su.local_dir string = "C:/kdev_que/sU"
	file com read file = (eval( (eval( .su.path )) // "/sU_setup.cmd" ))

end	


var set var=.___fileIsThere integer=(eval( file_exists(.OCDdir // "ocd_runBatch_input.txt") ))
if c=( eval(.___fileIsThere) )
   !*** batch process
	var set var = .ocdl.suppress_alerts int = 1
   system send=off echo=off command="del ocdlog.txt"
   ocd alert file="ocdlog_runBatch.txt" text=" "
   ocd alert file="ocdlog_runBatch.txt" text="Starting OCD Batch processing"
   ocd runBatch measures=no runSimulation=yes
   quit
   
elseif c=(FILE_EXISTS( GETCWD()//'/adams_spoof_run.command' ))
	var set var = .ocdl.suppress_alerts int = 1

	var set var = .gui.py int= (eval(run_python_code("import time")))
	var set var = .gui.py int= (eval(run_python_code("time.sleep(5)")))
	var set var = .gui.py int= (eval(run_python_code("open('./adams_done.command','w')")))
	quit

!elseif c=((FILE_EXISTS( GETCWD()//'/adams_run_single_noCP.command' )) || (FILE_EXISTS( GETCWD()//'/adams_run_full_noCP.command' ))|| (FILE_EXISTS( GETCWD()//'/adams_run_single_wCP.command' ))|| (FILE_EXISTS( GETCWD()//'/adams_run_full_wCP.command' )))
elseif c=((FILE_EXISTS( GETCWD()//'/adams_run_current.command' )) )
	var set var = .ocdl.suppress_alerts int = 1
	
	fil com rea fil = (eval( GETCWD()//'/adams_run_current.command' ))

	!quit
end

