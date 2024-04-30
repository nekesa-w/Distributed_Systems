# Distributed_Systems
## Implementing a customizable Load Balancer
  
## Coding Environment

* Programming Language: python
* Operationg System: Ubuntu 20.04 LTS or above 
* Docker: Version 20.10.23 or above 

## Task Description
### 1. SERVER
### 2. CONSISTENT HASHING
### 3. LOAD BALANCER
In this task three files were created:
1. loadbalancer.py
2. Dockerfile - it was updated so as to containerize the load balancer
3. Makefile - to deploy the whole stack in the Ubuntu environment

The values created in the consistent_hash_map.py, were used in the loadbalancer.py.
**Primary task of the loadbalancer** 
1. to route the client requests to one of the server replicas so that the overall load is equally distributed across the available replicas
### 4. ANALYSIS
