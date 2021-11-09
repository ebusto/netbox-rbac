from django.core.exceptions import PermissionDenied
from netbox.views           import generic
from utilities.permissions  import resolve_permission


#
# Bulk view mixins.
#
class BulkCheckView:
    def post(self, request, *args, **kwargs):
        perm = self.get_required_permission()

        if request.POST.get('_all'):
            qs = self.queryset.all()

            if self.filterset:
                qs = self.filterset(request.GET, qs).qs

        else:
            qs = self.queryset.filter(pk__in=request.POST.getlist('pk'))

        for obj in qs.iterator():
            if not request.user.has_perm(perm, obj):
                raise PermissionDenied('%s %s' % (resolve_permission(perm)[1], obj))

        return super().post(request, *args, **kwargs)


class BulkDeleteView(BulkCheckView, generic.BulkDeleteView):
    pass


class BulkEditView(BulkCheckView, generic.BulkEditView):
    pass


class BulkRenameView(BulkCheckView, generic.BulkRenameView):
    pass


#
# Object view mixins.
#
class ObjectCheckView:
    def get(self, request, *args, **kwargs):
        obj  = self.get_object(kwargs)
        perm = self.get_required_permission()

        if not request.user.has_perm(perm, obj):
            raise PermissionDenied('%s %s' % (resolve_permission(perm)[1], obj))

        return super().get(request, *args, **kwargs)


class ObjectDeleteView(ObjectCheckView, generic.ObjectDeleteView):
    pass


class ObjectEditView(ObjectCheckView, generic.ObjectEditView):
    pass
