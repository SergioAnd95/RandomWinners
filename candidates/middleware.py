from django.core.signing import BadSignature, Signer
from django.conf import settings

from .models import GroupCandidates


class GroupCandidatesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        request.cookies_to_delete = []
        request._group_cache = None
        request.group_candidates = self.get_group(request)

        return request


    def process_response(self, request, response):
        # Delete any surplus cookies
        cookies_to_delete = getattr(request, 'cookies_to_delete', [])
        for cookie_key in cookies_to_delete:
            response.delete_cookie(cookie_key)

        if not hasattr(request, 'group_candidates'):
            return response

        cookie_key = 'group_candidates'
        # Check if we need to set a cookie. If the cookies is already available
        # but is set in the cookies_to_delete list then we need to re-set it.
        has_group_cookie = (
            cookie_key in request.COOKIES
            and cookie_key not in cookies_to_delete)


        if (request.group_candidates and not has_group_cookie):

            cookie = self.get_group_hash(request.group_candidates.id)
            response.set_cookie(
                cookie_key, cookie,
                max_age=settings.GROUP_COOKIE_LIFETIME,
                httponly=True)
        return response

    def get_group(self, request):
        """
        Return the open group_candidates for this request
        """
        if request._group_cache is not None:
            return request._group_cache


        cookie_group = self.get_cookie_group(request)

        if cookie_group:

            group = cookie_group
        else:

            group = GroupCandidates()
            group.save()

        request._group_cache = group

        return group

    def get_cookie_group(self, request):

        group_candidates = None
        if 'group_candidates' in request.COOKIES:
            group_hash = request.COOKIES['group_candidates']

            try:
                group_id = Signer().unsign(group_hash)
                group_candidates = GroupCandidates.objects.get(pk=group_id)
            except (BadSignature, GroupCandidates.DoesNotExist):
                request.cookies_to_delete.append('group_candidates')
        return group_candidates

    def get_group_hash(self, group_id):
        return Signer().sign(group_id)
