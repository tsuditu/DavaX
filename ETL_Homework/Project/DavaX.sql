-- Creeaza schema Source
CREATE USER Source IDENTIFIED BY Source_123;
GRANT CONNECT, RESOURCE TO Source;
ALTER USER Source DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;

-- Creeaza schema Target
CREATE USER Target IDENTIFIED BY Target_123;
GRANT CONNECT, RESOURCE TO Target;
ALTER USER Target DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;

-- Creeaza un user "admin" - util daca ai nevoie sa accesezi rapid orice schema dintr-un singur cont
CREATE USER admin IDENTIFIED BY admin_123;
GRANT DBA TO admin;

-- Acorda toate privilegiile catre utilizatorii Source si Target (folosit in testare sau dev local)
GRANT ALL PRIVILEGES TO Source, Target;