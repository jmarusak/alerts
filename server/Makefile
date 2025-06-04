serve:
	uvicorn main:app --reload

deploy:
	gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app
