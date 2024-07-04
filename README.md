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

Examples of how the visualization will look - 
<img width="1029" alt="Screenshot 2024-07-04 at 1 01 26 PM" src="https://github.com/arpitadash/codevisualization/assets/22210816/56603c14-87c3-4cd6-a5c4-6dd414e6862f">
<img width="1029" alt="Screenshot 2024-07-04 at 1 01 39 PM" src="https://github.com/arpitadash/codevisualization/assets/22210816/ce7dce25-4402-4e21-a3a0-9011acbd4dc8">
