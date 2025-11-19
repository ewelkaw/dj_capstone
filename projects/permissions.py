from django.core.exceptions import PermissionDenied


def require_owner_or_staff(user, obj):
    if not user.is_authenticated:
        raise PermissionDenied("Login required")
    if user.is_staff:
        return
    if obj.owner_id != user.id:
        raise PermissionDenied("Not allowed")
