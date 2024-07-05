from typing import Callable, Any, Coroutine
import azure.functions as func
from haskellian import promise as P
from dslog import Logger

def job(
  app: func.FunctionApp, name: str, *,
  route: str, timer: str, logger: Logger = Logger.stdlib(),
  run_on_startup: bool = False
):
  """Registers a job both as a timer and an HTTP trigger."""
  def decorator(job: Callable[[], Any | Coroutine]):
    @app.route(route)
    async def http_trigger(req):
      try:
        await P.wait(job())
      except Exception as e:
        logger(f'HTTP trigger for job "{name}" failed: {e}', level='ERROR')
        raise e
      return func.HttpResponse(status_code=200)
      
    @app.timer_trigger('timer', timer, run_on_startup=run_on_startup)
    async def timer_trigger(timer: func.TimerRequest):
      try:
        await P.wait(job())
      except Exception as e:
        logger(f'Timer trigger for job "{name}" failed: {e}', level='ERROR')
        raise e
  return decorator
    