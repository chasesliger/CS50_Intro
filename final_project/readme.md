My project is "a web-based application using JavaScript, Python, and SQL, based in part on the web track’s distribution code" as per the example ideas given by CS50's final project page.
More specifially, I have designed an application using Flask as the main framework that allows a user view a list of all the national parks of the state that they have selected, then
with the click of a button bring up a page displaying the current weather at the park. CS50's IDE was used as the development environment.

As stated above, Flask is the microframework used to implement this web application. Two API's are also used: Open Weather and the National Park Services Developer's API. Based on the
user's selected state, we send an GET request to the NPS website that returns all the national parks in that state. These are then formatted and displayed on the user's homepage.
Next to each state is a button, that when clicked does a GET request to Open Weather that returns the current weather for the park based on the latitude and longitude (the park's
visitor center's geographic location is used, since parks can be very large).

Users can register by entering there name, password, and state. They can change the selected state via a button on the nav bar. They can also change their passord if needed. Ideas
for future implementations include allowing users to save parks in a list of favorites, get weather for multiple parks at a time, and subscribe some sort of forecasting system or
receive alerts when the weather will be particularly nice on a given day.