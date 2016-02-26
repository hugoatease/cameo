FROM python:2.7-onbuild
RUN pip install gunicorn
EXPOSE 8000
CMD ["gunicorn", "cameo:app", "-k gevent", "-w 2", "-b 0.0.0.0:8000"]
