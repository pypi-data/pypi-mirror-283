# Command-line tool for uploading your articles to smol.pub

**This is a command-line tool written in python that will allow you to upload your articles to <https://smol.pub> 
directly from your computer terminal.** This tool has been created as an alternative to the existing official bash script 
created by smol.pub and available at <https://smol.pub/cli>.

For further information about smol.pub, please visit <https://smol.pub/manual>

## How to install this utility

1. Open your terminal 
2. Clone this repository or download a copy of it
3. Change directory to the repository directory
4. Use the command `pip install .` to install it

*Example:*
```sh
/home/example $ git clone https://github.com/fmaida/smolpub
/home/example $ cd smolpub
/home/example/smolpub $ pip install .
```

## How to invoke this tool from the command line

In your terminal, from any folder you can enter the command:

```sh
$ smolpub <article-to-upload>
```

Where `<article-to-upload>` is a valid path to a text file on your computer.

*Example:*
```sh
$ printf "# This is a test article\n\nHello world, this is the body" > article.gmi
$ smolpub article.gmi
```

The tool will extract this data from your text file:

1. **Article title.** Will be extracted from the very first line in your text file.
2. **Article slug.** Will be extracted from your text file name, file extension excluded.
3. **Article body.** Will be extracted starting from the third line on in your text file.

If the provided text file exists and has a valid structure (see below), the article contained 
in the text file will be uploaded to <https://smol.pub> as a new article or (if an article 
with the same slug already exists) will replace the previous article with the same slug.

## Requirements

### Smol.pub Token 

In order to upload the articles to https://smol.pub you will have to provide a valid token string. 
The token string must be placed in a text file under `~/.config/.smolpub`. If you need to obtain 
your personal token string, please visit the url <https://smol.pub/settings> from your browser.

### A valid article structure

In order for the tool to recognize the title and the body of your article, you will have to structure your 
text file by entering a '#' character as the first character on the first line of your file, then an empty 
string as the second line of your file. Any line following the first two will be considered part of your 
article body.

*Example:*
```
# This is the title of the article

Hello world. This is the body of the article, from this line I can write
anything. Et harum quidem rerum facilis est et expedita distinctio. Nam
libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit,
quo minus id, quod maxime placeat, facere possimus, omnis voluptas
assumenda est, omnis dolor repellendus.
```

## Known limitations

At the moment, this tool does not support the upload of images or other media files.
