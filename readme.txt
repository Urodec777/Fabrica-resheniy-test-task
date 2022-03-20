celery -A message_sender worker -B -l INFO
redis-server