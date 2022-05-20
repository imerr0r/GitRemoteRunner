import git
import time
import paramiko


class Pusher(git.Repo):
    def __init__(self):
        '''Initialize local path to GH repo '''
        self.localpath = "."
        super().__init__(self.localpath)

    def Commit(self):
        '''Add all changes and commit them to GH'''
        print("[+] Trying to add a commit")
        self.git.add(all=True)
        if len(self.git.diff(self.head.commit.tree)) > 0:
            self.index.commit('PusherCommit {}'.format(int(time.time())))
            print("[+] Committed")
        else:
            print("[!] Nothing to commit")

    def Push(self):
        '''Push changes to GH'''
        origin = self.remote(name='origin')
        origin.push()
        print("[+] Pushed")


class SSHer():
    def __init__(self):
        '''Initialize remote host credentials and path to run '''
        self.host = "10.10.10.222"
        self.user = "root"
        self.password = "roottoor123"
        self.remote_path = "/home/user/repo"
        self.remote_file = "main.py"

    def OpenSSH(self):
        '''Set up SSH connection to remote host'''
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.user, password=self.password)
        self.transport = self.ssh.get_transport()
        self.session = self.transport.open_session()
        self.session.set_combine_stderr(True)
        self.session.get_pty()
        print('[+] SSH connection opened ')

    def RemotePullAndRun(self):
        '''Kill running program and run a new one at remote host'''
        kill_running = " | ".join([
            'ps -ax',
            'grep python',
            'grep -v "/usr/bin/python3 /usr"',
            'grep -v grep',
            'awk -F" " \'system("sudo kill "$1"")\';',
        ])

        run_new = "; ".join([
            "cd {}".format(self.remote_path),
            "git pull",
            "chmod 755 ./{}".format(self.remote_file),
            "sudo -k python3 ./{};".format(self.remote_file)
        ])

        print('[+] Git-pulling and running program.')
        self.session.exec_command(kill_running + run_new)
        self.stdin = self.session.makefile('wb', -1)
        self.stdout = self.session.makefile('rb', -1)
        self.stdin.write(self.password + '\n')
        self.stdin.flush()
        print('[+] Running program.\n\n')

    def RemoteRead(self):
        '''Read remote stdout and print to local console'''
        while True:
            received = self.stdout.readline().decode()
            print(received, end='')

            if self.stdout.channel.exit_status_ready():
                break
        print('[+] Program ends.')


pusher = Pusher()
pusher.Commit()
pusher.Push()

ssher = SSHer()
ssher.OpenSSH()
ssher.RemotePullAndRun()
ssher.RemoteRead()

