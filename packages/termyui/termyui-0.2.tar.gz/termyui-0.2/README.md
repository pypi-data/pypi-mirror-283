```
   __
  / /____  _________ ___  __  __
 / __/ _ \/ ___/ __ `__ \/ / / /
/ /_/  __/ /  / / / / / / /_/ / 
\__/\___/_/  /_/ /_/ /_/\__, /a  
                       /____/ 
Version 0.1                      
```

### TermyUI is for creating a simple and attractive UI for the terminal, ranging from clickable links to simple buttons, termyUI has it all!

[Visit PyPI page](https://pypi.org/project/termyUI/)

### About TermyUI -

TermyUI is built upon various libraries such as -
os, term-color, re, curses, pyfiglet, term_image, requests, io, etc.

TermyUI provide customizable widgets for the terminal such as - 
1. buttons, 
2. links, 
3. dropdowns, 
4. image displaying, 
5. tables, 
6. dropdowns
7. Text Customizablitity
and much more!

### Installing TermyUI

1. Open up your terminal and type - 

```pip install termyUI```

This command installs the termyUI module.

### Usage

A simple example - 
```
# example.py

from termy import Termy

def example_function():
    Termy.p("Button clicked!", color="green", style=["bold"])

def interactive_widgets():
    Termy.head_text("Interactive Widgets")
    Termy.p("The following are the widgets that are interactive:")

    Termy.p("Links - ", style=["bold"], color="red")
    Termy.p("Use Termy.link('www.example.com', 'Click me') for generating a clickable link.")
    Termy.link("https://www.example.com", "Click me")

    Termy.p("Buttons - ", style=["bold"], color="blue")
    Termy.p("Use Termy.btn('Click me', example_function) for creating a button.")
    Termy.btn("Click me", example_function)

    Termy.p("Menu - ", color="green", style=["bold"])
    Termy.p("You can find the example for this at -")
    Termy.link("https://example.com", "Here")

    Termy.p("Styled Input - ", color="yellow", style=["bold"])
    Termy.p("Use Termy.styled_input('Write something>>> ')")
    user_input = Termy.styled_input("Write something>>> ")
    Termy.p(f"You wrote: {user_input}", color="cyan")

def text_widgets():
    Termy.head_text("Text Widgets")
    Termy.p("The following are the text widgets:")

    Termy.p("Styled Text - ", style=["bold"], color="magenta")
    Termy.p("This is an example of styled text.", color="yellow", style=["underline"])

    Termy.p("Container - ", style=["bold"], color="cyan")
    Termy.container("This text is inside a container with a cyan border.", box_color="cyan")

def main_menu():
    options = [
        ("Interactive Widgets", interactive_widgets),
        ("Text Widgets", text_widgets)
    ]
    Termy.menu("TermyUI", options)

if __name__ == "__main__":
    main_menu()


```