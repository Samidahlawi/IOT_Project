# Postgresql Instruction On ubuntu + archlinux

## Archlinux
```bash
sudo pacman -S postgresql
sudo passwd postgres # set a password for the user postgres
su - postgres
initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data' 
exit
sudo systemctl start postgresql
# check the status of postgresql server with
sudo systemctl status postgresql
```

## ubuntu 

```bash
sudo apt install postgresql
sudo passwd postgres # set a password for the user postgres
sudo systemctl start postgresql
# check the status of postgresql server with
sudo systemctl status postgresql
```


## Postgresql command

First Enter as postgres admin user with 

```bash
$ su - postgres
```

Then execute the following command for entering interactive terminal

```bash
$ psql
```

Create a database:
```bash
$ CREATE DATABASE ${databasename} ;
```

Create User:
```bash
$ CREATE USER ${username} WITH PASSWORD '${password}' ;
# or with encrypted password
$ ALTER USER <username> WITH ENCRYPTED PASSWORD '<password>';
```

Give user privilieges one of these things:
- Superuser
- Create role
- Create DB
- Replication
- Bypass RLS

```bash
ALTER USER ${username} WITH ${privilege} ;
# Example
ALTER USER berrybed WITH SUPERUSER;
```

Grant all privileges on a database to a user
```bash
$ GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
```

### SQLAlchemy 

```bash
uri :  	postgresql://user:pass@localhost:5432/dbname
```