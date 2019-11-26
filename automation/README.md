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

After activating the virtualenv,
- run `aws configure`
- type in your credentials, use region 'ap-southeast-1'

For Windows user,
- run `set KEY_PAIR=<your aws keypair>`

- run `python main.py` and boto3 will use your key to create ec2 instances
