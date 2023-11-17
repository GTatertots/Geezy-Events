

clean_db:
	cd db && rm events.db
	cd db && python3 create_db.py