from typing import Callable, ParamSpec, TypeVar, overload, Coroutine
from functools import wraps
import inspect
import logging
import azure.functions as func

Ps = ParamSpec('Ps')
T = TypeVar('T')

def startup(make: Callable[[], func.FunctionApp], *, error_message: Callable[[Exception], str] = lambda _: 'Service is down'):
  """Tries to create the app. Otherwise sets up a `/health` route to trigger logging of the startup exception"""
  exc = None
  try:
    return make()
  except Exception as e:
    logging.error(e)
    exc = e

    app = func.FunctionApp(func.AuthLevel.ANONYMOUS)

    @app.route('health')
    def health(req):
      logging.error('Startup error: ' + str(exc))
      return func.HttpResponse(error_message(exc), status_code=500)
    
    return app
  

def function(name: str):
  @overload
  def decorator(f: Callable[Ps, Coroutine[T, None, None]]) -> Callable[Ps, Coroutine[T, None, None]]: ...
  @overload
  def decorator(f: Callable[Ps, T]) -> Callable[Ps, T]: ...
  def decorator(f): # type: ignore
    if inspect.iscoroutinefunction(f):
      @wraps(f)
      async def _awrapper(*args: Ps.args, **kwargs: Ps.kwargs):
        try:
          return await f(*args, **kwargs)
        except Exception as e:
          logging.error(f'Error running "{name}": {e}')
          raise e
      return _awrapper
    else:
      @wraps(f)
      def _wrapper(*args: Ps.args, **kwargs: Ps.kwargs):
        try:
          return f(*args, **kwargs)
        except Exception as e:
          logging.error(f'Error running "{name}": {e}')
          raise e
    return _wrapper
  return decorator
    