# DeepVote
Anonymous faculty voting system developed by:

|       Name       | Roll No |        Email        |
|:----------------:|:-------:|:-------------------:|
|  Chaman Agrawal  |  160205 | chamanag@iitk.ac.in |
| Lakshay Bandlish |  160360 | lakshayb@iitk.ac.in |
|  Raghukul Raman  |  160538 | raghukul@iitk.ac.in |
|   Yash Mahajan   |  160822 | ymahajan@iitk.ac.in |
|  Yasharth Bajpai |  170822 |   yashb@iitk.ac.in  |

# Introduction
DeepVote is an Ethereum based online voting system for faculty members. It allow faculty members of any institution to vote on any matter. With the help of blockchain, out voting system provides anonymity to the users and the votes can not be tampered once casted.

# Description

## Admin
The admin can take the public keys of all the faculty through the faculty e-mail. The admin can create an poll with the choices he wants and can select the end of poll date which is time till which one can vote. The admin will then go to poll page and publish the ethereum contract.
## Voter
The voter can generate a key pair and can send it to admin while registering though e-mail . The voter will click on the fetch link to get all the current polls available. He will then go to poll page select an option and can vote till the end of the voting period. After that the voter must click on the reveal button on the pole to get his vote counted before the end of the voting period.
## Results
The final results will be viewable on the admin webpage.

# How it works

## Preserving Anonymity
The **Two Stage Commit-Reveal Voting** & **Linkable One Time Ring Signature**  logics used in our app takes care of keeping the voter anonymous even in a closed voting group. The admin contract needs to verify if the voter is a valid one i.e. In the list of eligible voters & has not voted before,which is accomplished by the Linkable-OTRS. Thereafter,the TSCRV aids in making the vote hash/vote verifiable on the blockchain without giving a hint away about the users identity.

## Verifying Correct Voting
The voter can use his transaction id to access the hash of his committed vote and a randomly generated nonce on the blockchain which is as well saved as a local copy on the disk.The user can hash his vote and nonce manually and compare it with one uploaded on the blockchain to ensure the integrity of the poll.

## Keeping Private Information Secure/Taking Impersonation out of Question
Assuming that the voter's device is password protected, the architecture of the app ensures that user's private information doesn't go out from his device i.e. private key,vote,nonce etc. are saved on voter's PC and all manipulation using them are done locally.


# Setup
Prerequisites:
  * Web3.py
  * Solc 0.4.24 (Install from binaries)
  * Django
  * Php
  * Ganache CLI
  * python3 
  * python3 modules- hashlib,pysha3,pickle

# Running the Project
Run the ethereum blockchain network
```
sudo ganache-cli
```
For the admin server, goto admin directory and run
```
python3 manage.py runserver
```
The admin will create a new poll from the admin page with the commit and reveal period specified.

The voters will vote by runing the php local server in the local directory.
```
php -S localhost:8080
```
