from typing import Callable
import logging
import azure.functions as func

def safe(make: Callable[[], func.FunctionApp]):
  try:
    return make()
  except Exception as e:
    logging.error(e)

    app = func.FunctionApp(func.AuthLevel.ANONYMOUS)

    @app.route('health')
    def health(req):
      logging.error('Health Check Failed: ' + str(e))
      return func.HttpResponse('Error Creating App', status_code=500)