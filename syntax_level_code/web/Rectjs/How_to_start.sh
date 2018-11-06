#install nodejs and npm 
sudo apt-get update
sudo apt-get install nodejs
sudo apt-get install npm

#To create a react project package
npm install create-react-app -g //g for globally accessable

#Create a react project
create-react-app <name of the project>

*******************************************************************************
#Change directory into project folder
cd <project>

#Starts the development server.
npm start

#Bundles the app into static files for production.
npm run build

#Starts the test runner.
npm test

#Removes this tool and copies build dependencies, configuration files
#and scripts into the app directory.
npm run eject
*********************************************************************************
#Radium is used for inline style with sudo selector with media query.
npm install --save radium
