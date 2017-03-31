from PySide.QtCore import QFile
from PySide.QtCore import QTimer
from PySide.QtGui import QColor
from PySide.QtGui import QListWidgetItem
from PySide.QtUiTools import QUiLoader
from PySide import QtCore, QtGui, QtUiTools
from que import *
import time, os, stat
import subprocess

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


COMPLETED = 'COMPLETED'
QUEUED = 'QUEUED'
FAILED = 'FAILED'
RUNNING = 'RUNNING'
STOPPED = 'STOPPED'

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.initUI()

        self.que = JobList(self)


    def initUI(self):

        loader = QUiLoader()
        file = QFile("./Source_Queuer/gui.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        self.ui.setWindowIcon(QtGui.QIcon('C:/Users/Joe/Dropbox/code/projects/queuer/Source_Queuer/logo.png'))
        self.setWindowIcon(QtGui.QIcon('C:/Users/Joe/Dropbox/code/projects/queuer/Source_Queuer/logo.png'))
        file.close()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)

        connectBtn = QtGui.QPushButton("Connect", self)

        # connectBtn.clicked.connect(self.connectClicked)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_refresh)
        self.timer.start(1000)

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Sans Typewriter"))
        self.ui.list_order.setFont(font)


        self.ui.setWindowTitle('Window')
        self.ui.show()

        # connectors
        self.ui.list_order.LineWrapMode = 0
        self.ui.list_order.itemClicked.connect(self.on_list_modify)

        self.ui.btn_up.clicked.connect(self.btn_up)
        self.ui.btn_down.clicked.connect(self.btn_down)
        self.ui.btn_top.clicked.connect(self.btn_top)
        self.ui.btn_bottom.clicked.connect(self.btn_bottom)

        self.ui.btn_refresh.clicked.connect(self.refresh_from_file)
        self.ui.btn_stop.clicked.connect(self.stop_que)
        self.ui.btn_kill_advance.clicked.connect(self.kill_advance)
        self.ui.btn_kill_stop.clicked.connect(self.kill_stop)
        self.ui.btn_start.clicked.connect(self.start_que)
        self.ui.btn_open_folder.clicked.connect(self.open_folder)
        self.ui.chk_show_completed.stateChanged.connect(self.toggle_completed)

        # start-only widget initialization
        self.show_completed = self.ui.chk_show_completed.isChecked()


    def toggle_completed(self):
        print self.ui.chk_show_completed.isChecked()
        self.show_completed = self.ui.chk_show_completed.isChecked()


    def open_folder(self):
        path = self.que.get(self.ui.list_order.currentItem()).path

        path = path.replace('/', '\\')
        subprocess.Popen('explorer "{0}"'.format(path))

    def btn_up(self):
        self.que.reorder(self.active_job, -1)

    def btn_down(self):
        self.que.reorder(self.active_job, 1)

    def btn_top(self):
        self.que.reorder(self.active_job, 0, absolute=True)

    def btn_bottom(self):
        self.que.reorder(self.active_job, -1, absolute=True)

    def stop_que(self):
        f_write('que.commands', 'stop')

    def kill_advance(self):
        f_write('que.commands', 'kill_advance')

    def kill_stop(self):
        f_write('que.commands', 'kill_quit')

    def start_que(self):
        print os.getcwd()
        os.system('start python ./Source_Queuer/que.py')

    def on_list_modify(self):

        # job specific (de)activations
        self.active_job = self.que.get(self.ui.list_order.currentItem())
        if self.active_job.status in [COMPLETE, RUNNING]:
            self.ui.btn_reque.setEnabled(True)
        else:
            self.ui.btn_reque.setEnabled(False)

        # # que status
        # log_age = time.time() - os.stat('./que.log')[stat.ST_MTIME]
        # if log_age < 2.0:
        #     self.ui.setWindowTitle("JobQue    Queuer Status: Running")
        #     self.que_status = RUNNING
        #     self.ui.btn_stop.setEnabled(True)
        #     self.ui.btn_start.setEnabled(False)
        # else:
        #     self.ui.setWindowTitle("JobQue    Queuer Status: Not Running")
        #     self.que_status = STOPPED
        #     self.ui.btn_stop.setEnabled(False)
        #     self.ui.btn_start.setEnabled(True)

        # job info
        try:
            pData_path = glob.glob(self.active_job.path + '/PatientData.csv')[0]
            pData = f_read(pData_path)
        except:

            pData = False



        patInfo = {}
        mtime = os.path.getmtime(self.active_job.path)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))

        patInfo.update(locals())

        if pData:
            self.ui.text_job_info.setText(pData_path)
            for line in pData.split('\n'):
                row = line.split(',')
                if len(row) > 1:
                    patInfo[row[0]] = row[1]


            info_text='''%(pData_path)s
    Name: %(patientFirstName)s %(patientLastName)s
    Side: %(side)s
    Surgeon: %(surgeon)s
    Queued: %(mtime)s
    ''' % patInfo

        else:
            info_text = "could not find PatientData.csv"

        self.ui.text_job_info.setText(info_text)


    def loop_refresh(self):


        # print '!'
        """Check que_order.csv for updates and various other status updates, happens every 50ms"""

        # log

        que_running = False

        if os.path.isfile('que.log'):

            m_time = os.path.getmtime('que_order.csv')
            que_log_age = time.time() - m_time

            if que_log_age > 30:  # que no active
                if que_log_age < 119:
                    age = '%s seconds' % int(int(que_log_age/5) * 5)
                elif  que_log_age < 7200:
                    age = '%s minutes' % str(int(que_log_age/60.0))
                else:
                    age = '%s hours' % str(int(que_log_age/60.0))
                self.ui.label_que_log.setText('Que log (not updated in %s)' % age)

                que_running = False



            else:
                self.ui.label_que_log.setText('Que log')
                que_running = True
                # self.ui.btn_stop.setEnabled(False)
                # self.ui.btn_start.setEnabled(True)

                self.ui.setWindowTitle('JobQueuer Queuer Status: Not Running')


            self.ui.text_log.setText(f_read('que.log'))
            self.ui.text_log.verticalScrollBar().setValue(self.ui.text_log.verticalScrollBar().maximum())

        else:

            self.ui.text_log.setText('que.log not detected in current dir')

        if que_running:
            # self.ui.btn_stop.setEnabled(True)
            # self.ui.btn_start.setEnabled(False)
            self.ui.setWindowTitle('JobQueuer Queuer Status: Running')
        else:
            # self.ui.btn_stop.setEnabled(False)
            # self.ui.btn_start.setEnabled(True)
            self.ui.setWindowTitle('JobQueuer Queuer Status: Not Running')

        self.refresh_from_file(update_only=True)

    def refresh_from_file(self, update_only=False):

        # print '!!'
        lines = f_read('./que_order.csv').split('\n')
        rows = [x.split('#')[0].split(',') for x in lines]
        rows = [x for x in rows if len(x) > 1]

        old_jobs = [(x.path, x.status) for x in self.que.list]

        if len(old_jobs) > 1:
            _ = 0

        if update_only:
            for row in rows:
                pat = os.path.basename(row[0])
                job = self.que.get(pat)
                if job is None:
                    job = self.que.add(*row)
                else:
                    job.status = row[1]
                    job.path = row[0]

                # print '!!', job.label
        else:
            self.que.clear()
            for row in rows:
                self.que.add(*row)

        # print '}}'
        self.refresh_internal()

    def refresh_internal(self):
        self.quelist_selected_job = self.que.get(self.ui.list_order.currentItem())
        self.ui.list_order.clear()
        for job in self.que:

            if (job.status == COMPLETE) and (self.show_completed == False):
                continue
            job.label = '%-50s%s' % (job.short_path(), job.status)

            # print '>>', job.label

            item = QListWidgetItem(job.label)
            self.ui.list_order.addItem(item)
            if self.quelist_selected_job == job:
                self.ui.list_order.setCurrentItem(item)
                self.active_item = job
                # item.setBackground(QColor.blue)

class JobList:
    def __init__(self, parent):
        self.parent = parent
        self.list = []

    def __iter__(self):
        for x in self.list:
            yield x

    def clear(self):
        self.list = []

    def add(self, path, status=None):
        job = Job(path, status)
        self.list.append(job)
        return job

    def get(self, key):

        if key is None:
            return None

        if not type(key) == str:
            key = key.text()  # listWidgetItem
            # except:
            #     pass

        for job in self.list:
            if key in job.label:
                return job

    def reorder(self, job, pos_change=-1, absolute=False):

        if not job.__class__.__name__ == "Job":
            job = self.get(job)

        if absolute:
            if pos_change < 0:
                pos_change = len(self.list) + pos_change
            new_index = pos_change
        else:
            new_index = self.list.index(job) + pos_change
        self.list.remove(job)
        self.list.insert(new_index, job)

        self.parent.refresh_internal()

        que_order = ''
        for job in self.list:
            que_order += '%s\n' % job.path

        print que_order

        f_write('que_order_mod.csv', que_order)


class Job:
    def __init__(self, path, status=None):
        self.path = path
        self.status = status
        self.label = ''

    def short_path(self):
        return self.path.replace(slash_fix(os.getcwd()), os.path.basename(os.getcwd()))



if __name__ == "__main__":

    f_write('que.commands', '')
    i =  0
    while not os.path.isdir('./Source_Queuer'):
        i +=1
        os.chdir('../')
        if i > 5:
            raise Exception("Tried and failed to os.chdir('../') to dir containing Source_Queuer")
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('C:/Users/Joe/Dropbox/code/projects/queuer/Source_Queuer/logo.png'))
    myapp = StartQT4()
    myapp.refresh_from_file()

    # QtCore.QTimer.singleShot(0, myapp.loop_refresh)
    sys.exit(app.exec_())