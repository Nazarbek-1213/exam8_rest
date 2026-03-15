from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsClient(BasePermission):
    message = "Only clients can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'


class IsFreelancer(BasePermission):
    message = "Only freelancers can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'freelancer'


class IsClientOrReadOnly(BasePermission):
    message = "Only clients can create or modify projects."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'client'


class IsContractParticipant(BasePermission):
    message = "You are not a participant of this contract."

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user or obj.freelancer == request.user


class IsProjectOwner(BasePermission):
    message = "You are not the owner of this project."

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user
