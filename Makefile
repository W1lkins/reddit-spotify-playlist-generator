help:
	@echo 'Usage:'
	@echo '    venv|install|ltt|chill'

venv:
	virtualenv venv

install:
	./venv/bin/pip install -r requirements.txt

ltt:
	./venv/bin/python main.py --username 'wilkinsss'

chill:
	./venv/bin/python main.py --username 'wilkinsss' --playlist_name '"/r/chillmusic" Top of this week' --subreddit 'chillmusic'

