# DFS
A very simple implementation of a distributed file system


### Usage

To start the whole system on a local machine run

`docker-compose up --build --scale storage_server=4`

and then run 

`docker-compose run client`

to start the client container and interact with the DFS


### Communication protocols

###### Storage server startup
 - start broadcasting a udp hello message
 - wait for naming server to respond, learn it's address
 - connect to the naming server via tcp, exchange initial information
 
###### Naming server operation
- commands related to directory tree are only executed on namig server by manipulating directories in naming server's file system
- on file create/delete request from client, create files with the same name in local file system
this files will store the actual locations (storage address, filename on storage) of the files
- run daemon that manages file replicas and creates new one if insufficient
- on read/write request, respond with the actual file locations on the storage servers and let client commit changes/ pull from a random source
- on storage disconnect, mark all the entries as zombies
- on reconnect, check what files on storage are still up to date (compare hashes with the live nodes). If not, delete files and
remove corresponding entries on the naming server

### Contribution
All done by me (Vladislav Kalmykov)
