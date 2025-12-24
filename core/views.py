from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import VisitorEntryForm
from .models import Property, VisitorEntry

def home(request):
    # Get first property for test link
    test_property = Property.objects.first()
    test_property_id = test_property.id if test_property else None
    return render(request, 'home.html', {
        'test_property_id': test_property_id
    })

@login_required
def dashboard(request):
    properties = Property.objects.filter(owner=request.user)
    pending_requests = VisitorEntry.objects.filter(property__in=properties, status='pending')
    return render(request, 'dashboard.html', {
        'properties': properties,
        'pending_requests': pending_requests
    })

def visitor_entry(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = VisitorEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.property = property
            if entry.reason != 'other':
                entry.other_reason = ''
            entry.save()
            return render(request, 'waiting.html')
    else:
        form = VisitorEntryForm()
    return render(request, 'visitor_entry.html', {'form': form, 'property': property})

@login_required
def approve_entry(request, entry_id):
    entry = get_object_or_404(VisitorEntry, id=entry_id, property__owner=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        entry.status = 'approved' if action == 'approve' else 'rejected'
        entry.save()
        messages.success(request, f'Visitor {entry.visitor_name} has been {entry.status.lower()}!')
        return redirect('dashboard')
    return render(request, 'approval.html', {'entry': entry})



from django.http import JsonResponse

def check_status(request, entry_id):
    entry = get_object_or_404(VisitorEntry, id=entry_id)
    return JsonResponse({'status': entry.status})