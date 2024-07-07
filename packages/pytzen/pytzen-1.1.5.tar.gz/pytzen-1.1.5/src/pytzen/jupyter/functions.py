from typing import Optional
from IPython.display import Markdown, display

def display_markdown(
        filename: Optional[str] = None,
        content: Optional[str] = None,
        language: Optional[str] = None
        ) -> None:
    """
    Displays content or the contents of a specified file as formatted 
    Markdown in a Jupyter notebook, optionally with syntax highlighting 
    for a specified language.

    Parameters:
    - filename (Optional[str]): The path to the file whose contents will 
      be displayed. Required if content is not provided.
    - content (Optional[str]): Markdown content to be displayed 
      directly. If provided, filename is ignored.
    - language (Optional[str]): The language identifier for syntax 
      highlighting (e.g., 'python', 'Dockerfile'). If None, no specific 
      syntax highlighting is applied.

    Returns:
    - None: This function does not return a value; it outputs directly 
      to the Jupyter notebook interface.

    Raises:
    - ValueError: If both filename and content are None.
    - FileNotFoundError: If the specified file does not exist or cannot 
      be opened.
    - IOError: If there are issues reading the file.

    Usage:
    - To display the contents of a Dockerfile with Dockerfile syntax 
      highlighting, use:
        display_markdown(filename="Dockerfile", language="Dockerfile")
    
    - To display provided Markdown content, use:
        display_markdown(content="# Hello World!")

    - To display the contents of a full Markdown file like README.md, 
      use:
        display_markdown(filename="README.md")
    """
    if content is None:
        if filename is None:
            raise ValueError("Either filename or content must be provided.")
        try:
            with open(filename, "r") as file:
                content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {filename} was not found.")
        except IOError as e:
            raise IOError(
                f"An error occurred while reading {filename}: {str(e)}")

    if language:
        formatted_content = f'```{language}\n{content}\n```'
    else:
        formatted_content = content

    display(Markdown(formatted_content))