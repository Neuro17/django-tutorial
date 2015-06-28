## **MVC in Django**

Ci sono un elevato numero di funzioni che possono essere usate per facilitare e modularizzare compiti “standard”.
 - interazione con db
 - autenticazione
 -etc
 
Gle elementi MVVC sono gestiti in 3 file separati:

- `models.py`   -> i modelli
- `views.py`    -> le viste
- `urls.py`     -> i controller

### **Model**

Il componente Model dell'applicazione è implementato direttamente come collezione di classi Python, che poi andranno 
a rappresentare le tabelle del database. Il codice SQL per creare lo schema viene generato automaticamente da Django
quando si esegue il deployment del modello.

Si crea un n 'virtual object database' accessibile e usabile direttamente attraverso linguaggio di programmazione ad oggetti.

### **View**

Si usano template per generare diversi tipi di output, e accesso ai dati del model attraverso API Python.

### **Controller**
il file `urls.py` serve per mappare gli URL richiesti sulle view che restituiscono le pagine richieste. Si possono usare
funzioni built-in e espressioni regolari per mappare gli URL richiesti.


### **Filosofia di progetto**
Favorire lo sviluppo rapido dell'applicazione, scrivendo meno codice senza ripeterlo, e interagendo con il DB principalmente
con codice SQL autogenerato.


#### **API per il DB**
Limitare al massimo le interazioni con il DB. I dati sono accessibii da ogni modulo e i join vengono creati automaticamente
dallo strato di interfacciamento software. Rimane possibile scrivere direttamente codice SQL, ma solo quando è veramente
necessario.


#### **URL nel controller**
URL puliti e riutilizzabili: evitare le estensioni negli URL.


#### **Utilizzo di template per le view**
Lo scopo è separare la logica dalla presentazione. Si evita la ridondanza, si è più protetti contro codice malevolo e si
facilita l'estendibilità per il futuro.

#### **View**
Nessun bisogno di creare nuove classi, sono essenzialmente realizzate attraverso delle funzioni Python. Si usano oggetti 
che incapsulano le richieste HTTP.

### **Struttura di un progetto Django**
 
 mysite (dir top-level)
 |_ manage.py
 |_ mysite (package Python)
 |  |_ __init__.py 
 |  |_ settings.py
 |  |_ urls.py
 |_ app1 (package Python)
    |_ __init__.py
    |_ models.py
    |_ vies.py
    |_ ...
    
Un singolo progetto Django può essere spezzato in diverse sotto-applicazioni (ognuna sarà un package separato, come `app1`),
che avrà tutti i suoi componenti MVC (model, views, urls). Applicazioni diverse possono interagire importado i package.

- `manage.py`
script per automatizzare le operazioni di Django.

- `mysite/mysite`
cartella della applicazione principale (omonima )del progetto

- `settings.py`
impostazioni per il funzionamento dell'applicazione, tra cui: definizione dei path dell'applicazione e configurazione di 
accesso a DB

- `urls.py`
 configurazione degli URL per il progetto (livello root).   
   
## **Tutorial base**
Creo il progetto direttamente da pycharm, oppure con il comando:

    django-admin.py startproject mysite
    
Per usare MySQL devo prima creare il DB:

    $ mysql --user=root -p
    mysql> CREATE DATABASE djangodb;
    mysql> CREATE USER 'djangouser'@'localhost' IDENTIFIED BY 'rue1iep5';
    mysql> GRANT ALL PRIVILEGES ON djangodb.* TO 'djangouser'@'localhost' WITH GRANT OPTION; 
    mysql> show databases;
 
Devo aggiungere la connessione al DB creato nel file `settings.py`

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'djangodb',
            'USER': 'djangouser',
            'PASSWORD': 'rue1iep5',
            'HOST': '',
            'PORT': '',
        }
    }
    
Per PostgreSQL:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'djangodb',
            'USER': 'djangouser',
            'PASSWORD': 'rue1iep5',
            'HOST': '',
            'PORT': '',
        }
    }
    
All'interno del progetto creo una nuova app

    $ python manage.py startapp polls
    
Creo i modelli all'interno di `polls/models.py`

    from django.db import models
    
    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        
        def __unicode__(self):
            return self.question_text

          def was_published_recently(self):
            return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    
    class Choice(models.Model):
        question = models.ForeignKey(Question)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)
        
        def __unicode__(self):
            return self.choice_text
        
Aggiungo l'app alla lista delle app disponibili in `mysite/settings.py`

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'polls',
    )

Ora tutto è pronto per sfruttare le comodità di django:

- sincronizziamo il DB

    $ python manage.py makemigrations polls

- creiamo le tabelle
    
    $ python manage.py migrate

- SQL generato (mostra il codice SQL generato)

    $ python manage.py sqlmigrate polls 0001

- Controllo

    $ python manage.py check

- Python shell 
    
    $ python manage.py shell
    
Le migrazioni sono uno strumento estremamente potente che permette modifiche in corso d'opera senza perdere i dati già 
inseriti. I passaggi per applicare le modifiche consistono in:

- modificare il modello
- lanciare `python manage.py makemigrations`
- lanciare `python manage.py migrate`
    
A questo punto il model mette a disposizione una serie di metodi e utility per interrogare il DB, ad esempio

Statement | descrizione
-----------------------
 q = Question(question_text="What's new?", pub_date=timezone.now()) |   crea un nuovo oggetto Question
 q.save()                                                           |   salva sul DB (sincronizzazione esplicita)
Question.objects.all()  |   select di tutti gli elementi della tabella Question (se non è definito __unicode__ da una 
rappresentazione inutile,come quando non si fa l'override di toString() in JAVA)

    
    

    




