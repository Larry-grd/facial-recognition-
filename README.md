
## Usage

### Environment

Create virtual environment using Anaconda.
```
conda create -n face python=3.7
conda activate face
pip install -r requirements.txt
```

### MySQL Install

[Mac](https://dev.mysql.com/doc/mysql-osx-excerpt/5.7/en/osx-installation-pkg.html)

[Ubuntu](https://dev.mysql.com/doc/mysql-linuxunix-excerpt/5.7/en/linux-installation.html)

[Windows](https://dev.mysql.com/downloads/installer/)

You'll obtain an account and password after installation, then you should modify the `faces.py`, `faces_val.py`, `homePage.py`, `loginpage.py`, `registration.py` with the corresponding
`user` and `passwd`:
```
# create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="xxxxx", database="group15")
```

### Create Databse

1. Log in to mysql via terminal
2. create databse
```
create database group15;
use group15;
source crateDB.sql;
```

*******



## Run

### 1. Run the main program

```
python main.py
```

### 2. Register

Register a account, use 30350005 uid, other fileds can be customized.


### 3. Log-in
Use 30350005 to log in, and enjoy the program!