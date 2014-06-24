from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

# Create your views here.
@dajaxice_register
def test(request):
    return simplejson.dumps({'count':19})