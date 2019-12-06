### Initialization

#### Install awscli and boto3 in python env
- create python environment and install requirements

For Windows User
- run command prompt
- type `pip install virtualenv`

Creating a virtualenv
- type `virtualenv env`

To activate the isolated virtualenv  
If you are using powershell or powershell-based VSCode terminal
- go to server folder
- run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once
- run `.\\env\Scripts\activate`

If you are using command prompt
- run `.\\env\Scripts\activate`

Installing Python Dependencies
- run `pip install -r requirements.txt`

#### Running the script

- run `python main.py <access key> <secret access key> <key pair> <absolute path of .pem file> <number of nodes>` and boto3 will use your key to create ec2 instances
- run `python clean.py` to terminate instances and clean up
