# codevisualization
To visualize react code repo based on imports
# Requirements 
You will need python3 installed
To install the necessary imports:
pip3 install networkx
pip3 install pyvis

# Running the file
1. Paste this file in the parent component where your web and native repos have been cloned into
2. run the command 'python3 create_component.py'
3. Answer the following questions:
 'What is the app you are interested in?' - the app name as stored in the code repo eg.: appName
  'Interactions within which folder?' - which folder within the app you are interested in. eg.: components
   'Any other interactions you want to visualize?(y/n)' - if you want to visualize the secondary interactions of the files in the previously selected folder with files from another folder
    'What is the interaction folder name?' - the absolute path of the folder: eg.:src/widgets
4. After the file is successfully run, a file called nx_appName.html will be created. Open that on chrome.

