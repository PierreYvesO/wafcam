# WAFCAM

## Deploy your local Application (Build v3) on Windows 10

1. Install WAMP Server
2. Install dependencies

### Setup Local Server (Wamp Server on Windows 10)
> https://sourceforge.net/projects/wampserver/files/WampServer%203/WampServer%203.0.0/ - Version : 3.2.3

Installation guide :
- Choose your language
- Choose the folder destination for WAMP
- Install the default configuration
    - PHP 7.3.21
    - MySQL 5.7.31
    - PhpMyAdmin 5.0.2
- Choose your default IDE and browser

### Setup Required Dependencies
To be able to run our Application on your local environment, you must install some dependencies :

- Install NodeJS and NPM - [guide here](#web-app-environment)
- Install Python  - [guide here](#python)

### Run Web Application
Running guide :
- Go on the official latest build of WafCam, [here build v3](https://github.com/PierreYvesO/wafcam/tree/build-v3)
- Clone it into your local server directory (usually at /www)
- Open new terminal from your operating system and go to the directory
```
cd C:\wamp64\www\
```
- Install dependencies/updates from NodeJS and NPM
```
npm install
```
- Start the application
```
npm start
```
- After that your application is running, you must enable access to Web Local API. Go on the following directory
```
cd C:\wamp64\www\wafcam\web\
```
- And run the following command
```
node src/routes.js
``` 
You are now able to check your working application on your computer (default port is 3000)

### Run Image Processing
Running guide : [guide here](#python)

## Development Setup

1. Install Web App Environment
2. Create your local database
3. Install Python Environment
4. Setup your GPU (optional)

### Web App Environment
Install NodeJS and NPM 
> https://nodejs.org/en/download/

Check your version of NodeJS and NPM :
```
node -v
```
> nodeJS project version : 14.16.0
```
npm -v
```
> npm project version : 6.14.11

Change the folder directory
```
cd wafcam/web
```

Install/update your dependencies
```
npm install
```

Now you can start the application and see the URL where your app is running (http://localhost:3000 for example)
```
npm start
```

(Optional: if you need to build your project from React App) 
```
npm run build
```

#### Add Web App Build To Local Server
Deployment guide :
- On Github website, choice your build version on branches (e.j build-v1)
- Get the link and clone it on your "/www" local repository

> Optional : if you want to make your own build, [check it out](#web-app-environment)

### Database (with PhpMyAdmin)
Install [WampServer v3.2.3](#setup-local-server-wamp-server-on-windows-10)

Go to "PhpMyAdmin" interface with this URL : http://localhost/phpmyadmin/ (default path)

Connect to the website with your logs !
> default username : root
> default password : (none)

If you don't have an already existing database, please create one and name it :
```
2z2tz_patcam_test 
```

Otherwise, delete it and create it again with the exaclty same name !

After these steps, click on "Import" button.

Put the file "2z2tz_patcam_test.sql". You should find it here :
```
repository_git : database/HERE
```

Then "Execute" and your database is ready to be used.

### Python
using python 3.8
Setup python environnement (https://docs.python.org/3/library/venv.html)
```
pip install -r requirements.txt
```
In case you want to add a new module to the project make sure to update the requirements
```
pip freeze < requirements.txt
```
Launch the python back-end
```
cd 'F:\Path\to\wafcam'
$env:PYTHONPATH = 'F:\Path\to\wafcam'
venv\Scripts\activate
.\python_back\launchWAFCAM.py
```

### Unused/Optional Setup
<details><summary>GPU Config</summary>

(Not used at the moment but it could be possible to use GPU to detect objects)
Tensorflow config : 
- Update Nvidia drivers tested with 460.x versions
- Download CUDA 11.2 [here](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exelocal)
- Download cuDNN 8.1.1 [here](https://developer.nvidia.com/rdp/cudnn-download) unzip and add <DIR>/cuda/bin to you path
- test with 
    ```
  python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
    ```

</details>
