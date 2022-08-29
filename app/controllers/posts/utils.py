from typing import Dict, Any, List
from app.controllers.comments.utils import _comment_to_dict
from app.repositories.models import Post


def _post_to_dict(post: Post, with_content: bool = False) -> Dict[str, Any]:
    """ Return some basic information about a post as a dictionary """
    post_dict = {
        "id": post.id,
        "title": post.title,
        "timestamp": post.created_at,
        "author": {
            "id": post.user.id,
            "name": post.user.username
        },
        "num_comments": post.num_comments
    }

    if with_content:
        post_dict["content"] = post.content

    return post_dict


def queryset_to_tree(query: List):
    """ Convert a list of queries to a tree """

    if len(query) == 0:
        return []
    if len(query) == 1:
        return query[0]

    _coments_dict = {}
    roots = []
    node = None

    """
        Populates the auxiliary dictionary with the comment id as key and the index as value than
        initializes the children key with an empty list
    """
    for i in range(len(query)):
        _coments_dict[query[i].id] = i
        query[i] = _comment_to_dict(query[i])
        query[i]['children'] = []

    """
        If the node of the tree has a parent append it to the parent children list
        else it is a root
    """
    for i in range(len(query)):
        node = query[i]
        if node.get('parent'):
            query[_coments_dict[node['parent']['id']]]['children'].append(node)
        else:
            roots.append(node)
    return roots