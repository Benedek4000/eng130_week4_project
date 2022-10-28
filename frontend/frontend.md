# Frontend Development

## Overview

We will be using [Flask](https://flask.palletsprojects.com/en/1.1.x/) to create a web application. Flask is a Python web framework that allows you to create web applications. It gives developers flexibility and is a more accessible framework for new developers since you can build a web application quickly using only a single Python file. Flask will be used to create a backend for the web application. The frontend will use [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) and [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) to create the user interface. The frontend will also use [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) and [Bootstrap](https://getbootstrap.com/) to create the user interface.

The HTML will use [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) to render the HTML. Jinja is a templating language for Python. With Jinja, you can build rich templates that power the front end of your Python web applications.

## Wireframe

So before we even start coding, we need to plan what our pages will look like. A wireframe is a schematic or blueprint that is useful for helping you, your programmers and designers think and communicate about the structure of the software or website you're building.

![wireframe](images\wireframes\StoragePage.png)

Doing this work now, before any code is written and before the visual design is finalized, will save you lots of time and adjustment work later down the line.

## Flask

So first we to need to install Flask on our machine. To do this do you must use the pip package installer. On your local host terminal run `pip install flask`.
Now that you have your programming environment set up, you’ll start using Flask.

Let's start explaining a code using Flask.

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'
```

In the first line you first import the `Flask` object from the `flask` package.

You then use it to create your Flask application instance with the name `app`.
You pass the special variable `__name__` which holds the name of the current Python module.

Once you create the `app` instance, you use it to handle incoming web requests and send responses to the user.

`@app.route("/")` is a Python decorator that Flask provides to assign URLs in our app to functions easily. It's easy to understand what is happening at first glance: the decorator is telling our `@app` that whenever a user visits our app domain at the given `.route()`, execute the `hello()` function.

## Jinja

Jinja2 works with Python 2.6.x, 2.7.x and >= 3.3. There are multiple ways of installing Jinja but we will use the pip package installer again, `pip install Jinja2`.

Now we can render our first Jinja template.

```
import jinja2
environment = jinja2.Environment()
template = environment.from_string("Hello, {{ name }}!")
template.render(name="World")
```

The core component of Jinja is the Environment() class where you can create a Jinja environment without any arguments.
Later you can change the parameters of Environment to customize your environment.
Here, you’re creating a plain environment where you load the string "Hello, {{ name }}!" as a template.

We can use the Jinja template to reduce the amount of code on our pages. Let's look at an example.
Below is our home page;

```
{% extends 'layout.html' %}

{% block content %}
    <div class="container">
        <h1>{{title}}</h1>
        <p>{{description}}</p>
    </div>
{% endblock %}
```

So you might be wondering what these blocks of code mean. To explain this we must also look at the layout page.

```
<!doctype html>
<html>

  <head>
    <title>{{title}}</title>
    <meta charset="utf-8">
    <meta name="description" content={{description}}>
    <link rel="shortcut icon" href="/favicon.ico">
  </head>

  <body>
    {% include 'navigation.html' %}
    {% block content %}{% endblock %}
  </body>

</html>
```

When a page template "extends" another, that template will contain all HTML of the extended parent. When home.html extends layout.html, we need to figure out where in layout.html our page will be mounted. Jinja handles this by declaring and matching reserved spaces in our templates named "blocks." In other words, instead of copying everything from the layout page into the the home page, we can just use `extend` to achieve the same thing.

## JavaScript

Javascript is used by programmers across the world to create dynamic and interactive web content like applications and browsers. JavaScript is so popular that it's the most used programming language in the world, used as a client-side programming language by 97.0% of all websites.

JavaScript allows developers to implement features like:

- Showing and hiding menus or information
- Adding hover effects
- Creating image galleries in a carousel format
- Zooming in or zooming out on an image
- Playing audio or video on a web page
- Adding animations
- Creating drop down and hamburger-style menus

## CSS and Bootstrap

Cascading Style Sheet(CSS) is a language used to describes how HTML elements are to be displayed on a web page or layout of HTML documents like fonts, color, margin, padding, Height, Width, Background images, etc.

```
  body {
    background-color: blue;
  }
  h1 {
    background–color: purple;
  }
```

Bootstrap is a collection of CSS classes and JavaScript function and it is used for responsive design and building responsive applications. It generally works on a grid system for creating page layout with the help of rows and columns and it supports all browsers for creating responsive websites.

To make use of Bootstap you must link the stylesheet to your pages.

```
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
```

Bootstrapping is generally easier than creating your own CSS elements as you don't have to write your code from scratch, we can use the pre-defined classes.

## Colour Palette

- ![#3d5a80](https://via.placeholder.com/15/3d5a80/000000?text=+) `#3d5a80`
- ![#98c1d9](https://via.placeholder.com/15/98c1d9/000000?text=+) `#98c1d9`
- ![#e0fbfc](https://via.placeholder.com/15/e0fbfc/000000?text=+) `#e0fbfc`
- ![#ee6c4d](https://via.placeholder.com/15/ee6c4d/000000?text=+) `#ee6c4d`
- ![#293241](https://via.placeholder.com/15/293241/000000?text=+) `#293241`
