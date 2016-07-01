import os

def get_login_user():
	# cmd = ['who|grep','tty|awk',"{'print'","$1'}"]
	# process = subprocess.Popen(cmd, bufsize=-1, stdout=subprocess.PIPE)
	# return process.stdout.readline()
	home = os.getenv('HOME')
	user = os.path.basename(home)
	return user

#ls -R /media/reisy/databank | awk '/:$/&&f{s=$0;f=0} /:$/&&!f{sub(/:$/,"");s=$0;f=1;next} NF&&f{ print s"/"$0 }'
