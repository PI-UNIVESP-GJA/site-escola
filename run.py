from app import app
# ---> comando para instalar requeriments ---> . venv/bin/pip install -r requeriments.txt/ venv\Scripts\pip install -r requeriments.txt
# ---> comando para iniciar o ambiente ---> . venv/bin/activate / venv\Scripts\activate
# ---> comando para iniciar o projeto ---> export FLASK_APP=run / set FLASK_APP=run
# ---> comando para buildar o projeto ---> flask run  / venv\Scripts\python run.py

#if __name__=="__main__":
    #manager.run()
if __name__=="__main__":
    app.run(debug = True)
