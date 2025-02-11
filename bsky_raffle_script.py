"""Automatically runs a raffle on a Bluesky post given certain perameters."""
from json import load
from random import shuffle, randint
from atproto import Client, exceptions

def account_login():
    """Logs in to the account specified in login.json"""
    client = Client()

    try: # Try login with session string
        session = open("session_string.txt", encoding="utf-8").read()
        client.login(session)

    except (FileNotFoundError, ValueError): # If session string missing or invalid, login normally
        credentials = load(open("login.json", encoding="utf-8"))

        client.login(credentials["handle"], credentials["password"])
        session = client.export_session_string()

        try:
            open("session_string.txt", "x", encoding="utf-8").write(session)

        except FileExistsError:
            open("session_string.txt", "w", encoding="utf-8").write(session)
    return client

CLIENT = account_login()
RAFFLE_OPTIONS = load(open("options.json", encoding="utf-8"))
RAFFLE_HANDLE = ""

def get_candidates():
    """Log in and prompt user for the post embed (HTML)."""
    global RAFFLE_HANDLE
    while True:
        uri = input("Paste the post link: ").strip()
        try:
            split_uri = uri.replace("//", "/").split("/")

            link_type = "at" if uri[0:5] == "at://" else "https"
            match link_type:
                case "https":
                    actor = CLIENT.app.bsky.actor.get_profile({"actor": split_uri[-3]})
                case "at":
                    actor = CLIENT.app.bsky.actor.get_profile({"actor": split_uri[1]})

            RAFFLE_HANDLE, did = actor.handle, actor.did
            post_uri = f"at://{did}/app.bsky.feed.post/{split_uri[-1]}"
            break
        except (IndexError, ValueError, exceptions.AtProtocolError):
            print("ERROR: Invalid URL. Perhaps it's incorrect?")
    print("\n")

    # Get relevant post data for likes, comments, and reposts
    must_follow = RAFFLE_OPTIONS["follow"]
    must_like = RAFFLE_OPTIONS["like"]
    must_repost = RAFFLE_OPTIONS["repost"]

    must_comment = RAFFLE_OPTIONS["comment"]
    comment_needs_image = RAFFLE_OPTIONS["image"]

    blacklist = [tag.replace("@", "") for tag in RAFFLE_OPTIONS["blacklist"]]

    if RAFFLE_HANDLE not in blacklist: # Ensures the host can't win
        blacklist.append(RAFFLE_HANDLE)

    if must_repost:
        repost_handles = []
        repost_list = CLIENT.get_reposted_by(post_uri).reposted_by
        if len(repost_list) > 0:
            for repost in repost_list:
                if must_follow and repost.viewer.followed_by is None:
                    continue # Follow Check
                if repost.handle not in repost_handles: # Skips duplicates just in case
                    repost_handles.append(repost.handle)

    if must_like:
        like_handles = []
        like_list = CLIENT.get_likes(post_uri).likes
        if len(like_list) > 0:
            for like in like_list:
                actor = like.actor
                if must_follow and actor.viewer.followed_by is None:
                    continue # Follow Check
                if actor.handle not in like_handles: # Skips duplicates just in case
                    like_handles.append(actor.handle)

    if must_comment:
        comment_handles = []
        comment_list = CLIENT.get_post_thread(post_uri, 1).thread.replies
        if len(comment_list) > 0:
            for comment in comment_list:
                post = comment.post
                if must_follow and post.author.viewer.followed_by is None:
                    continue # Follow Check
                try:
                    if comment_needs_image and post.record.embed.py_type != "app.bsky.embed.images":
                        continue # Image Embed Check
                except TypeError:
                    continue # No embed found.
                if post.author.handle not in comment_handles: # Skips duplicates
                    comment_handles.append(post.author.handle)

    # Compare all data to get the final candidate list

    final_handle_list = []
    if must_like and must_comment:
        final_handle_list = [h for h in like_handles if h in comment_handles]
    elif must_like:
        final_handle_list = like_handles
    else:
        final_handle_list = comment_handles
    if must_repost:
        final_handle_list = [h for h in final_handle_list if h in repost_handles]
    final_handle_list = [h for h in final_handle_list if h not in blacklist]
    return final_handle_list


def select_winners(final_handle_list):
    """Select the winners."""
    if len(final_handle_list) > 0:
        final_handle_list = list(set(final_handle_list)) # Absolutely sure to remove all duplicates.
        shuffle(final_handle_list)
        winners = []
        win_amount = RAFFLE_OPTIONS["winners"]
        if len(final_handle_list) > win_amount:
            for _ in range(win_amount):
                winners.append(final_handle_list.pop(randint(0, len(final_handle_list) - 1)))
        else:
            winners = final_handle_list
            print("(There were fewer candidates than specified winners. Everyone wins!\n\n)")
        if win_amount == 1:
            print(f"And the winner for {RAFFLE_HANDLE}'s raffle is:\n")
        else:
            print(f"And the winners for {RAFFLE_HANDLE}'s raffle are:\n")

        for winner in winners:
            print(winner)

        print("\nThank you everyone for participating!\n\n")
    else:
        print("\n\nThere are no users that meet the specified criteria for this raffle.\n\n")


def reroll(names: list[str], candidates: list[str]):
    """Rerolls the selected winners from the list of candidates."""
    new_winners = []
    for _ in names:
        new_winners.append(candidates.pop(randint(0, len(candidates) - 1)))
    return new_winners


def main():
    """Run the thing."""
    try:
        candidates = get_candidates()
        select_winners(candidates)
    except exceptions.AtProtocolError:
        print("Your handle and/or password are incorrect or you are being rate limited.")
        print("Make sure your login credentials are correct, and if the issue persists,")
        print("wait a minute or so.")

if __name__ == "__main__":
    main()
