from typing import List, Optional
from .models import Comment


def get_comment_by_id(comment_id: int) -> Optional[Comment]:
    """ Return the comment referenced by comment_id. Return None otherwise. """
    return Comment.query.get(comment_id)


def get_comment_by_parent_id(parent_comment_id: int) -> Optional[Comment]:
    """ Return the comment referenced by parent_comment_id. Return None otherwise. """
    return Comment.query.get(parent_comment_id=parent_comment_id)


def get_all_user_comments_bt_post(user_id: int, post_id: int):
    return (Comment.query
    .order_by(Comment.created_at.desc())
    .filter_by(user_id=user_id, post_id=post_id)
    .all()
    )

def get_children_by_parent_id(parent_comment_id: int):
    return (Comment.query
    .order_by(Comment.created_at.desc())
    .filter_by(parent_comment_id=parent_comment_id)
    .all()
    )


def get_post_comments(post_id: int) -> List[Comment]:
    """ Retrieve all comments associated with a post, sorted from most to least
        recent
    """
    return (
        Comment.query
        .order_by(Comment.created_at.desc())
        .filter_by(post_id=post_id)
        .all()
    )


def get_user_comments(user_id: int) -> List[Comment]:
    """ Retrieve all comments associated with a user, sorted from most to least
        recent
    """
    return (
        Comment.query
        .order_by(Comment.created_at.desc())
        .filter_by(user_id=user_id)
        .all()
    )
