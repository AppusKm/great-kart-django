# this take request as an argument and return dictionary of data as context

# TODO  if we are using context_processors.py inform that in settings templates options i
# TODO  we are creating this because once it is registered in settings this will available all other templates also
from .models import Category
def categoryMenuList(request):
    cat_list = Category.objects.all()
    return dict(cats = cat_list)