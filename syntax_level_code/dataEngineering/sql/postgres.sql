--install
$sudo apt-get install postgresql-client
$psql -h server.domain.org database user
psql: could not connect to server: Connection refused
	Is the server running on host "server.domain.org" (65.254.244.180) and accepting
	TCP/IP connections on port 5432?
$sudo apt-get install postgresql postgresql-contrib
$apt-cache search postgres
$sudo apt-get install pgadmin3
$sudo -u postgres psql postgres
\password postgres
$sudo -u postgres psql
postgres=#
$sudo -u postgres -i 
$psql
$exit

--
