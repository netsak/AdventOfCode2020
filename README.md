# Advent Of Code 2020

## My Philosophy
My philosophy for solving the puzzles is to use the the python (3 of cause! Do I really
have to mention this in the year 2020???) standard library only (unless I encounter
problems where I really need heavy weapons like numpy >:-).
But even then I'll stick to the most common libraries (IMHO) every decent python programmer should know.

The challenge is to anticipate the task in the second part of each day puzzle so that I can reuse most of the code I needed for the first part.

Error handling is only for the brave and for these simple one-time tasks it would be more 
obfuscation then something good.

Beside that the code should be simple to read and self-explanatory.


## Spoiler Alert
I use assertions in my code with the right answers so that in case I have to refactor for
the second puzzle the first right solution won't get destroyed.

## Usage
Actually just run the day file:
```bash
$ python3 day-01.py
```
Okay on day three I needed (wanted!) more-itertools so best use an virtual environment:
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python day-03.py
```
