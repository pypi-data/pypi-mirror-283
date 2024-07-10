from pathlib import Path
from os.path import basename, dirname, isfile
import subprocess
import sys
import re


# The script needs the python library "requests". If the library
# is not found, the script will be halted
try:
    import requests
except ModuleNotFoundError:
    print("'Requests' Library was not found. "
          + "Please install requests.",
          file=sys.stderr)
    sys.exit(1)


HOST = "https://smol.pub"

def load_token():
    """
    Load the token string from the file 
    located under ~/.config/.smolpub
    """
    
    config_path = Path.home() / ".config" / ".smolpub"
    if not isfile(config_path):                
        print(f"Token file not found. Please add a valid "
              + f"token string under \"{config_path}\". "
              + "To obtain a token string, please visit "
              + "https://smol.pub/settings",
              file=sys.stderr)
        raise FileNotFoundError(f"{config_path} does not exist")
    with open(config_path, "r") as f:
        token = f.read().strip()
    return token

def open_validate_article(filename):
    """
    Load an article from a file 
    and extracts its title, slug and content
    """
    
    # Load the article from the file
    try:    
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Article file \"{filename}\" not found.",
              file=sys.stderr)
        raise FileNotFoundError(f"{filename} does not exist")
    
    # Extract the title from the first line
    title = lines[0][1:].strip()

    # Extract the slug from the filename
    slug = basename(filename).lower().split(".")[0]
    full_pattern = re.compile('[^a-z0-9\\-]|_')
    slug = re.sub(full_pattern, '', slug)
    
    # Checks if the article is valid
    is_valid = False
    if len(lines) >= 2:
        if lines[0].strip()[0] == "#" and lines[1].strip() == "":
            is_valid = True
    
    # Extract the content from the remaining lines
    content = "".join(lines[2:])
                      
    # Returns the title, slug, content 
    # and if the article is valid
    return (title, slug, content, is_valid)

def upload_article(title, slug, content):
    """
    Uploads an article to smol.pub server
    """

    try:
        token = load_token()
    except FileNotFoundError:
        sys.exit(1)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    cookies = {"smolpub": token}
    payload = {"title": title, 
               "slug": slug, 
               "content": content}
    request = requests.Request("POST", f"{HOST}/posts/save", 
                               headers=headers, 
                               data=payload,
                               cookies=cookies).prepare()
    
    # Tries to send the article as a new post
    try:
        session = requests.Session()
        result = session.send(request)
    except requests.exceptions.SSLError:
        print("A SSL Error has occurred. Unable to connect to the server.",
              file=sys.stderr)
        sys.exit(1)

    if result.status_code == 500:
        # If the upload fails because the article already 
        # exists, tries to send it again as an update
        request = requests.Request("POST", 
                                   f"{HOST}/posts/{slug}/update",
                                   headers=headers, data=payload,
                                   cookies=cookies).prepare()
        session = requests.Session()
        result = session.send(request)        
    elif result.status_code == 200:
        # Otherwise, the upload was successful
        pass
    else:
        # In any other case of failure,
        # prints the status code and exits
        print(f"Unexpected error: {result.status_code}",
              file=sys.stderr)
        sys.exit(1)


def app():

    # Check that the user has provided the 
    # correct number of arguments
    if len(sys.argv) < 2:
        print(f"Usage: {basename(dirname(__file__))} <file>")
        sys.exit(1)

    # Load the article from the file and verifies its vailidity
    try:
        title, slug, content, is_valid = open_validate_article(sys.argv[1])
    except FileNotFoundError:
        sys.exit(1)

    if is_valid:    
        upload_article(title=title, slug=slug, content=content)
    else:
        print(f"\"{sys.argv[1]}\" does not contain a valid article. "
              + f"A valid article must begin with a '#' symbol "
              + f"and have an empty second line.",
              file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    app()
