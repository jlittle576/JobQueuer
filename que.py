import sys, os, shutil, glob, copy, time, datetime, inspect, re, random, math
from collections import OrderedDict
from dateutil import tz
from utilities import *

TICK = 0
LOOP_TICK = 0


def tick():
    global TICK, LOOP_TICK
    # print 'tick %s   loop_tick: %s' % (TICK, LOOP_TICK)

    if TICK == 30:
        _ = 0

    TICK += 1
    LOOP_TICK += 1



# setup sentinels
RUN_MODE = RUN_DOE
RETURN_TO_QUE = False
FILE_TRANSFER_WAIT_TIME = 10
# QUE_TOP_DIR = '//192.168.10.254/kdev_que_1/' #

# development settings
DEV_MODE = False
if os.path.isdir('C:/Users/Joe/Dropbox/code/projects'):   # like, omg, super advanced user detected
    #
    # kill_adams()
    # DEV_MODE = True
    #
    # TEST_TRANSFER_WAIT = True
    # TEST_QUE_MOD = True
    ADAMS_START_LIMIT = 60
    RUN_MODE = RUN_DOE
    RETURN_TO_QUE = True
    # DOE_COMPLETE_STRING = SINGLE_COMPLETE_STRING
    FILE_TRANSFER_WAIT_TIME = 2
    # TEST_QUE_ADD = False


# ToDo: Handle folders that are being transferred
# ToDo: add check for current status instead of just queueing
# ToDo: handle popup errors
# ToDo: implement basic error message / timeout


def log(msg):
    ts =  datetime.datetime.now().strftime('%m/%d %H:%M:%S - ')

    key_sep = re.findall('^([A-Z]+)\s+(.*)', msg)
    if len(key_sep)>0:
        msg = '%-15s%s' % key_sep[0]
    msg = ts + msg

    print msg

    f_add('que.log', msg + '\n')


def main():

    # -- path setup --

    fl_self = slash_fix(os.path.realpath(__file__))
    print fl_self
    if not '/source_queuer' in fl_self.lower():
        raise Exception('File path initialization fail, "/source_queuer" folder not in path')
    else:
        top_dir = os.path.dirname(fl_self)
        if '/source_queuer' in fl_self.lower():
            top_dir = os.path.dirname(top_dir)

    os.chdir(top_dir)
    print 'Initialzing at top_dir: %s' % top_dir

    if 0:  # scratch code testing

        m_time = os.path.getmtime(top_dir + '/que/FOR_JR_4250K_model')
        mins_since_mod = (time.time() - m_time) / 60.0

    elif 1:  # run testing

        # -- test code --
        test_pat_folders = fl_get(top_dir + '/queTest*_model') + fl_get(top_dir + '/que/queTest*_model')
        f_write('que.log', '')
        os.system('start taskkill.exe /F /IM aview* /T')

        for fol in test_pat_folders:
            pat_run_fol = fol.replace('/que/queTest', '/queTest')
            pat_que_fol = fol if '/que/' in fol else fol.replace('queTest', 'que/queTest')

            # # sub to que transfer
            if RETURN_TO_QUE:
                if os.path.isdir(pat_run_fol):
                    shutil.move(pat_run_fol, pat_que_fol)

                # # set folder m_time for transfer wait testing
                # if TEST_TRANSFER_WAIT:
                #     mod_file = pat_que_fol + '/test'
                #     if os.path.isfile(mod_file):
                #         os.remove(mod_file)
                #     f_add(mod_file, '!')

        # dummy file cleanup
        temp_files = fl_get(top_dir + 'queTest*dummyTemp_model') + fl_get(top_dir + 'que/queTest*dummyTemp_model')
        for dummy_fl in temp_files:
            try:
                os.remove(dummy_fl)
            except:
                log('Warning, could not remove dummy file:' + dummy_fl)

        # -- que init --

        jobque = JoeQue(top_dir)
        jobque.start()


class JoeQue(object):
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.num_running = 0
        self.max_que = 1
        self.jobs = OrderedDict()
        self.que_input_path = top_dir + '/que'
        # self.get_stats()
        self.cmds_path = top_dir + '/que.commands'
        self.num_completed = 0
        self.que_order_inputs = []

    def add(self, model_fol):
        # status = self.check_transfer_complete(model_fol)
        self.jobs[copy.copy(model_fol)] = Job(self, model_fol)


    def export_que_list(self):
        # print 'Exporting...'

        ts = datetime.datetime.now().strftime('%m/%d %H:%M:%S')
        list = '''# Written %s
# To Reorder
#   - copy this file
#       > windows explorer copy is fine, which will give a name like que_order - Copy.csv
#       > though any name other than que_order.csv or que_order_mod.csv is fine
#   - in the copied file, reorder the jobs
#   - save as que_order_mod.csv, which will be immediately read and deleted if que is running
#   - que_order.csv (constantly updated) should be contain your new imputs
#
# Notes:
#  - order/presence of jobs which are complete doesn't matter
#  - only neccessary syntax is folder name, 1 per line, status is ignored

#
''' % ts


        def que_print_sort(k):
            prio = {COMPLETE: 1, FAILED: 2, RUNNING: 3}
            status = self.jobs[k].status
            return prio[status] if status in prio else (self.jobs.keys().index(k) + 10)

        keys = sorted(self.jobs.keys(), key=que_print_sort)
        # keys = self.jobs.keys()

        ks = [(k,self.jobs[k].status) for k in keys]

        for k, s in ks:
            if 'RUN' in s:
                _ = 0
        for k in keys:
            job = self.jobs[k]
            run_type = job.run_type.replace('_run', '').lower().title()
            list += '%s,%s,run_type=%s\n' % (job.path, job.status, run_type)
        f_write('que_order.csv', list)

    def manage_que_order(self):
        """Called anytime the que order is modified
                > que_order_mod.csv detected
                > job completion
                > que add
                > kill advance command
                """

        if os.path.exists('que_order_mod.csv'):
            list_mod = f_read('que_order_mod.csv').split('\n')
            os.remove('que_order_mod.csv')
            self.que_order_inputs = []

            for line in list_mod:
                for job in self.jobs:
                    if self.jobs[job].pat_name in line:
                        self.que_order_inputs.append(job)

                    for k, v in re.findall('(\w+)=(\w+)', line):
                        self.jobs[job].__dict__[k] = v
                        log('%s: %s set to %s' % (job, k, v))


        new_list = copy.copy(self.que_order_inputs)
        for job in self.jobs.keys():
            if not job in new_list:
                    new_list.append(job)

        self.old_jobs = copy.copy(self.jobs)
        self.jobs = OrderedDict()
        for name in new_list:
            job = self.old_jobs[name]
            self.jobs[name] = job

    def randomize_que(self):
        # create a new que order list
        self.export_que_list()
        new_job_order = re.findall('queTest.*_model', f_read('que_order.csv'))
        random.shuffle(new_job_order)
        f_write('que_order_mod.csv', '\n'.join(new_job_order))

    def get_job_by_patient(self, pat):
        for job in self.jobs.values():
            # print '||', job
            if pat in job.path:
                return job
        else:
            return None

    def folder_status_query(self, fol):

        for job in self.jobs:
            if os.path.basename(job) == os.path.basename(fol):
                return self.jobs[job].status
        return None
        # pat = os.path.basename(fol).replace('_model', '')
        # job = self.get_job_by_patient(pat)
        # return job.status if job is not None else None

    def start(self):
        """Main program loop"""

        watch = None
        notify_on_finish = True
        # kill_adams()
        i = 0

        timers = True
        while 1:

            global LOOP_TICK
            LOOP_TICK = 0

            # loop init
            done = False
            time.sleep(0.25)

            # test functions
            if TEST_QUE_ADD and self.num_completed == 2:
                pat_run_fol = fl_get('queTest*_model')[0]
                if not self.top_dir in pat_run_fol: pat_run_fol = self.top_dir + pat_run_fol
                pat_sub_fol = pat_run_fol.replace('/queTest', '/que/queTest').replace('queTest_', 'queTest_dupe_')
                os.mkdir(self.top_dir+'que/queTest_dummyTemp_model')


            # check for new folders
            # ToDo: check for redundant folders in que/run dirs
            # ToDo: assign que order based on mod time of new folders
            for model_fol in fl_get(self.que_input_path + '/*_model'):
                if self.folder_status_query(model_fol) not in [QUEUED, WAITING_FOR_TRANSFER_COMPLETION]:
                    # print '++%s - %s' % (model_fol, self.folder_status_query(model_fol))
                    self.add(model_fol)
                    i += 1
                    if i > 5:
                        _ = 0

            # check for run completion
            for job in self.jobs.values():
                if job.status == RUNNING:
                    if job.check_complete():
                        self.num_running -= 1
                        self.num_completed += 1

            # check for transfer completion
            for job in self.jobs.values():
                if job.status == WAITING_FOR_TRANSFER_COMPLETION:
                    job.check_transfer_complete()

            # test functions
            # if (self.num_running < self.max_que):
            if (self.num_running < self.max_que) and TEST_QUE_MOD and (self.num_completed == 1):
                self.randomize_que()

            # submission
            self.num_running = 0
            for job in self.jobs.values():
                if job.status == RUNNING:
                    self.num_running += 1

            finished = True
            for name, job in self.jobs.items():
                tick()
                if job.status in [QUEUED, WAITING_FOR_TRANSFER_COMPLETION, RUNNING]:
                    tick()

                    notify_on_finish = True
                    finished = False
                if (job.status == QUEUED) and self.num_running < self.max_que:
                    tick()

                    self.num_running += 1
                    job.submit()
                    self.current_job = name
            if finished and notify_on_finish:
                notify_on_finish = False
                log('No remaining jobs in que! (Still monitoring que dir...)')


            # que_order.csv interaction
            if os.path.isfile('que_order_mod.csv'):
                self.manage_que_order()
            self.export_que_list()

            # external command interations
            cmd_opts = ['kill_after_job', 'kill_advance', 'kill_quit']
            if os.path.isfile(self.cmds_path):
                commands = f_read(self.cmds_path)
                for cmd in cmd_opts:
                    if cmd in commands:
                        log('EXECUTING external command: ' + cmd)
                        break

                cmd = '>' + cmd

                # f_write(self.cmds_path, '')
                os.remove(self.cmds_path)
                for cmd in commands.split('\n'):
                    if 'stop' in cmd:
                        done = True
                        log('STOP command entered, queuer process stopped...')
                    if 'kill_advance' in cmd:
                        log('KILL_ADVANCE command entered, killing current job and running next in que')
                        kill_adams()
                        self.jobs[self.current_job].set_status('KILLED')
                        self.manage_que_order()

                    if 'kill_quit' in cmd:
                        done = True
                        log('KILL_STOP command entered, killing current job and exiting queuer')
                        self.jobs[self.current_job].set_status('KILLED')
                        kill_adams()

            if done: break


class Job(object):
    def __init__(self, parent, model_dir):
        # print '}I}:%s' % model_dir
        self.parent = parent
        self.queued_path = model_dir  # assumption that only folders in que dir path are initialized
        self.path = model_dir
        self.pData_text = f_read(self.path + '/PatientData.csv')
        self.analysisType = re.findall('analysisType,(\w+)', self.pData_text)[0]
        self.run_type = SINGLE if self.analysisType.lower() in 'postop ' else FULL
        self.fol_name = os.path.basename(self.path)
        self.stat_path = model_dir + '/que.stat'
        self.status = 'INITIALIZED'
        self.substatus = None
        self.fol_size = 0
        # print 'I:',self.fol_name
        self.time_of_last_size_change = 0
        self.last_transfer_status_msg_time = datetime.datetime.utcnow()
        # self.set_status(QUEUED)
        # print 'init'
        self.check_transfer_complete()
        self.pat_name = self.fol_name.replace('_model', '')
        self.submitted_path = os.path.dirname(os.path.dirname(self.queued_path)) + '/' + self.fol_name
        self.res_folder = None
        self.ocdlog_path = None


    def short_path(self):
        return self.path.replace(self.parent.top_dir, os.path.basename(self.parent.top_dir))

    def submit(self):

        if os.path.isdir(self.submitted_path):
            log('Cannot submit %s because %s already exists' % (self.queued_path, self.submitted_path))
        shutil.move(self.queued_path, self.submitted_path)
        self.path = self.submitted_path
        log('MOVED %s >> %s' % (self.pat_name, self.short_path()))
        self.submit_time = time.time()

        for fl in glob.glob('./*command'):
            os.remove(fl)

        self.set_status(RUNNING, WAITING_FOR_ADAMS_START)

        f_write('ocdjoblist.csv', '#,Name\n1,' + self.pat_name)
        f_write('ocdrunlist.txt', '1')

        cmd_name = 'adams_run_full.command' if self.run_type == FULL else 'adams_run_single.command'

        if RUN_MODE == SPOOF_SINGLE:

            f_write('adams_spoof_run.command', '')
            os.system('start C:/MSC.Software/Adams_x64/2014_0_1/common/mdi.bat aview ru-st i')
            self.res_folder = '%s/%s_dummyResults_model_%s' % (
            self.submitted_path, self.pat_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            self.ocdlog_path = '%s/ocdlog_dummy.txt' % self.res_folder
            os.mkdir(self.res_folder)
            f_write(self.ocdlog_path, 'Information: Model creation complete')

        elif RUN_MODE == SPOOF_DOE:

            f_write('adams_spoof_run.command', '')
            os.system('call C:/MSC.Software/Adams_x64/2014_0_1/common/mdi.bat aview ru-st i')
            self.res_folder = '%s/%s_dummyResults_model_%s' % (
            self.submitted_path, self.pat_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            self.ocdlog_path = '%s/ocdlog_dummy.txt' % self.res_folder
            os.mkdir(self.res_folder)

        elif RUN_MODE == RUN_DOE:

            f_write(cmd_name, '')
            os.system('C:/MSC.Software/Adams_x64/2014_0_1/common/mdi.bat aview ru-st i')
            # os.system('start cmd.exe /C start __adams__start_and_run_current.bat')

    def check_transfer_complete(self):
        """Makes sure a certain amount of time has pasted since las mod date changed"""
        mod_time = datetime.datetime.utcfromtimestamp(os.path.getmtime(self.path))
        current_time = datetime.datetime.utcnow()
        secs_since_m_time = (current_time - mod_time).total_seconds()


        new_size = int(get_dir_size(self.path))

        if self.time_of_last_size_change == 0:
            self.time_of_last_size_change = copy.copy(current_time)
        if new_size > (self.fol_size+1):
            # print '\nnew_size > (self.fol_size+1)'
            # print '  self.fol_name   :', self.fol_name
            # print '  new_size        :', new_size
            # print '  self.fol_size   :', self.fol_size
            self.fol_size = copy.copy(new_size)
            self.time_of_last_size_change = copy.copy(current_time)
        # else:
        #     print '<='

        self.secs_since_filesize_change = (current_time - self.time_of_last_size_change).total_seconds()


        # print 'current_time                   ',  current_time
        # print 'mod_time                       ',  mod_time
        # print 'self.time_of_last_size_change  ',  self.time_of_last_size_change
        # print 'self.secs_since_filesize_change',  self.secs_since_filesize_change


        # import datetime
        # # import os
        # dt = os.path.getmtime(self.path)
        # print (datetime.datetime.fromtimestamp(dt))
        # print (datetime.datetime.utcfromtimestamp(dt))
        #
        # print self.short_path(), secs_since_m_time, self.status
        # print self.short_path(), current_time, self.time_of_last_size_change, self.secs_since_filesize_change

        # print 'ctc'
        if self.secs_since_filesize_change > FILE_TRANSFER_WAIT_TIME:
            self.set_status(QUEUED)
        else:
            self.set_status(WAITING_FOR_TRANSFER_COMPLETION)

    def check_complete(self):

        if 'DOE' in RUN_MODE:
            if 'ful' in self.run_type.lower():
                ocdlog_complete_test = DOE_COMPLETE_STRING
            else:
                ocdlog_complete_test = SINGLE_COMPLETE_STRING
        elif 'SINGLE' in RUN_MODE:
            ocdlog_complete_test = SINGLE_COMPLETE_STRING

        res_folders = fl_get('%s/%s*model_20*' % (self.path, self.pat_name))
        if len(res_folders) > 0:
            new_res_fol = sorted(res_folders)[-1]
            new_res_fol_m_time = os.path.getmtime(new_res_fol)
            if new_res_fol_m_time > self.submit_time:
                self.res_folder = new_res_fol
                self.set_status(RUNNING, MONITORING_ADAMS_LOG)



        self.timeouts = [(WAITING_FOR_ADAMS_START, ADAMS_START_LIMIT, 'Adams failed to start or load the patient properly within %(secs_since)s, please check for model/license issues'),
                         (MONITORING_ADAMS_LOG, 60*60, 'Terminating adams run, failed to complete after %(mins_since)s, please check OCD log for issues')]

        for condition, limit, timeout_msg in self.timeouts:
            if self.substatus == condition:
                secs_since = seconds_since(self.substatus_time)
                mins_since = secs_since / 60.0
                if secs_since > limit:
                    kill_adams()
                    log(timeout_msg % locals())
                    log('Killing Adams')
                    self.set_status(FAILED, TIMED_OUT)
                    return True


        # ts_old = self.prev_res_fol.split('model_')[1]
        # ts_new = new_res_fol.split('model_')[1]
        # if not (ts_old[1:] in ts_new):
        #     if not (self.res_folder == new_res_fol):
        #         log('FOUND new res folder %s' % new_res_fol)
        #     self.res_folder = new_res_fol

        if self.res_folder is not None:
            ocdlog_search = fl_get('%s/ocdlog*.txt' % self.res_folder)
            if len(ocdlog_search) == 1:
                new_ocdlog_path = fl_get('%s/ocdlog*.txt' % self.res_folder)[0]
                if not new_ocdlog_path == self.ocdlog_path:
                    log('FOUND ocdLog: %s' % new_ocdlog_path)
                    log('   Waiting for file to contain string: "%s"' % ocdlog_complete_test)
                self.ocdlog_path = new_ocdlog_path

        if self.ocdlog_path is not None:
            if 'SPOOF' in RUN_MODE:
                if os.path.isfile('./adams_done.command'):
                    # print '>> spoof.done found'
                    os.remove('./adams_done.command')
                    f_write(self.ocdlog_path, 'RUNSTUDY COMPLETE Information: Model creation complete')
                else:
                    f_write(self.ocdlog_path, 'Im not dead yet!!')

            ocdlog = f_read(self.ocdlog_path)

            # complete test
            if ocdlog_complete_test in ocdlog:
                self.set_status(COMPLETE)
                return True

            # fail test
            elif 'Aborting model build' in ocdlog:
                log("'Aborting model build' found in ocdlog, aborting. See ocdlog (path above) for more info.")
                kill_adams()
                self.set_status(FAILED)
                return True

        return False

    def set_status(self, status, substatus=None):
        old_status = copy.copy(self.status)

        job_info = 'status:%s\n' % self.status

        for k, v in self.__dict__.items():
            job_info += '  %s: %s\n' % (k, v)


        msg = '%s %s (%s)' % (status, self.short_path(), self.run_type)
        if status in [WAITING_FOR_TRANSFER_COMPLETION]:
            msg += ' (folder size increased %s secs ago, waiting for %s)' % (int(self.secs_since_filesize_change), FILE_TRANSFER_WAIT_TIME)

        # time_since_last_transfer_status_update = int((time_now() - self.last_transfer_status_msg_time).total_seconds())

        if status is not self.status:
            if 'RUN' in status:
                _ = 0
            self.last_transfer_status_msg_time = datetime.datetime.now()
            self.status = status
            self.status_time = time_now()
            # if not self.status == WAITING_FOR_TRANSFER_COMPLETION:
            #     f_write(self.path+'/que.stat', job_info)

            log(msg)

        if substatus is not self.substatus:
            self.substatus = substatus
            self.substatus_time = time_now()

            # log(msg)

        # elif time_since_last_transfer_status_update > 10:
        #     self.last_transfer_status_msg_time = datetime.datetime.now()
        #     log(msg)

        # ToDo: Periodic updates about trandser wait time

        self.parent.manage_que_order()

if __name__ == '__main__':
    main()
