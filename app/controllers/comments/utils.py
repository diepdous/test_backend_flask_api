from typing import Dict, Any, List
from app.repositories.models import Comment
from app.repositories.comments import get_children_by_parent_id


def _comment_to_dict(comment: Comment) -> Dict[str, Any]:
    """ Represent a Comment as a dictionary """
    return {
        "id": comment.id,
        "timestamp": comment.created_at,
        "content": comment.content,
        "author": {
            "id": comment.user.id,
            "name": comment.user.username
        },
        "post": {
            "id": comment.post.id,
            "title": comment.post.title
        },
        "parent": {
            "id": comment.parent_comment.id,
            "author": comment.parent_comment.user.username
        } if comment.parent_comment else None
    }


def get_children(comment: Comment):
    """ 
        Get all the children of a comment recursively
    """

    _children = []
    children = get_children_by_parent_id(comment.id)
    if not children: return []
    for child in children:
        _child = _comment_to_dict(child)
        _child['children'] = get_children(child)
        _children.append(_child)
    return _children