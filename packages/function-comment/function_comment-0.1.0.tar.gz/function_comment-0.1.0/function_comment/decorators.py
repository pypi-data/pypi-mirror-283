# function_comment/decorators.py
def bbkp(func):
    """Decorator to mark a function as not to be interpreted."""
    func._dont_interpret = True
    return func

def ujmp(func):
    """Decorator to replace the function with a no-op if marked by bbkp."""
    def wrapped(*args, **kwargs):
        if getattr(wrapped, '_dont_interpret', False):
            return
        return func(*args, **kwargs)
    
    wrapped._dont_interpret = getattr(func, '_dont_interpret', False)
    return wrapped

