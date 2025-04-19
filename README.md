NEED TO BE RUN UNDER OS UBUNTU
For CLI UI
- Run setup.sh
- Go to directory "logic" and run "pip install -e ." 
- Run "acktool" to test 

For Web UI
- Open a terminal to run server:
    - python3 -m venv venv
    - source venv/bin/activate
    - run "./setup.sh"
    - run "python3 server.py" in folder "logic"

- Open other terminal, Go to directory "FE" and run: npm install and npm start to have web UI
