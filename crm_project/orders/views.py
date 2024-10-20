from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Category, Status, User
from .forms import OrderForm, MessageForm, ManagerOrderUpdateForm
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.
def assign_manager():
    from django.db.models import Count
    return User.objects.filter(is_manager=True).annotate(order_count=Count('orders')).order_by('order_count').first()

@login_required
def create_order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user  
            order.manager = assign_manager()  
            order.category = Category.objects.first()  
            order.status = Status.objects.first()  
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})

@login_required
def edit_order_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user.is_manager:  
        if request.method == 'POST':
            form = ManagerOrderUpdateForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('order_list')
        else:
            form = ManagerOrderUpdateForm(instance=order)
    else:
        return redirect('order_list') 

    return render(request, 'orders/edit_order.html', {'form': form, 'order': order})

@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user != order.client and not request.user.is_manager:
        return redirect('order_list')

    messages = order.messages.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.order = order
            message.sender = request.user
            message.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = MessageForm()

    return render(request, 'orders/order_detail.html', {'order': order, 'messages': messages, 'form': form})

from django.shortcuts import get_object_or_404

@login_required
def order_list_view(request):
    query = request.GET.get('q', '')  
    status_filter = request.GET.get('status', '') 
    category_filter = request.GET.get('category', '')  

    if request.user.is_manager:
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(client=request.user).order_by('-created_at')

    if status_filter:
        status_obj = get_object_or_404(Status, name=status_filter)
        orders = orders.filter(status=status_obj.id)

    if category_filter:
        orders = orders.filter(category__name=category_filter)

    if query:
        orders = orders.filter(Q(title__icontains=query) | Q(id__icontains=query))

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'query': query,  
        'status_filter': status_filter, 
        'category_filter': category_filter,  
    })