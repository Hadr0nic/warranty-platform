from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RepairRequest, ProductCategory

from files.models import UploadedFile
from files.utils import upload_to_arvan

def repair_create(request):
    categories = ProductCategory.objects.all()

    if request.method == "POST":

        if not request.user.is_authenticated:
            messages.error(request, "You must log in to submit a repair request.")
            return redirect("login")

        if request.user.role != "customer":
            messages.error(request, "Admins and technicians cannot request repairs.")
            return redirect("repair_create")

        category_id = request.POST.get("product_category")
        if not category_id:
            messages.error(request, "Please select a product category.")
            return redirect("repair_create")


        repair = RepairRequest.objects.create( # repair request
            user=request.user,
            title=request.POST.get("title", "").strip(),
            description=request.POST.get("description", "").strip(),
            product_category_id=category_id,
            address=request.POST.get("address", "").strip()  # adress is optional
        )

        # uploaded files
        # 1. Damage picture (optional)
        damage_file = request.FILES.get("damage_picture")
        if damage_file:
            # upload to ArvanCloud and get URL
            url = upload_to_arvan(damage_file, folder="damage")

            UploadedFile.objects.create(
                user=request.user,
                repair_request=repair,
                file_type=UploadedFile.IMAGE,
                file_url=url,
            )

        # 2. Warranty card picture (mandatory)
        warranty_file = request.FILES.get("warranty_card")
        if not warranty_file:
            messages.error(request, "Warranty card picture is required.")
            repair.delete()  
            return redirect("repair_create")

        url = upload_to_arvan(warranty_file, folder="warranty")
        UploadedFile.objects.create(
            user=request.user,
            repair_request=repair,
            file_type=UploadedFile.IMAGE,
            file_url=url,
        )


        return redirect("dashboard")

    return render(request, "create.html", {"categories": categories})