from itertools import groupby
from werkzeug.exceptions import NotFound
from flask import Blueprint, jsonify

from app.repositories import comments as repositories

from ..comments.utils import _comment_to_dict, get_children

BLUEPRINT = Blueprint('users', __name__)

@BLUEPRINT.route('/users/<user_id>/comments')
def get_user_comments_tree(user_id):
    user_comments = repositories.get_user_comments(user_id)
    result = []
    comments = []

    """
        Group the comments by the post ID
    """
    comments_group_by = [list(comments) for _,comments in groupby(user_comments, key=lambda comment: comment.post_id)]

    for user_comments in comments_group_by:
        comments = []
        post_id = user_comments[0].post_id
        for comment in user_comments:
            _comment = _comment_to_dict(comment)
            """
                Get all the comment children than the parents
            """
            _comment['children'] = get_children(comment)
            while _comment.get('parent'):
                parent = repositories.get_comment_by_id(_comment['parent']['id'])
                _parent = _comment_to_dict(parent)
                _parent['children'] = [_comment]
                _comment = _parent

                if not _comment.get('parent'): break
            comments.append(_comment)
        result.append({
            'post_id': post_id,
            'comments': comments,
        })
    return jsonify(result)