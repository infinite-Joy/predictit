This is the frontend part compatible with heroku

frontend: this renders the output from the companies.txt and uses flask framework
          apart from that spawns a background process for the background process

background_task.py: this one does the actual background work

Procfile: this tells heroku what processes are there. this is needed by heroku to run the processes

requirements.txt: this tells the dependencies

companies.txt: this is the shared resource between the clock and frontend. <name should be changed>

