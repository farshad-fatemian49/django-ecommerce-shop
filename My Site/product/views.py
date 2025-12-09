from django.shortcuts import get_object_or_404, render , redirect
from .models import Product , Comments , Toptrend , DiscountedProducts
# Create your views here.
from .forms import Buy , CommentForm , ProductForm
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
from django.conf import settings
# def product_list(request):
#     products = Product.objects.all()
    
#     paginator = Paginator(products, 4) # Show 4 contacts per page.

#     page_number = request.GET.get('page')
#     Products_final = paginator.get_page(page_number)
    
#     context = {
#         "products" : Products_final,
        
#     }
#     return render(request,"product/furn-master/List_final.html",context)






def product_detail(request,id):
    
    
    selected_product = get_object_or_404(Product,id=id)
    # tags = list(selected_product.tags)
    
    AllComments = list(selected_product.comments.all())
    AllPictures = list(selected_product.Pictures.all())
    
    if selected_product.available :
        buy_form = Buy(quantity_m = selected_product.number)
    else :
        buy_form = False    
        
    #comment part
    
    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.writer = request.user
            obj.product = selected_product
            obj.save()
            return HttpResponseRedirect(request.path_info)
    else :
        form = CommentForm()
        
        
        
    # edited by me start greatest path of session wowwwwwww
    cart = request.session.get(settings.CART_SESSION_ID)
    product_id = str(selected_product.id)
    if product_id not in cart:
        cart_product_form = CartAddProductForm()
    else:
        cart_product_form = CartAddProductForm(initial={
            'quantity': cart[product_id]['quantity'],
            'override':True,
        })
    # edited by me end
        
    
    context = {
        "s_product" : selected_product ,
        # "tags": tags ,
        "buy_form1" : buy_form ,
        "s_comments" : AllComments,
        "s_Pictures" : AllPictures,
        "form" : form ,
        'form2':cart_product_form,
    }
    return render(request,"product/detail_final2.html",context)

#edit product part

@login_required
def product_update(request,id):
    selected_product = get_object_or_404(Product,id=id)
    if request.user == selected_product.seller:
        form = ProductForm(request.POST or None,instance=selected_product)
        if request.method == "POST" :
            if form.is_valid():
                form.save()
                # return HttpResponseRedirect("/"+"product/"+str(id))
                return redirect('product:product_list')
        else:
            form = ProductForm(instance=selected_product)
        context ={
            "form":form,
            "product":selected_product
        }
        return render(request,"product/product_update.html",context)
    else:
        HttpResponseForbidden
        
        
@login_required
def comment_update(request,c_id,p_id):
    selected_product = get_object_or_404(Product,id=p_id)
    selected_comment = get_object_or_404(Comments,id=c_id)
    if request.user == selected_comment.writer:
        form = CommentForm(request.POST or None,instance=selected_comment)
        if request.method == "POST" :
            if form.is_valid():
                form.save()
                # return HttpResponseRedirect("/"+"product/"+str(id))
                return redirect("/"+"product/"+str(p_id))
        else:
            form = CommentForm(instance=selected_comment)
        context ={
            "form":form,
            "comment":selected_comment,
            "s_product":selected_product,
        }
        return render(request,"product/comment_update.html",context)
    else:
        HttpResponseForbidden
            
    
    
def Product_Category(request,category):
    
    products = Product.objects.filter(category__slug = category)
    
    paginator = Paginator(products, 4) # Show 4 contacts per page.

    page_number = request.GET.get('page')
    Products_final = paginator.get_page(page_number)
    toptrends = Toptrend.objects.all()
    toptrends = list(toptrends)
    context = {
        "products" : Products_final,
        'toptrends': toptrends[1:],
        'active': toptrends[0]
        
    }
    return render(request,"product/product_list2.html",context)
    
    
    
    
def Product_Tag(request,tag):
    
    products = Product.objects.filter(tags__slug = tag)
    
    paginator = Paginator(products, 4) # Show 4 contacts per page.

    page_number = request.GET.get('page')
    Products_final = paginator.get_page(page_number)
    
    toptrends = Toptrend.objects.all()
    toptrends = list(toptrends)
    context = {
        "products" : Products_final,
        'toptrends': toptrends[1:],
        'active': toptrends[0]
        
    }
    return render(request,"product/product_list2.html",context)


# def search(request):
#     if request.method == "GET":
#         q = request.GET.get("search")
        
#     products = Product.objects.filter(name__icontains = q)
#     return render( request,"product/furn-master/List_final.html",{"products" : products} )

from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request,order=None):
    if order :
        order = str(order)
        products_list = Product.objects.order_by(order)
    else:
        products_list = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products_list = Product.objects.filter(
            Q(description__icontains=query) | Q(name__icontains=query) 
        ).distinct()
        if order :
            order = str(order)
            products_list = products_list.order_by(order)
        
        
        
    paginator = Paginator(products_list, 4) # 4 products per page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    
    
    toptrends = Toptrend.objects.all()
    toptrends = list(toptrends)
    D_products = DiscountedProducts.objects.all()
    context = {
        'products': products,
        'toptrends': toptrends[1:],
        'active': toptrends[0],
        "d_products":D_products,
    }
    return render(request, "product/product_list2.html", context)


@login_required
def Dashboard(request):
    seller = request.user
    products = seller.products.all()
    
    context = {
        'products': products,
    }
    return render(request, "product/Dashboard.html", context)
    
    