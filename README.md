# blockchain_project
## DeepVote

# Introduction
DeepVote is an Ethereum based online voting system for faculty members. It allow faculty members of any institution to vote on any matter. With the help of blockchain, out voting system provides anonymity to the users and the votes can not be tampered once casted.

# Setup
Prerequisites:
  * Web3.py
  * Solc 0.4.24
  * Django
  * Php
  * Ganache CLI

# Running the Project
Run the ethereum blockchain network
```
sudo ganache-cli
```
For the admin server, goto admin directory and run
```
python3 manage.py
```
The admin will create a new poll from the admin page with the commit and reveal period specified.

The voters will vote by runing the php local server and select from the list of polls created.
