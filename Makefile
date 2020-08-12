.PHONY: tools migrate setup

setup: tools migrate

tools:
		sudo yum -y install postgresql
		cd ~/environment/; sudo wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/5.2.4/flyway-commandline-5.2.4-linux-x64.tar.gz | tar xvz && sudo ln -s `pwd`/flyway-5.2.4/flyway /usr/local/bin
		sudo python3 -m pip install -r requirements.txt

migrate:
		flyway -configFiles=flyway.conf migrate
