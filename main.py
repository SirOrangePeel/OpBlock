from website import create_app #Grab the method from the custom "website" package. This is the folder
# from flask import redirect, url_for


app = create_app() #Create the app object

if __name__ == '__main__':
    app.run(debug=True) #If this specific python file is being run then start app in debug mode