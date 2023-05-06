# Python Pharma-Health Chat App 

## System-Dev-Final-Project
The problem domain of this project is healthcare and pharmaceuticals industry. In this industry, communication is lax and streamlining communication between healtcare providers and pharaceutical industry is paramount.

I am interested in using a designed technology system to improve communication and coordination in healthcare and pharmaceutical industry. I believe that a well-designed software system can play a key role in addressing this issue in both interconnected industries.

A prototype system that allows for easy and secure communication between healthcare providers and pharmaceutical companies. This system would include several easy-to-use features such as secure messaging, file sharing, and appointment scheduling is the scope of this system being developed.

However, I had to reduce the scope of the project to only reflect secure messaging between the healthcare providers and pharmaceutical companies. Developing the other features such as file sharing and appointment scheduling like I originally planned was a bit too much, I therefore decided to scale down and go with the most important aspect of the prototype, which is communication. 

This prototype app is in the form of a chatroom where users can register with a username and login information and enter a chatroom to have secure communication. If no chatroom exists, one can be created and the code can be given to other participants to join the chat room as well. I used socketio framework in Flask to execute this connection. Socketio can have up to 20 or more people in a chatroom 

All the requirements and library dependencies are in the virtual environment ".venv"

How to test the app:
-  Run "flask run" in the virtual environment
-  Register on the registration page.
-  Login with Username and password.
-  Select a name and create a room.
-  Open another tab, copy and paste the url excluding "/room"
-  This will go back to the chatroom where you have the option to create or join chatroom.
-  Select "join chatroom" and put in the code generated from the created chatroom.
-  Now two windows should be opened, and two people should be able to chat with each other. 
-  To exit, just close the chatroom window.