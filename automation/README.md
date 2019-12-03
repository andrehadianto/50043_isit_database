### Initialization

#### Install awscli and boto3 in python env

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

- run `python main.py <access key> <secret access key> <key pair> <absolute path of .pem file>` and boto3 will use your key to create ec2 instances
