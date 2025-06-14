# Notice: I have created a web app that I am continuing to update and refine, which performs the same function as this script and then some, and with a more friendly user interface. See [that project's source repo](https://github.com/ioh-UwU/raffleSky).

## If you run into any issues using this script, please DM me on Bluesky! <br/> [@iohtheprotogen.art](https://iohtheprotogen.art/)

# bsky-raffle
A little script to run raffles on Bluesky posts through the API. I'm planning on hosting this as a web app with a UI on GitHub Pages eventually, but for now, here's the script! This is also partly for transparency with my own raffles.

# Setup
First, be sure you've got Python installed, as well as the `atproto` package. I used Python version 3.10.11 for this project.

Next, download the Python file and the two JSON files and stick them in some folder on your computer (or use the zip file I've put here).

# Configuration
`login.json` is where you'll put your handle (__WITHOUT__ the `@` sign) and an app password. If you don't have an app password, you can generate one at https://bsky.app/settings/app-passwords. 
When you're done, the file should look something like this (be sure to hit save):
```
{
  "handle": "handle.extension",
  "password: "xxxx-xxxx-xxxx-xxxx"
}
```

`options.json` holds the settings for the raffle itself. Change these based on what you want people to do to enter your raffle.

`"follow"` $~~~$ If the user needs to be following you&emsp;&emsp;&emsp;&emsp;&emsp;(default is `true`) <br/>
`"like"` $~~~~~~~$ If the user needs to like the post&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(default is `true`) <br/>
`"repost"` $~~~$ If the user needs to repost the post&emsp;&emsp;&ensp; &emsp;&ensp;&ensp;&ensp;&nbsp;(default is `false`) <br/>
`"comment"` $~$ If the user needs to comment on the post&emsp;&ensp;&nbsp;&ensp;&ensp;(default is `false`) <br/>
`"image"` $~~~~~$ If the comment needs to have an image in it &emsp;&nbsp;(default is `false`) <br/>
`"winners"`$~~$ The number of winners to select for the raffle&nbsp;&ensp;&nbsp;(default is `1`) <br/>

And finally, the `blacklist`. You can add handles to this list (inside the square brackets) to filter them out of all raffles you run with this script.

# Running the Script
Once that's all done, run the Python file. 
(This is easiest if you open a Command Prompt window in the folder you put everything else in and run
`python bsky_raffle_script.py`.

Assuming nothing wacky has happened, you will be prompted to paste in the link to the post you want to run the raffle on. <br/>
This can be the regular HTTPS link or an AT URI if you've got that. All will work!

Then hit enter. You should receive text that looks something like:
```
And the winners for <your handle>'s raffle are:

[list of winners, each on a new line]

Thank you everyone for participating!
```
Otherwise, if there aren't any users that meet the criteria for your raffle, the script will tell you that.

Another thing to note: a `session_string.txt` file will be created when you log in. This is an alternative login method that tries to use an existing session rather than starting a new one to reduce API calls. You should not edit this file, but nothing breaks if you delete it.

And that's it! To change the raffle settings, mess around with `options.json`.
