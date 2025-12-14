from rest_framework import permissions


class IsRole(permissions.BasePermission):
    """Allow access only to users with matching role."""

    allowed_roles: tuple[str, ...] = ()

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsCustomer(IsRole):
    allowed_roles = ("user",)


class IsVendor(IsRole):
    allowed_roles = ("vendor",)


class IsRider(IsRole):
    allowed_roles = ("rider",)


class IsVendorOwner(permissions.BasePermission):
    """Vendor can modify only their own vendor-linked objects."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated or user.role != "vendor":
            return False

        vendor = getattr(user, "vendor_profile", None)
        if vendor is None:
            return False

        if hasattr(obj, "vendor"):
            return obj.vendor == vendor
        if hasattr(obj, "user"):
            return obj.user == user
        # Allow vendors to manage their own Vendor profile objects directly.
        if hasattr(obj, "restaurant_name"):
            return obj == vendor
        return False
