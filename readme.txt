This repo contains test task from Фабрика Решений. 
All required libs installed in venv, use pip3 install -r req.txt after activation venv (To activate write in your shell "source venv/bin/activate" in root directory).
Commands to begin to work:
					celery -A message_sender worker -B -l INFO
					redis-server
					python3 manage.py runserver
							
					USE AFTER 'cd message_sender' COMMAND.

Also, make sure you have watched urls.py in message_sender directory. It's compulsory for navigate in API.

As for additional tasks, I've done only 6 and 9 tips. 6 it's default django bonus.
