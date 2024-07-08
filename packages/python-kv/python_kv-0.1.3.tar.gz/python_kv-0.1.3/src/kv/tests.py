from haskellian import either as E, Left
from dslog import Logger
from kv import KV

@E.do()
async def test(kv: KV[str], logger: Logger = Logger.click().prefix('[TEST]')):
  assert (await kv.keys().map(E.unsafe).sync()) == [], 'KV must be empty for testing'
  ok = True
  items = [('a', '1'), ('b', '2'), ('c', '3')]

  logger('Inserting items...')
  for k, v in items:
    (await kv.insert(k, v)).unsafe()
  logger('Inserted items OK')

  logger('Testing point read...')
  for k, v in items:
    if (r := (await kv.read(k)).unsafe()) != v:
      logger('Point read error. Expected:', v, 'Got:', r, level='ERROR')
      ok = False
  logger('Point read OK')

  logger('Testing keys...')
  keys = await kv.keys().map(E.unsafe).sync()
  if set(keys) != set(k for k, _ in items):
    logger('Keys error. Expected:', [k for k, _ in items], 'Got:', keys, level='ERROR')
    ok = False
  logger('Keys OK')

  logger('Testing point delete...')
  for k, _ in items:
    (await kv.delete(k)).unsafe()
    r = (await kv.read(k))
    if r.tag != 'left' or r.value.reason != 'inexistent-item':
      logger('Point delete error. Expected: Left("inexistent-item") Got:', r, level='ERROR')
      ok = False
  logger('Point delete OK')

  logger('Reinserting items...', level='DEBUG')
  for k, v in items:
    (await kv.insert(k, v)).unsafe()

  logger('Testing clear...')
  (await kv.clear()).unsafe()
  keys = await kv.keys().map(E.unsafe).sync()
  if keys != []:
    logger('Clear error. Expected: [] Got:', keys, level='ERROR')
    ok = False
  logger('Clear OK')

  if not ok:
    Left('Some tests failed').unsafe()