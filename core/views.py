from django.db import connection, DatabaseError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CustomerRecord
from .forms import CustomerForm, CustomerUpdateForm

def home(request):
    return render(request, "core/home.html", {})

def healthcheck(request):
    import time
    from django.conf import settings as conf
    start = time.monotonic()
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
        ok = True; msg = "Database connection OK"
    except DatabaseError as e:
        ok = False; msg = f"Database error: {e}"
    elapsed = round((time.monotonic() - start) * 1000, 1)

    db_conf = conf.DATABASES.get("default", {})
    engine = db_conf.get("ENGINE", "unknown").rsplit(".", 1)[-1]
    db_name = db_conf.get("NAME", "unknown")
    if hasattr(db_name, "name"):
        db_name = db_name.name  # PosixPath → str

    try:
        record_count = CustomerRecord.objects.count()
    except Exception:
        record_count = "N/A"

    return render(request, "core/health.html", {
        "ok": ok,
        "message": msg,
        "db_engine": engine,
        "db_name": db_name,
        "debug_mode": "Enabled" if conf.DEBUG else "Disabled",
        "record_count": record_count,
        "response_time": elapsed,
    })

def records_list(request):
    q = request.GET.get("q", "").strip()
    qs = CustomerRecord.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(ifsc__icontains=q) | Q(city__icontains=q) | Q(applicant_no__icontains=q) | Q(branch__icontains=q))
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "core/records_list.html", {"page_obj": page_obj, "q": q, "count": qs.count()})

def add_record(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record added successfully.")
            return HttpResponseRedirect(reverse("records_list"))
    else:
        form = CustomerForm()
    return render(request, "core/add_record.html", {"form": form})

def edit_record(request, pk):
    record = get_object_or_404(CustomerRecord, pk=pk)
    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record #{pk} updated.")
            return HttpResponseRedirect(reverse("records_list"))
    else:
        form = CustomerUpdateForm(instance=record)
    return render(request, "core/edit_record.html", {"form": form, "record": record})

def delete_record(request, pk):
    record = get_object_or_404(CustomerRecord, pk=pk)
    if request.method == "POST":
        record.delete()
        messages.warning(request, f"Record #{pk} deleted.")
        return HttpResponseRedirect(reverse("records_list"))
    return render(request, "core/delete_record.html", {"record": record})

def _totals_from_records(records):
    return {"credit": sum((r.credit for r in records), 0.0), "debit": sum((r.debit for r in records), 0.0), "balance": sum((r.balance for r in records), 0.0)}

def passbook_all(request):
    records = CustomerRecord.objects.all()
    totals = _totals_from_records(records)
    return render(request, "core/passbook_all.html", {"records": records, "totals": totals})

def passbook_branch(request):
    branch_code = request.GET.get("branch")
    rows = []
    with connection.cursor() as cur:
        if branch_code:
            cur.execute("SELECT applicant_no,name,ifsc,credit,debit,balance,city,branch FROM customer_records WHERE branch = %s", [branch_code])
        else:
            cur.execute("SELECT applicant_no,name,ifsc,credit,debit,balance,city,branch FROM customer_records")
        rows = cur.fetchall()
    totals = {"credit":0.0,"debit":0.0,"balance":0.0}
    for r in rows:
        totals["credit"] += float(r[3]); totals["debit"] += float(r[4]); totals["balance"] += float(r[5])
    return render(request, "core/passbook_branch.html", {"rows": rows, "branch": branch_code or "", "totals": totals})

def passbook_applicant(request):
    applicant = request.GET.get("applicant_no")
    row = None
    if applicant:
        with connection.cursor() as cur:
            cur.execute("SELECT applicant_no,name,ifsc,credit,debit,balance,city,branch FROM customer_records WHERE applicant_no = %s", [applicant])
            row = cur.fetchone()
    return render(request, "core/passbook_applicant.html", {"row": row, "applicant": applicant or ""})

def sql_queries(request):
    return render(request, "core/sql_queries.html", {})

def source_code(request):
    return render(request, "core/source_code.html", {})
