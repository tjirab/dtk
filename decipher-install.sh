cdcdbin/bash
INFO=1
DEBUG=1
FLD=".decipher"
CURDIR=`pwd`

# add_api function
add_api () {
echo "[ACTION] Do you already have your API token ready? (y/n)?"
unset READY
read READY
while [[ ! ${READY} =~ ^(y|n)$ ]]; do
	[[ $INFO -eq 1 ]] && echo "[ERROR]  Cannot recognise input; accepting y or n"
	read READY
done
if [ ${READY} = "n" ]; then
	echo "[INFO]  In order to get your API token, follow these instructions
	1.) go/okta
	2.) Select decipher
	3.) Click your profile on the top right
	4.) Click API access in the drop down menu
	5.) Hit 'Create new API key'
	6.) Copy this to your clipboard (CMD+C)
	7.) Paste this value in the next step"
fi
echo "[ACTION] Please enter your API token"
unset TOKEN
read -s TOKEN
while [[ ! ${#TOKEN} -eq 64 ]]; do
	echo "[ERROR] Token must be 64 characters long"
	read -s TOKEN
done
echo "[INFO]  Token accepted"
echo "APITOKEN=${TOKEN}" >> config
}

cd ~

# Checking if folder exists
[[ $INFO -eq 1 ]] && echo "[INFO]  Checking if ${FLD} exists"
if [ ! -d "${FLD}" ]; then
  [[ $INFO -eq 1 ]] && echo "[INFO]  Creating ${FLD} in ~"
  mkdir "${FLD}"
else
	[[ $INFO -eq 1 ]] && echo "[INFO]  OK"
fi

# Checking if conifg file exists
cd ${FLD}
[[ $INFO -eq 1 ]] && echo "[INFO]  Checking if config file exists"
if [ ! -f "config" ]; then
	[[ $INFO -eq 1 ]] && echo "[INFO]  Creating config file"
  touch "config"
else
	[[ $INFO -eq 1 ]] && echo "[INFO]  OK"
fi

# Checking if api-token is present
[[ $INFO -eq 1 ]] && echo "[INFO]  Checking API token presence"
if grep -q APITOKEN "config"; then
  [[ $INFO -eq 1 ]] && echo "[ACTION] An api-token was found. Do you want to update it (y/n)?"
  unset UPDATE
  read UPDATE
  while [[ ! ${UPDATE} =~ ^(y|n)$ ]]; do
  	[[ $INFO -eq 1 ]] && echo "[ERROR]  Cannot recognise input; accepting y or n"
  	read UPDATE
	done
	if [ ${UPDATE} = "y" ]; then
		sed -i '' '/^APITOKEN/d' config
		add_api
	else
		[[ $INFO -eq 1 ]] && echo "[INFO]  Not making any changes"
	fi
else
	add_api
fi

# Decipher login attempt
[[ $INFO -eq 1 ]] && echo "[INFO]  Attempt to log-in with API key"
[[ $INFO -eq 1 ]] && echo "[INFO]  Advise: use option 1 (64-character API key) which should be in your clipboard"
beacon login

# Create link
sudo ln -s "python ${CURDIR}/main.py" /usr/local/bin/dct

echo "\nDone!\n\nNow run 'dct' in terminal to activate the program\n\n"