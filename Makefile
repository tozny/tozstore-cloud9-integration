.PHONY: tools e3db-python-pre-release migrate setup

setup: e3db-python-pre-release tools migrate

tools:
		sudo yum -y install postgresql
		cd ~/environment/; sudo wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/5.2.4/flyway-commandline-5.2.4-linux-x64.tar.gz | tar xvz && sudo ln -s `pwd`/flyway-5.2.4/flyway /usr/local/bin
		sudo python3 -m pip install requirements -r requirements.txt

e3db-python-pre-release:
		cd ~/environment/; git clone https://github.com/tozny/e3db-python.git
		sudo python3 -m pip install wheel
		cd ~/environment/e3db-python/; sudo python3 setup.py bdist_wheel
		sudo python3 -m pip install --find-links=/home/ec2-user/environment/e3db-python/dist/ e3db==2.1.0

migrate:
		flyway -configFiles=flyway.conf migrate
