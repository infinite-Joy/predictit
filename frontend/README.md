This is the frontend part compatible with heroku

frontend: this renders the output from the companies.txt and uses flask framework

clock: this is the scheduler and depends on the APScheduler library

Procfile: this tells heroku what processes are there. this is needed by heroku to run the processes

requirements.txt: this tells the dependencies

companies.txt: this is the shared resource between the clock and frontend. <name should be changed>

