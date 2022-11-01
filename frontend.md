# Frontend Development

## Overview

We will be using [Flask](https://flask.palletsprojects.com/en/1.1.x/) to create a web application. Flask is a Python web framework that allows you to create web applications.Flask will be used to create a backend for the web application. The frontend will use [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) and [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) to create the user interface. The frontend will also use [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) and [Bootstrap](https://getbootstrap.com/) to create the user interface.

The HTML will use [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) to render the HTML. Jinja is a templating language for Python.

## Wireframe

Wireframes are a visual guide that represents the skeletal framework of a website. The wireframe illustrates the page layout or structure of a site. Wireframes allow you to plan the information hierarchy of your pages, and how much space each piece of content should occupy.

Some wireframe for the web application is shown below.

![Wireframe](/images/wireframes/Login.png)
![Wireframe](/images/wireframes/Sign-up.png)
![Wireframe](/images/wireframes/VideoPage.png)
![Wireframe](/images/wireframes/VideoRecording.png)

## Jinja

### What is Jinja?

Jinja2 is a modern day templating language for Python developers. It was made after Django’s template. It is used to create HTML, XML or other markup formats that are returned to the user via an HTTP request.

### Why Jinja?

The main reason for using Jinja is for the template inheritance. This allows you to create a base template that contains the HTML that is common to all pages on the site. Then you can create child templates that extend the base template and add or override blocks in the base template.

Jinja has delimiter tags that are used to indicate that a block of code is to be evaluated and replaced with the result. The default delimiter tags are `{{` and `}}`.

Different delimiters tags.

`{% %}` - Statements
`{{ }}` - Expressions to print to the template output
`{# #}` - Comments not included in the template output

We utilize the `{% %}` tag in our HTML to inherit from the base template. We also use the `{% %}` tag to include the CSS and JavaScript files.

## JavaScript

### What is JavaScript?

JavaScript is a scripting language that allows you to implement complex features on web pages. It is a lightweight, interpreted programming language with first-class functions. JavaScript is a dynamic language and supports object-oriented programming. JavaScript is mainly used to create interactive effects within web browsers.

Where HTML and CSS are languages that give structure and style to web pages, JavaScript gives web pages interactive elements that engage a user.

### Where is React/Angular?

Javascript has many web frameworks that can be used to create web applications such as React and Angular.
We will not be using React or Angular for this project. The frontend will use HTML and CSS to create the strutcure of the page and the user interaction will be done using plain JavaScript. The reason for this is that our aim for this project was to create a minimal viable product. Also with the given time frame, we did not have enough time to learn React or Angular and then develop the web application.

Using Javascript we created fucntions what will Vaildate (not verifiy) the user input for the login and sign up pages, we did this because it will reduece the amount of requests to the backend.

## CSS and Bootstrap

## Colour Palette

- ![#3d5a80](https://via.placeholder.com/15/3d5a80/000000?text=+) `#3d5a80`
- ![#98c1d9](https://via.placeholder.com/15/98c1d9/000000?text=+) `#98c1d9`
- ![#e0fbfc](https://via.placeholder.com/15/e0fbfc/000000?text=+) `#e0fbfc`
- ![#ee6c4d](https://via.placeholder.com/15/ee6c4d/000000?text=+) `#ee6c4d`
- ![#293241](https://via.placeholder.com/15/293241/000000?text=+) `#293241`
