# bsky-raffle
A little script to run raffles on Bluesky posts through the API. I'm planning on hosting this as a web-app with a UI on GitHub Pages eventually, but for now, here's the script! This is also partly for transparency with my own raffles.

# Setup
First, be sure you've got Python installed, as well as the `atproto` package. I used Python version 3.10.11 for this project.

Next, download the python file and the two json files and stick them in some folder on your computer (or use the zip file I've put in here also).

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

`"follow"` If the user needs to be following you (default is `true`) <br/>
`"like"` If the user needs to like the post (default is `true`) <br/>
`"repost"` If the user needs to repost the post (default is `false`) <br/>
`"comment"` If the user needs to comment on the post (default is `false`) <br/>
`"image"` If the comment needs to have an image in it (default is `false`) <br/>
`"winners"` The number of winners to select for the raffle (default is `1`) <br/>

And finally, the `blacklist`. You can add handles to this list (inside the square brackets) to filter them out of all raffles you run with this script.

# Running the Script
Once that's all done, run the python file. 
(This is easiest if you open a Command Prompt window in the folder you put everything else in and run
`python.exe bsky_raffle_script.py`.

Assuming nothing wacky has happened, you will be prompted to paste in the embed code for your raffle post. <br/>
The script extracts the `at://` uri that the API needs to retrieve the post. There's probably a better way to get this, but this is the easiest route I found. <br/>

This code can be found by clicking the three dots on your post and then the "Embed post" option. Then triple-click the text field and hit `Ctrl + C` to copy it __as one line.__ (Pressing "Copy code" will copy it as multiple lines, which breaks the script.)

![image](https://github.com/user-attachments/assets/4675b982-100f-41c2-9bb1-21afa196d38d)
![image](https://github.com/user-attachments/assets/bbce4d4f-f92d-44ce-b9f4-221832d057e1)

Paste this into the text field as one line and hit enter. You should recieve text that looks soemthing like:
```
And the winners for <your handle>'s raffle are:

[list of winners, each on a new line]

Thank you everyone for participating!
```
Another thing to note: a `session_string.txt` file will be created when you log in. This is an alternative login method that tries to to use an existing session rather than starting a new one to reduce API calls. You should not edit this file, and nothing breaks if you delete it.

And that's it! To change the raffle settings, mess around with `options.json`.
If you run into any issues using this script, feel free to shoot me a DM on Bluesky! <br/>
[@iohtheprotogen.art](https://iohtheprotogen.art/)
