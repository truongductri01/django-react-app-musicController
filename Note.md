# Table of Contents

1. [Set up: extensions and installations](#1-set-up)
2. [Start Django project and app: Create first app and first api view using serializer](#2-start-project)
3. [Implement React under the control of webpack and babel](#3-implement-react) <!--Add url in both Router and urls.py-->
4. [Handling POST request](#4-handling-post-request)
5. Create the React Components
6. [Send the request from Frontend component to Backend](#6-send-request-from-frontend)
7. [Calling api endpoints from the frontend](#7-call-api-endpoint-from-frontend) <!-- With the variable inside the path in Route   -->
8. [Joining the room and validate the roomCode](#8-joining-room)
9. [ComponentDidMount and Django Session](#9-django-session)
10. [Leaving the room](#10-leaving-the-room)
11. [React Default Props](#11-react-default-props)
12. [Using Spotify Api](#12-using-spotify-api)
13. [Getting Song information and pooling requests]
14. [Play and Pause Spotify]

- [Note](#note)
- [Terms](#terms)
- [Questions](#questions)

# 1. Set up

### Extensions for VS Code:

1. JavaScript (ES6) code snippets
2. Python
3. Django
4. ES7 React/Redux/GraphQL/React-Native snippets
5. npm

### Install the required tech:

1. Python
2. Django and REST framework: `pip install django djangorestframework`
3. NodeJs and npm

Get back to Table of Contents: [back](#table-of-contents)

# 2. Start project

### Create the project

1. Start a django project: <code>django-admin startproject music_controller</code>
2. Inside the new music_controller folder, start a new app (<code>django-admin startapp api</code>), called **api**
3. Go to the settings.py inside the music_controller folder, add **api.apps.ApiConfig** and **rest_framework** into the **INSTALLED_APPS** array
4. Submit the change by using the code:
   ```
   >>> cd music_controller
   >>> python .\manage.py migrates
   ```

### Create the first View

1. Go to views.py in the **api** folder and create a function which return HttpResponse("Hello")
   ```python
   def main(request):
      return HttpResponse("Hello")
   ```
2. Create urls.py file inside **api** to control folder local view url

   ```python
   from django.urls import path
   from .views import main

   urlpatterns = [
      path("", main)
   ]
   ```

3. Use include in the urls.py of the _music_controller_ folder to dispatch and guide the request to the right urls file as we desire

   ```python
   from django.urls.conf import include

   urlpattern = [
      path("api/", include("api.urls")),
   ]
   ```

4. Run the server: `python .\manage.py runserver` and go to the right url in format: [url_from_the code]/api

### Create a Model:

1. Create the class inside the models.py of the **api** folder and add all the needed fields
2. The class should inherit models.Model and the fields serve as form's inputs

   ```python
   # Create your models here.
   class Room(models.Model):
    # Describe the fields
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)  # automatically add the time when the object is created

   ```

3. Make migrations and migrate to accept the changes. Only need to do this when the models.py files changed
   ```
   >>> cd music_controller
   >>> python .\manage.py makemigrations
   >>> python .\manage.py migrate
   ```

### Create API views: return JSON file with data of all room in the database

1. Create django serializer: control of the information the server will return or accept as an api
2. Create a Create View in views.py
3. Render the View in the urls.py inside api folder

Get back to Table of Contents: [back](#table-of-contents)

# 3. Implement React

1. Start a new app: django-admin startapp frontend
2. This folder will hold all the design for the UI
3. Create the folders preparing for React integration
4. init npm: npm init -y
5. Adding the required dependencie in package.json and run npm install
6. Config babel in babel.config.json
7. Config webpack in webpack.config.json
8. Add code to package.json: "dev": "webpack --mode development --watch", "build": "webpack --mode production"

> Django will render the templates and react will control the page's behavior

9. Add a function which will search for and render the html file for the frontend in the views.py of the big frontend folder. <code>return render(request, "frontend/index.html")</code>
   > Django will look for **templates** folder to search for the right **.html** files
10. Create the url and include in the **music_controller/urls.py** file
11. Create a React component inside the frontend/src/components folder
12. Include the app inside th settings "INSTALLED_APP": "frontend.apps.FrontendConfig"

_Explanation on how React works here_: React files will be compiled by webpack into one single js file which will then be implemented inside an index.html file. The django will then execute the views.py which will search for the html templates and render out on the page

14. Create more components and add the router to both React and Djago
    We just need to simple state: <code>path("join", index)</code> without specifying the component because django will know where to go to the right url
15. Now when you run the django server, React component will be rendered automatically

Get back to Table of Contents: [back](#table-of-contents)

# 4. Handling POST Request

1. Create new serializer for the Room Creation
2. Add a CreateRoomView into the views.py of the api folder which inherits the APIView
3. The serializer will handling the rendering of the UI for posting related to api.
4. Overwrite the post function inside the new view to handle the post request

- Check if the session is already existed or not using the session key. the key serve like a unique id of the room. If the key existed mean the room is created and if there is a post request related to that then it should only be updated information
- If the session_key does not exist before, create new room

5. Issues here: the host is the same if created new room - needed to be changed

Get back to Table of Contents: [back](#table-of-contents)

# 6. Send Request From Frontend

> code is in **frontend/src/components/CreateRoomPage.js**

1. Create the React component as a form with required information
2. After getting required information, create a POST JSON object. Notice the keys inside the body that is the same as the required keys in the django serializer

```javascript
const requestOptions = {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    // The keys here need to be the same as the element names you need for the form in the backend
    votes_to_skip: this.state.votesToSkip,
    guest_can_pause: this.state.guestCanPause,
  }),
};
```

3. Create a POST request and send it to the backend url:
   ```javascript
   // Send the request to the backend and redirect to the room page with the room code
   fetch("/api/create_room", requestOptions)
     .then((response) => response.json())
     .then((data) => this.props.history.push(`/room/${data.code}`)); // go to the room with the right code without importing history
   ```

**Note**: The code will not work yet as we have not defined any url in the form of /room/:roomCode.  
 We will do it in the next section

Get back to Table of Contents: [back](#table-of-contents)

# 7. Call api endpoint from Frontend

1. Create a Room component
2. Create a Route from Homepage.js to that Component:

```javascript
// Room must be assigned to the component variable so that the code later could read the roomCode in the url
<Route path="/room/:roomCode" component={Room}></Route> // :roomCode is the url parameter
```

3. Add the right link into the urls.py file:

```python
   path("room/<str:roomCode>", index)  # <str:roomCode> is the url parameter
```

4. Get the roomCode from within the Room.js file:
   ```javascript
   // the roomCode came from the url parameter
   this.roomCode = this.props.match.params.roomCode;
   ```
5. Create a Room View in `api/views.py` which is reponsible for validating the roomCode passing in by checking whether any code is passed in or the code is valid or not

Get back to Table of Contents: [back](#table-of-contents)

# 8. Joining Room

1. Create an api endpoint for the join POST request (JoinRoom in views.py and in urls.py)
2. Pass the roomCode into the request data session (Hompage.js and frontend/urls.py)
3. Create a request in frontend

   ```javascript
   const requestOptions = {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     body: JSON.stringify({
       // The keys here need to be the same as the element names you need for the form in the backend
       votes_to_skip: this.state.votesToSkip,
       guest_can_pause: this.state.guestCanPause,
     }),
   };
   ```

4. Send the request to fetch and redirect to the right room

   ```javascript
   // Send the request to the backend and redirect to the room page with the room code
   fetch("/api/create_room", requestOptions)
     .then((response) => response.json())
     .then((data) => this.props.history.push(`/room/${data.code}`));
   ```

Get back to Table of Contents: [back](#table-of-contents)

# 9. Django Session

What are we gonna do? Control of the session of the users to send them to the room without entering any roomCode if they were in the room before closing the browser without leaving

> Browser cache will keep track of the session, so we can make use of that to create this convenience

1. Create an api endpoint to retrieve the roomCode of the session

   ```python
   class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {"code": self.request.session.get("room_code")}
        return JsonResponse(data, status=status.HTTP_200_OK)
   ```

2. Remember to add that into the urls.py inside **api** folder

   ```python
       path("user_in_room", UserInRoom.as_view())
   ```

3. Fetch the url from the frontend to access the roomCode, if there is any
   ```javascript
   fetch("/api/user_in_room")
     .then((response) => response.json())
     .then((data) => {
       console.log(data.code);
     });
   ```
4. Redirect the user to the room if the roomCode exist
   ```javascript
   <Route
     path="/"
     render={() => {
       return this.state.roomCode ? (
         <Redirect to={`/room/${this.state.roomCode}`}></Redirect>
       ) : (
         this.renderHomePage()
       );
     }}
   ></Route>
   ```

# 10. Leaving The Room

1. Create an api to delete the room information from the database (LeaveRoom in views.py and urls.py)
2. From the Frontend, send a POST request to the api endpoint
3. Also remember to clear the roomCode in the homepage as the user has left the room

Get back to Table of Contents: [back](#table-of-contents)

# 11. React Default Props

1. Using default props help you simplify the props passing down process

   ```javascript
   // These two lines will work similarly
   <CreateRoomPage />
   <CreateRoomPage testing={true}/>
   ```

2. Inside the CreateRoomPage component, you can access the testing prop
   ```javascript
   this.props.testing;
   ```
3. But it will raise an error without default props. At the top of the CreateRoomPage class, above constructor, define a static default props
   ```javascript
   static defaultProps = {testing: false}
   ```

Get back to Table of Contents: [back](#table-of-contents)

# 12. Using Spotify Api

Guide: [Spotify api](https://developer.spotify.com/documentation/general/guides/authorization-guide/)

Simple explanation:

1. Application will send a request to Spotify
2. Spotify will then ask the user to login
3. After successfully login, an access token and a refresh token will be sent to the application
4. The app can use the access token to implement the features.
5. The access token will expire after an hour, then the refresh token should be sent to Spotify to ask for a new access token

Setup Steps:

1. Go to this page and Login with a valid account: [Spotify for Developers]
   (https://developer.spotify.com/dashboard/applications)
2. Click on **Create an App**
3. Create a new app in **music_controller** folder: `python .\manage.py startapp spotify`
4. In the **spotify** app, create a credentials.py file to store the information we do not want to publish

   ```python
   CLIENT_ID = "..."
   CLIENT_SECRET = "..."
   REDIRECT_URL = ""
   ```

5. Create a function that will handle the authorization from Spotify
6. Redirect to the frontend app, remember to add app_name into urls.py of **frontend** folder

How does the code works?

1. The User create the Room
2. Then the server ask for authorization to Spotify
3. After going through Spotify authorization process, the browser will be directed to a page where the server stores the SpotifyToken.
4. After that, the code will redirect the user back into the room
   Get back to Table of Contents: [back](#table-of-contents)

### Note:

1. python .\manage.py makemigrations for everytime some things is updated (models)
   then python .\manage.py migrate
2. Notice the endpoints using in the urls files
3. Fat models, thin views: put most of the logic onto the models
4. Using rest_framwork from django to handle post and get request for api. Can even create new object
5. Notice the component prop of Material-UI component. Very convenient. Example, instead of wrapping a button inside a Link component from react-router-dom, we can:
   ```javascript
   <Button color="secondary" variant="contained" to="/" component={Link}>
     Back
   </Button>
   ```
6. Sometimes the code is updated but not the frontend as the old version is stored in the browser cache. Inspect the browser, then right click on the **Reload** symbol and choose delete cache and hard reload
7. To create an api endpoint: create a View in views.py which inherit APIView. Then overwrite the function based on the request method you want to do with the api. Then add the view to the urls.py. With the added url, we have an api endpoint
8. Choosing between POST and GET request:
   - If you only read the data from the api: GET method
   - If somehow you change the data: POST method
9. _patch_ is the method to update a database data
10. To save data in the database: create a model, then pass information to that model and then save the model to the database
11. We can use Callback function to update the page props without refreshing the page

Get back to Table of Contents: [back](#table-of-contents)

### Terms:

1. End point: location of a webserver that you want to go to: /main
2. Session: Used to controll who is the host aka. whether the user is logged in or not

Get back to Table of Contents: [back](#table-of-contents)

### Questions:

1. Why using serializer?
   > To create UI interface to show API response and form to create new Object (Room)

Get back to Table of Contents: [back](#table-of-contents)

### What is done?

1. Create a server using Django
2. Build up REST API endpoints using Django rest_framework
3. Build Frontend using React and Material-UI
4. Bundle the code using webpack and babel
5. Access music library using Spotify api

### Handle to notify people when pausing the songs

### Show the next song
