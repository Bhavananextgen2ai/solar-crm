# leads/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count, Sum
from datetime import date

from .models import Lead
from .forms import LeadForm

# ---------------------------
# Enquiry Form View
# ---------------------------
def enquiry_view(request):
    if request.method == "POST":
        form = LeadForm(request.POST, request.FILES)
        if form.is_valid():
            lead = form.save(commit=False)
            # Optional: assign current user if needed
            # lead.assigned_to = request.user
            lead.save()
            messages.success(request, "Lead created successfully!")
            return redirect('leads:lead_list')   # 🔹 include namespace
        else:
            print(form.errors)  # Debug errors
    else:
        form = LeadForm()

    return render(request, 'leads/enquiry.html', {'form': form})

# ---------------------------
# Lead List View (Search Filter)
# ---------------------------
def lead_list(request):
    query = request.GET.get("q", "").strip()
    leads = Lead.objects.all()

    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    leads = leads.order_by("-created_at")

    return render(request, "leads/lead_list.html", {
        "leads": leads,
        "query": query,
    })

# ---------------------------
# Lead Detail View
# ---------------------------
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, "leads/lead_detail.html", {"lead": lead})

# ---------------------------
# Add Lead View
# ---------------------------
def add_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST, request.FILES)
        if form.is_valid():
            lead = form.save(commit=False)
            # Optional: assign current user automatically
            # lead.assigned_to = request.user
            lead.save()
            messages.success(request, "Lead added successfully!")
            return redirect("leads:lead_list")
        else:
            print(form.errors)
    else:
        form = LeadForm()

    return render(request, "leads/add_lead.html", {"form": form})

# ---------------------------
# Edit Lead View
# ---------------------------
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = LeadForm(request.POST, request.FILES, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead updated successfully!")
            return redirect('leads:lead_list')
        else:
            print(form.errors)
    else:
        form = LeadForm(instance=lead)

    return render(request, 'leads/lead_edit.html', {
        'form': form
    })
   

# ---------------------------
# Delete Lead View
# ---------------------------
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.success(request, "Lead deleted successfully!")
    return redirect("leads:lead_list")

# ---------------------------
# Dashboard View
# ---------------------------
def dashboard(request):
    today = date.today()

    total_leads = Lead.objects.count()
    converted_leads = Lead.objects.filter(status="converted").count()
    pending_leads = Lead.objects.exclude(status="converted").count()

    total_revenue = 0

    status_counts = Lead.objects.values("status").annotate(count=Count("id"))

    # ✅ Follow-up filtering
    today_followups = Lead.objects.filter(follow_up_date=today)
    overdue_followups = Lead.objects.filter(follow_up_date__lt=today)

    context = {
        "total_leads": total_leads,
        "converted_leads": converted_leads,
        "pending_leads": pending_leads,
        "total_revenue": total_revenue,
        "status_counts": status_counts,
        "recent_leads": Lead.objects.order_by("-created_at")[:5],
        "today_followups": today_followups,
        "overdue_followups": overdue_followups,
    }

    return render(request, "leads/dashboard.html", context)

# ---------------------------
# Generate Invoice
# ---------------------------
def generate_invoice(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    invoice_data = {
        "invoice_number": f"INV-{lead.id:05d}",
        "date": lead.created_at,
        "lead_name": lead.name,
        "lead_email": lead.email,
        "lead_phone": lead.phone,
        "status": lead.status,
    }
    return render(request, "leads/invoice.html", {"invoice": invoice_data})

# ---------------------------
# Record Payment
# ---------------------------
def record_payment(request):
    if request.method == "POST":
        lead_id = request.POST.get("lead_id")
        amount = request.POST.get("amount")
        lead = get_object_or_404(Lead, id=lead_id)
        Payment.objects.create(lead=lead, amount=amount)
        messages.success(request, "Payment recorded successfully!")
        return redirect("leads:dashboard")

    leads = Lead.objects.all()
    return render(request, "leads/record_payment.html", {"leads": leads})