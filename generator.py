import random

def _generate_param(param):
    """
    Generate value of a param.
    """
    final_param = param
    if isinstance(param, list):
        final_param = random.choice(param)
    elif isinstance(param, dict):
        struct = {}
        for k, v in param.iteritems():
            struct[k] = v if not isinstance(v, list) else random.choice(v)
        final_param = struct

    return final_param


def generate_methods(method_spec, site_info, number_of_requests, shuffle=True):
    """
    Generate a list of XML-RPC method tuples based on method specification.
    A method tuple is like ('method_name', [param1, param2, ...]).
    The higher the priority of a method, the more requests will be generated.
    """
    auth_info = [site_info['blog_id'], site_info['username'], site_info['password']]
    methods = []
    consumed_requests = 0
    total_priority = float(sum((t[2] for t in method_spec)))

    for method, params, priority in method_spec:
        actual_name = 'wp.' + method
        requests_in_ratio = int(number_of_requests * priority / total_priority)
        # make sure at least 1 request is allocated
        allocated_requests = requests_in_ratio if requests_in_ratio > 0 else 1
        consumed_requests += allocated_requests

        for i in xrange(allocated_requests):
            actual_params = list(auth_info)
            for param in params:
                actual_params.append(_generate_param(param))
            methods.append((actual_name, actual_params))

        if consumed_requests == number_of_requests:
            # enough!
            break

    if consumed_requests < number_of_requests:
        # not enough, append some
        # use random to keep ratio
        methods += [random.choice(methods) for i in range(number_of_requests-consumed_requests)]

    if shuffle:
        # shuffle to make pattern more realistic
        random.shuffle(methods)

    return methods
