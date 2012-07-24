# test configuration of WordPress XML-RPC
import datetime

# basic site information
site_info = {
    'endpoint': 'http://example.com/wordpress/xmlrpc.php',
    'blog_id': 1,
    'username': 'username_goes_here',
    'password': 'password_goes_here',
}

# methods configuration
# parameters except blog_id, username and password should be arranged in a list
# if the parameter is struct and the configured value is a list, a random one will be picked
method_specification = [
    ('getPost', [range(1, 20)], 10),
    ('getPosts', [{
        'post_type': ['post', 'page', 'revision', 'attachment'],
        'post_status': ['publish', 'inherit'],
    }], 10),
    ('newPost', [{
        'post_type': ['post', 'page'],
        'post_status': ['publish', 'draft', 'future'],
        'post_title': ['Bird', 'Dog', 'Testing XML-RPC', 'Dudu'],
        'post_author': 1,
        'post_excerpt': ['excerpt1', 'excerpt2', 'excerpt3', 'excerpt4'],
        'post_content': 'sample content',
        'post_date': datetime.datetime.utcnow(),
        'comment_status': ['open', 'closed'],
        'sticky': [True, False],
    }], 15),
    ('getPostType', [['page', 'post', 'attachment', 'revision']], 5),
    ('getPostFormats', [], 5),
    ('getPostStatusList', [], 5),
    ('getTaxonomies', [], 5),
    ('getTaxonomy', [['category', 'post_tag', 'post_format']], 5),
    ('getTerms', [['category', 'post_tag', 'post_format']], 5),
]

