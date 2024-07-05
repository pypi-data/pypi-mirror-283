from typing import Union

from ._utilities import timestamp_to_readable, TIME_FORMAT


def clean_users(
    data: Union[list[dict], dict], time_format: TIME_FORMAT
) -> Union[list[dict], dict]:
    """
    Cleans a list/single object of raw user data.

    :param data: A list of dict objects, each containing raw user data.
    :type data: list[dict]
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A list of parsed dict objects, each containing user data Or a dict object containing user data.
    :rtype: Union[list[dict], dict]
    """

    def build_user(user: dict) -> dict:
        """
        Cleans raw user data to get only the needed data.

        :param user: Raw user data.
        :type user: dict
        :return: A dict object containing parsed user data.
        :rtype: dict
        """
        return {
            "name": user.get("name"),
            "id": user.get("id"),
            "avatar_url": user.get("icon_img"),
            "is_verified": user.get("verified"),
            "has_verified_email": user.get("has_verified_email"),
            "is_gold": user.get("is_gold"),
            "is_mod": user.get("is_mod"),
            "is_blocked": user.get("is_blocked"),
            "is_employee": user.get("is_employee"),
            "hidden_from_bots": user.get("hide_from_robots"),
            "accepts_followers": user.get("accept_followers"),
            "comment_karma": user.get("comment_karma"),
            "link_karma": user.get("link_karma"),
            "awardee_karma": user.get("awardee_karma"),
            "total_karma": user.get("total_karma"),
            "subreddit": user.get("subreddit"),
            "created": (
                timestamp_to_readable(
                    timestamp=user.get("created"), time_format=time_format
                )
                if user.get("created")
                else "NaN"
            ),
        }

    converted_data = None
    if isinstance(data, list) and len(data) != 0:
        converted_data = [build_user(user.get("data")) for user in data]

    elif isinstance(data, dict) and "is_employee" in data:
        converted_data = build_user(data)

    return converted_data


def clean_posts(
    data: Union[dict, list], time_format: TIME_FORMAT
) -> Union[list[dict], dict]:
    """
    Cleans a list/single object of raw post data.

    :param data: A list of dict objects, each containing raw post data.
    :type data: list[dict]
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A list of parsed dict objects, each containing post data Or a dict object containing post data.
    :rtype: Union[list[dict], dict]
    """

    def build_post(post: dict) -> dict:
        """
        Cleans raw post data to get only the needed data.

        :param post: Raw post data.
        :type post: dict
        :return: A dict object containing parsed post data.
        :rtype: dict
        """
        return {
            "author": post.get("author"),
            "title": post.get("title"),
            "body": post.get("selftext"),
            "id": post.get("id"),
            "subreddit": post.get("subreddit"),
            "subreddit_id": post.get("subreddit_id"),
            "subreddit_type": post.get("subreddit_type"),
            "upvotes": post.get("ups"),
            "upvote_ratio": post.get("upvote_ratio"),
            "downvotes": post.get("downs"),
            "thumbnail": post.get("thumbnail"),
            "gilded": post.get("gilded"),
            "is_nsfw": post.get("over_18"),
            "is_shareable": post.get("is_reddit_media_domain"),
            "is_robot_indexable": post.get("is_robot_indexable"),
            "permalink": post.get("permalink"),
            "is_locked": post.get("locked"),
            "is_archived": post.get("archived"),
            "domain": post.get("domain"),
            "score": post.get("score"),
            "edited": (
                timestamp_to_readable(
                    timestamp=post.get("edited"), time_format=time_format
                )
                if post.get("edited")
                else False
            ),
            "comments": post.get("num_comments"),
            "created": (
                timestamp_to_readable(
                    timestamp=post.get("created"), time_format=time_format
                )
                if post.get("created")
                else "NaN"
            ),
        }

    if isinstance(data, dict):
        return build_post(post=data)

    elif isinstance(data, list):
        return [build_post(post.get("data")) for post in data if post.get("data")]


def clean_comments(comments: list[dict], time_format: TIME_FORMAT) -> list[dict]:
    """
    Cleans a list of raw comments data to get only the needed data in each item.

    :param comments: A list of dict objects, each containing raw comment data.
    :type comments: list[dict]
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A list of parsed dict objects, each containing comments data.
    :rtype: list[dict]
    """
    if len(comments) != 0:
        comments_list: list = []
        for comment in comments:
            comment_data: dict = comment.get("data")
            comments_list.append(
                {
                    "body": comment_data.get("body"),
                    "id": comment_data.get("id"),
                    "author": comment_data.get("author"),
                    "author_is_premium": comment_data.get("author_premium"),
                    "upvotes": comment_data.get("ups"),
                    "downvotes": comment_data.get("downs"),
                    "subreddit": comment_data.get("subreddit_name_prefixed"),
                    "subreddit_type": comment_data.get("subreddit_type"),
                    "post_id": comment_data.get("link_id"),
                    "post_title": comment_data.get("link_title"),
                    "is_nsfw": comment_data.get("over_18"),
                    "is_edited": comment_data.get("edited"),
                    "score": comment_data.get("score"),
                    "hidden_score": comment_data.get("score_hidden"),
                    "gilded": comment_data.get("gilded"),
                    "is_stickied": comment_data.get("stickied"),
                    "is_locked": comment_data.get("locked"),
                    "is_archived": comment_data.get("archived"),
                    "created": (
                        timestamp_to_readable(
                            timestamp=comment.get("created"), time_format=time_format
                        )
                        if comment.get("created")
                        else "NaN"
                    ),
                }
            )

        return comments_list


def clean_subreddits(
    data: Union[list, dict], time_format, is_preview: bool = False
) -> Union[list[dict], dict]:
    """
    Cleans a list/single object of raw subreddits data.

    :param data: A list of dict objects, each containing raw subreddit data.
    :type data: list[dict]
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :param is_preview: A boolean value to determine whether a subreddit is a preview,
        i.e. Its object contains fewer data.
    :return: A list of parsed dict objects, each containing subreddits data Or a dict object containing subreddit data.
    :rtype: Union[list[dict], dict]
    """

    def build_subreddit(
        subreddit: dict,
    ) -> dict:
        """
        Cleans raw subreddit data to get only the needed data.

        :param subreddit: Raw subreddit data.
        :type subreddit: dict
        :return: A dict object containing parsed subreddit data.
        :rtype: dict
        """
        if is_preview:
            subreddit_obj = {
                "name": subreddit.get("display_name"),
                "id": subreddit.get("id"),
                "type": subreddit.get("subreddit_type"),
                "icon": subreddit.get("subreddit_icon", "").split("?")[0],
                "subscribers": subreddit.get("subscribers"),
                "whitelist_status": subreddit.get("whitelist_status"),
                "url": subreddit.get("url"),
                "created": timestamp_to_readable(
                    timestamp=subreddit.get("created"), time_format=time_format
                ),
            }
        else:
            subreddit_obj = {
                "name": subreddit.get("display_name"),
                "id": subreddit.get("id"),
                "description": subreddit.get("public_description"),
                "submit_text": subreddit.get("submit_text"),
                "icon": subreddit.get("subreddit_icon", "").split("?")[0],
                "type": subreddit.get("subreddit_type"),
                "subscribers": subreddit.get("subscribers"),
                "current_active_users": subreddit.get("accounts_active"),
                "is_nsfw": subreddit.get("over18"),
                "language": subreddit.get("lang"),
                "whitelist_status": subreddit.get("whitelist_status"),
                "url": subreddit.get("url"),
                "created": (
                    timestamp_to_readable(
                        timestamp=subreddit.get("created"), time_format=time_format
                    )
                    if subreddit.get("created")
                    else "NaN"
                ),
            }

        return subreddit_obj

    subreddit_data = None
    if isinstance(data, list) and len(data) != 0:
        subreddit_data = [
            build_subreddit(subreddit=subreddit.get("data")) for subreddit in data
        ]

    elif isinstance(data, dict) and "subreddit_type" in data:
        subreddit_data = build_subreddit(subreddit=data)

    return subreddit_data


def clean_subreddit_wiki_page(wiki_page: dict, time_format: TIME_FORMAT) -> dict:
    """
    Cleans raw subreddit wiki page data to get only the needed data.

    :param wiki_page: Raw wiki page data.
    :type wiki_page: dict
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A dict object of parsed wiki page data.
    :rtype: dict
    """
    if "revision_id" in wiki_page:
        page_data: dict = wiki_page.get("data")
        user: dict = page_data.get("revision_by").get("data")

        return {
            "revision_id": page_data.get("revision_id"),
            "revision_date": timestamp_to_readable(
                timestamp=page_data.get("revision_date")
            ),
            "content_markdown": page_data.get("content_md"),
            "revised_by": {
                "name": user.get("name"),
                "id": user.get("id"),
                "avatar_url": user.get("icon_img"),
                "is_verified": user.get("verified"),
                "has_verified_email": user.get("has_verified_email"),
                "is_gold": user.get("is_gold"),
                "is_mod": user.get("is_mod"),
                "is_blocked": user.get("is_blocked"),
                "is_employee": user.get("is_employee"),
                "hidden_from_bots": user.get("hide_from_robots"),
                "accepts_followers": user.get("accept_followers"),
                "comment_karma": user.get("comment_karma"),
                "link_karma": user.get("link_karma"),
                "awardee_karma": user.get("awardee_karma"),
                "total_karma": user.get("total_karma"),
                "subreddit": user.get("subreddit"),
                "created": timestamp_to_readable(
                    timestamp=user.get("created"), time_format=time_format
                ),
            },
        }
