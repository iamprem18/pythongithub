#Install Base image 
FROM python:3.7

#Make /app as working directory
WORKDIR .
ARG username=$username

RUN git clone https://github.com/$username/pythongithub.git

#Install Dependencies
RUN pip install pyOpenSSL
RUN pip install flask

#Expose to Port:5000
EXPOSE 7000

#Run the application
ENTRYPOINT [ "python" ] 
CMD [ "/pythongithub/app.py" ]