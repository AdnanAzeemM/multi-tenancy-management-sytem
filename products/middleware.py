from django.http import HttpResponseForbidden
from django_tenants.utils import get_tenant_model, get_public_schema_name, schema_context
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.backends import TokenBackend
from user.models import CustomUser, Client


class CheckTenantDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_model = get_tenant_model()
        current_tenant = request.tenant

        if current_tenant.schema_name == get_public_schema_name():
            return self.get_response(request)

        tenant_domain = current_tenant.domain_url
        user_email = None
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            token = header_token.split(' ')[1]
            try:
                valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
                user_email = valid_data['email']
            except ValidationError as v:
                print("validation error", v)

        if user_email is not None:
            user = CustomUser.objects.get(email=user_email)
            user_domain = user.get_domain()
            if user_domain == tenant_domain:
                return self.get_response(request)
            else:
                return HttpResponseForbidden("You do not have permission to access this domain.")

        response = self.get_response(request)
        return response