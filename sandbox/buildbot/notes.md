## Links:
- [Buildbot in 5mins](https://docs.buildbot.net/current/tutorial/fiveminutes.html#)

sudo yum install -y python3-pip git curl
pip3 search buildbot
sudo pip3 install buildbot
sudo pip3 install buildbot-www

Better to do this:
sudo pip3 install buildbot[bundle]



mkdir master
cd master/
buildbot create-master master
mv master/master.cfg.sample master/master.cfg

$ pwd
/home/centos/master
$ tail -f master/twistd.log 


ssh -L 8010:localhost:8010 -i ~/.ssh/dev1 centos@xx.xxx.xx.xxx


Buildbot worker:
---------------

sudo pip3 install buildbot-worker
sudo pip3 install setuptools-trial


Make config changes to master:
-----------------------------
$ vi master/master.cfg 
$ buildbot reconfig master

Install ansible:
----------------
pip3 install --user ansible
