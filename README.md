# Timely
#### Video Demo:  <https://youtu.be/SQsnNaTVhI4>

Timely is a Flask-based application that makes creating calendar events a breeze.

Using only 1 line, Timely extracts the details for your calendar event and gives you options to save it on multiple platforms.

## Features

- Automatic Title Extraction
- Automatic Datetime Extraction
- Automatic Address Extraction
- Cross-platform Usability


## Deployment

To deploy this project run

```bash
  flask run
```


## Demo

[Video here](https://youtu.be/SQsnNaTVhI4)


## Components of Timely

**Timely is made using Flask as such it has the standard components of a typical Flask application.**

### **app.py**

This is the main python file that controls the application. It primarily uses 3 libraries flask, spacy, and datefinder.

- **Flask** is used to run the application and connect all the front end with the back end.
A decision to use only one path and determine which page is to be displayed using form buttons and their values.
This was done because using multiple paths for the different parts of the application would lead to a bad user experience since the entire use process is linked to each other.

- **Spacy** is used here for several things and is a core application component.
The title of the event is extracted using spacy, this is done by looking for named entities that are labeled as nouns or verbs.
A similar approach is used for extracting the address.

- **Datefinder** is used because it contains the means already written to extract date and time from a string.
A spacy-based approach could have been used but without spending a ton of time training a custom NLP model for that datefinder proves to be a wonderful alternative.
Datefinder's default datefinding ability surpass even Spacy's at most time and have a much better time taken.

### **search.html**

This page contains the HTML for the search page of the app.
It uses a logo that changes colors, and a form to send the text collected to the next page.
The color changing logo was not the only thing used, previously even CSS animations and GIFs were used but ultimately a simple text logo seemed to do the trick.

CSS is used to animate the logo to change colors when the mouse hovers over it.

### **main.html**

This page contains the HTML for the second page of the app.
It has a big form that displays the data extracted from the user's description.


### **final.html**

This page contains the HTML for the final page of the app.
It has multiple bootstrap cards which display the links for the generated calendar events.

### **template.html**

This file has all the required HTML for the base webpage.

Which Includes:

- Script imports for all the tools I used (mainly: bootstrap & iconify along with other features which I found along the way)
- Favicon icons which I looked up and created, making them small and still dicipherable was a challenge and thus I choose a simpler more minimalist logo
- Navigation bar using bootstrap

### **styles.css**

This file contains all the css writen for the project.

Apart from all the css graciously provided by bootstrap many things had to be manually adjusted.

The site's color scheme and design was debated for over a very long time. I spent hours changing hex codes and rgb values to make it look appealing.
A website called coolors.co was my partner in this journey. The website has a great feature where it suggests colors based on the ones you already selected.

Simple things such as transitioning the page when it loads in with a fade took a lot of time to master as well. Since I only used Python, looking up things which had to be done with javascript was a elucidative process.

I also decided to add a simple progress bar because that gave a clearer idea about the application being a multitep process.


## Author

- [@DMion5](https://github.com/DMion5)

