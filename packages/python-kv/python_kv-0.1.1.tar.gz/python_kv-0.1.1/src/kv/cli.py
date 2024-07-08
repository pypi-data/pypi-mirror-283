import typer

app = typer.Typer()

@app.callback()
def callback(debug: bool = typer.Option(False, '--debug', help='Enable debug mode')):
  if debug:
    import debugpy
    debugpy.listen(5678)
    print('Waiting for debugger attach...')
    debugpy.wait_for_client()

@app.command()
def test(conn_str: str):
  """Performs some basic tests on `KV.of(conn_str)`"""
  import asyncio
  from kv import KV
  from kv.tests import test
  kv = KV.of(conn_str, str)
  async def run():
    e = await test(kv)
    if e.tag == 'left':
      print('ERROR RUNNING TESTS:\n', e.value)
      raise typer.Exit(code=1)
  asyncio.run(run())

def parse_type(type: str):
  if type == 'dict':
    return dict
  if type == 'list':
    return list
  if type == 'set':
    return set
  if type == 'str':
    return str
  if type == 'int':
    return int
  if type == 'float':
    return float
  if type == 'bool':
    return bool
  if type == 'bytes':
    return None
  raise ValueError(f'Invalid type: {type}')

@app.command()
def serve(
  conn_str: str = typer.Argument(..., help='KV connection string'),
  token: str = typer.Option('', '--token', help='Bearer token for authorization'),
  host: str = typer.Option('0.0.0.0', '--host'),
  port: int = typer.Option(8000, '-p', '--port'),
  type: str = typer.Option('bytes', '--type', help='Datatype. Supports: dict, list, set, str, int, float, bool, bytes (default)'),
):
  from kv import http, KV
  import uvicorn

  t = parse_type(type)
  print('Starting API with type:', type)
  kv = KV.of(conn_str, type=t)
  app = http.api(kv, type=t, token=token or None)

  uvicorn.run(app, host=host, port=port)