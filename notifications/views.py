from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Comment
from repairs.models import RepairRequest
from notifications.services import notify_admins_new_comment

@login_required
def comment_create_view(request, repair_id):
    repair = get_object_or_404(RepairRequest, id=repair_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if not content:
            messages.error(request, "Comment cannot be empty.")
            return redirect("dashboard")

        comment = Comment.objects.create(
            user=request.user,
            repair_request=repair,
            content=content
        )

        notify_admins_new_comment(comment)

        messages.success(request, "Comment added and admins notified.")
        return redirect("dashboard")
