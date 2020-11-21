from django import TEMPLATE

register = template.Library()

@register.filter(name='cut')
#Custom template filter
def cutFunc(value,arg):
    """
    This cuts out all values of "arg" from the string!
    """
    return value.replace(arg,'')

#Pass in 1) what you want to call this filter and 2) the function
# register.filter('cut',cutFunc)
