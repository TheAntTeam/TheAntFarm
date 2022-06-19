
run: env qtrc qtui
	./env/bin/python3 the_ant_farm.py

# Setup the virtual environment if the requirements change.
env: requirements.txt
	python3 -m venv ./env
	./env/bin/pip3 install -r requirements.txt

# Regenerate the QT Resources if the source file changes.
qtrc: env app_resources.qrc
	./env/bin/pyside2-rcc app_resources.qrc -o app_resources_rc.py

# Regenerate the QT Python source if the ui Design changes.
qtui: env app_resources.qrc the_ant_farm.ui
	./env/bin/pyside2-uic the_ant_farm.ui > ui_the_ant_farm.py

clean:
	rm -fr __pycache__
	rm -fr app_resources_rc.py
	rm -fr ui_the_ant_farm.py

clean-env:
	rm -fr ./env

