from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import DONE

class IsAuthenticatedAndDone(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method is SAFE_METHODS:
            return True
        
        return request.user.status == DONE
    

class IsAuthenticatedAndAuthor(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method is SAFE_METHODS:
            return True
        
        return request.user.status == DONE
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsAuthenticatedAndAuthorForMedia(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method is SAFE_METHODS:
            return True
        
        return request.user.status == DONE
    
    def has_object_permission(self, request, view, obj):
        return obj.post.user == request.user
    



