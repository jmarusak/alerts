serve:
	uvicorn main:app --reload

deploy:
	gunicorn --bind 0.0.0.0:3000 -w 1 -k uvicorn.workers.UvicornWorker main:app
