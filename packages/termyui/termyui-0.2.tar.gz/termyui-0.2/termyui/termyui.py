import curses
import pyfiglet
from termcolor import colored
import re
import os
from term_image.image import from_file, from_url
import requests
from io import BytesIO

__version__ = 0.1

class Termy:
    @staticmethod
    def head_text(text, font="slant", color="white", on_color=None, style=None):
        """Renders the given text in a specified font and color using pyfiglet and termcolor."""
        try:
            figlet = pyfiglet.Figlet(font=font)
            ascii_art = figlet.renderText(text)
            colored_art = colored(ascii_art, color=color, on_color=on_color, attrs=style)
            print(colored_art)
        except Exception as e:
            print(f"Error rendering head_text: {e}")

    @staticmethod
    def p(text, color="white", on_color=None, style=None):
        """Prints the given text in a specified color and style using termcolor."""
        try:
            colored_text = colored(text, color=color, on_color=on_color, attrs=style)
            print(colored_text)
        except Exception as e:
            print(f"Error rendering text: {e}")

    @staticmethod
    def link(url, link_text, color="blue", on_color=None, style=None):
        """Prints a hyperlink with the specified display text and URL."""
        try:
            colored_link_text = colored(link_text, color=color, on_color=on_color, attrs=style)
            print(f"\033]8;;{url}\033\\{colored_link_text}\033]8;;\033\\")
        except Exception as e:
            print(f"Error rendering link: {e}")

    @staticmethod
    def __render_markdown(text):
        """Renders markdown text with appropriate styles and colors."""
        try:
            text = re.sub(r'^(#{1}) (.*)', lambda m: colored(f'{m.group(2)}', 'red', attrs=['bold']), text, flags=re.MULTILINE)
            text = re.sub(r'^(#{2}) (.*)', lambda m: colored(f'{m.group(2)}', 'yellow', attrs=['bold']), text, flags=re.MULTILINE)
            text = re.sub(r'^(#{3}) (.*)', lambda m: colored(f'{m.group(2)}', 'green', attrs=['bold']), text, flags=re.MULTILINE)
            text = re.sub(r'^(#{4}) (.*)', lambda m: colored(f'{m.group(2)}', 'cyan', attrs=['bold']), text, flags=re.MULTILINE)
            text = re.sub(r'^(#{5}) (.*)', lambda m: colored(f'{m.group(2)}', 'blue', attrs=['bold']), text, flags=re.MULTILINE)
            text = re.sub(r'^(#{6}) (.*)', lambda m: colored(f'{m.group(2)}', 'magenta', attrs=['bold']), text, flags=re.MULTILINE)
            text = re.sub(r'\*\*(.*?)\*\*', lambda m: colored(m.group(1), attrs=['bold']), text)
            text = re.sub(r'\*(.*?)\*', lambda m: colored(m.group(1), attrs=['italic']), text)
            text = re.sub(r'^\* (.*)', lambda m: colored(f'- {m.group(1)}', 'white'), text, flags=re.MULTILINE)
            text = re.sub(r'^\d+\. (.*)', lambda m: colored(f'{m.group(0)}', 'white'), text, flags=re.MULTILINE)
            text = re.sub(r'^> (.*)', lambda m: colored(f'{m.group(0)}', 'blue', attrs=['dark']), text, flags=re.MULTILINE)

            return text
        except Exception as e:
            print(f"Error rendering markdown: {e}")
            return text

    @staticmethod
    def use_file(file_path, box_color="white"):
        """Reads a file, renders its markdown content, and prints it inside a box."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Render markdown
                rendered_content = Termy.__render_markdown(content)
                # Print content in a box with specified color
                Termy.container(rendered_content, box_color)
        except Exception as e:
            print(f"Error reading file: {e}")

    @staticmethod
    def container(content, box_color):
        """Prints the given content inside a box with a specified color."""
        try:
            lines = content.split('\n')
            max_length = max(len(line) for line in lines)
            print(f'╔{colored("═" * (max_length + 2), color=box_color)}╗')
            for line in lines:
                print(f'║ {line.ljust(max_length)} ║')
            print(f'╚{colored("═" * (max_length + 2), color=box_color)}╝')
        except Exception as e:
            print(f"Error printing box: {e}")

    @staticmethod
    def btn(label, func):
        """Displays a button with the specified label and triggers the associated function when clicked."""
        def button(stdscr):
            curses.mousemask(1)  # Enable mouse's events
            h, w = stdscr.getmaxyx()

            # Calculate position for the button - center it
            label_x = w // 2 - len(label) // 2
            label_y = h // 2

            while True:
                stdscr.clear()
                
                # Draw the button with a box around it
                stdscr.addstr(label_y - 1, label_x - 2, '-' + '-' * (len(label) + 2) + '-')
                stdscr.addstr(label_y, label_x - 2, '| ' + label + ' |')
                stdscr.addstr(label_y + 1, label_x - 2, '-' + '-' * (len(label) + 2) + '-')
                
                stdscr.refresh()
                
                key = stdscr.getch()
                
                if key == curses.KEY_MOUSE:
                    _, mx, my, _, _ = curses.getmouse()
                    if (label_x - 2 <= mx <= label_x + len(label) + 1) and (label_y - 1 <= my <= label_y + 1):
                        func()
                        break
                elif key in [10, 13]:  # Enter key
                    func()
                    break
                elif key == 27:  # ESC key
                    break

        try:
            curses.wrapper(button)
        except Exception as e:
            print(f"Error in button: {e}")

    @staticmethod
    def styled_input(prompt, color="white", on_color=None, style=None, border_color="grey"):
        """Prompts the user for input with a styled prompt message and lines above and below."""
        try:
            # Get terminal widths half legnth
            terminal_width = os.get_terminal_size().columns // 2

            # Create the styled prompt
            styled_prompt = colored(prompt, color=color, on_color=on_color, attrs=style)

            # Print top border
            print(colored("-" * terminal_width, color=border_color))

            # Print the prompt
            print(styled_prompt, end="")

            # Get user input
            user_input = input()

            # Print bottom borde
            print(colored("-" * terminal_width, color=border_color))

            return user_input
        except Exception as e:
            print(f"Error in styled_input: {e}")
            return input(prompt)

    @staticmethod
    def progress_bar(total, prefix='', suffix='', length=50, fill='█', 
                    bar_color='white', prefix_color='white', suffix_color='white',
                    bar_style=None, prefix_style=None, suffix_style=None, print_end="\r"):
        """Creates a styled progress bar that updates in the terminal."""
        def print_progress(iteration):
            percent = ("{0:.1f}").format(100 * (iteration / float(total)))
            filled_length = int(length * iteration // total)
            bar = fill * filled_length + '-' * (length - filled_length)
            
            # Apply color and style to bar, prefix, and suffix
            styled_prefix = colored(prefix, color=prefix_color, attrs=prefix_style)
            styled_suffix = colored(suffix, color=suffix_color, attrs=suffix_style)
            styled_bar = colored(bar, color=bar_color, attrs=bar_style)
            
            # Print the progress bar
            print(f'\r{styled_prefix} |{styled_bar}| {percent}% {styled_suffix}', end=print_end)
            
            # Print new line on complete
            if iteration == total:
                print()

        return print_progress
    @staticmethod
    def display_image(image_path=None, url=None):
        if image_path is None and url is None:
            raise ValueError("Please provide either an image path or a URL")

        try:
            if image_path:
                if image_path.lower().endswith((".jpg", ".jpeg", ".png")):
                    image = from_file(image_path)
                else:
                    raise ValueError("Unsupported image format. Supported formats: JPG, JPEG, PNG")
            else:
                try:
                    # Attempt to use from_url for direct URL processing (preferred)
                    image = from_url(url)
                except (AttributeError, NotImplementedError):
                    # Fallback to downloading and treating as a file
                    response = requests.get(url)
                    if response.status_code == 200:
                        image_data = BytesIO(response.content)
                        image = from_file(image_data)  # Treat downloaded data as a file
                    else:
                        raise ValueError(f"Failed to download image from URL: {url}")

            # Draw the image to the terminal
            image.draw()

        except Exception as e:
            print(f"Error displaying image: {e}")

    @staticmethod
    def menu(title, options):
        """Displays title and optons for the menu"""
        def menu(stdscr):
            # Initialize colors if supported
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            
            curses.curs_set(0)  # Hide cursor
            h, w = stdscr.getmaxyx()

            # Calculate the center position for the title
            title_x = w // 2 - len(title) // 2

            # Display title
            stdscr.addstr(1, title_x, title, curses.A_BOLD | curses.color_pair(1))
            stdscr.refresh()

            current_option = 0

            while True:
                # Display options
                for idx, (option_text, _) in enumerate(options):
                    x = w // 2 - len(option_text) // 2
                    y = h // 2 - len(options) // 2 + idx
                    if idx == current_option:
                        stdscr.addstr(y, x, option_text, curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, x, option_text)

                key = stdscr.getch()

                if key == curses.KEY_UP and current_option > 0:
                    current_option -= 1
                elif key == curses.KEY_DOWN and current_option < len(options) - 1:
                    current_option += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    # Execute the associated function
                    _, func = options[current_option]
                    if func:
                        func()
                    return current_option
                elif key == 27:  # ESC key
                    return None

        try:
            return curses.wrapper(menu)
        except Exception as e:
            print(f"Error in dropdown menu: {e}")

    @staticmethod
    def table(headers, data, header_color="cyan", row_color="white"):
        """Prints a table with headers and data."""
        try:
            # Calculate maximum width for each column
            col_widths = [max(len(str(item)) for item in column) for column in zip(headers, *data)]

            # Print header row
            Termy.__print_table_row(headers, col_widths, header_color)

            # Print data rows
            for row in data:
                Termy.__print_table_row(row, col_widths, row_color)

        except Exception as e:
            print(f"Error printing table: {e}")

    @staticmethod
    def __print_table_row(row_data, col_widths, color):
        """Prints a single row of the table."""
        row_str = " │ ".join(f"{item}".ljust(width) for item, width in zip(row_data, col_widths))
        print(colored(f"│ {row_str} │", color))

if __name__ == "__main__":
    ter = Termy()

    def interactive():
        ter.head_text("Interactive Widgets")
        ter.p("The following are the widgets that are interactive")

        ter.p("Links - ", style=["bold"], color="red")
        ter.p("-> Use Termy.link('www.example.com', 'click me') for generating a clickable link.\n")

        ter.p("Buttons - ", style=["bold"], color="blue")
        ter.p("-> Use Termy.btn('click me', example_function())\n")

        ter.p("Menu - ", color="green", style=["bold"])
        ter.p("-> You can find the example for this at - ")
        ter.link("Fillmelater.com", "Here\n")

        ter.p("Styled Input - ", color="yellow", style=["bold"])
        ter.p("-> Use styled_input('Write something>>> ')")
        


    def text():
        ter.head_text("Text Widgets")
        ter.p("The following are the text widgets")

        ter.p("Links - ", style=["bold"], color="red")
        ter.p("-> Use Termy.link('www.example.com', 'click me') for generating a clickable link.\n")

        ter.p("Buttons - ", style=["bold"], color="blue")
        ter.p("-> Use Termy.btn('click me', example_function())\n")

        ter.p("Menu - ", color="green", style=["bold"])
        ter.p("-> You can find the example for this at - ")
        ter.link("Fillmelater.com", "Here\n")

        ter.p("Styled Input - ", color="yellow", style=["bold"])
        ter.p("-> Use styled_input('Write something>>> ')")

    options = [("Interactive Widgets", interactive), ("Text Widgets", text)]
    ter.menu("TermyUI", options)