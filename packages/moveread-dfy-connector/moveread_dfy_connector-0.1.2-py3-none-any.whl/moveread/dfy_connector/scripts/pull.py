from argparse import ArgumentParser

def main():

  parser = ArgumentParser(description='DFY Puller')
  parser.add_argument('--sql', required=True, help='SQL connection string')
  parser.add_argument('--blob', required=True, help='DFY Blobs connection string')
  parser.add_argument('--pipeline', required=True, help='Pipeline endpoint')
  parser.add_argument('--token', required=True, help='Pipeline token')
  parser.add_argument('-n', '--max-games', default=None, type=int, help='Max games to pull')

  args = parser.parse_args()
  endpoint = args.pipeline.rstrip('/')

  from dslog import Logger
  logger = Logger.click().prefix('[PULLER]')
  logger(f'Pulling games to {endpoint}...')
  logger(f'- Max games: {args.max_games}')

  import asyncio
  from kv.api import KV
  from kv.rest import ClientKV
  from sqlmodel import create_engine, Session
  from pipeteer import http
  from moveread.dfy import queries
  from moveread.pipelines.dfy import DFYPipeline
  from moveread.dfy_connector import pull_games

  HEADERS = { 'Authorization': f'Bearer {args.token}' }
  req = http.bound_request(headers=HEADERS)
  pipe = DFYPipeline()
  Qpush, *_ = http.clients(pipe, f'{endpoint}/queues', request=req)
  blobs = ClientKV(f'{endpoint}/blobs', request=req)
  online_blobs = KV.of(args.blob)
  engine = create_engine(args.sql)

  with Session(engine) as s:
    uploaded = s.exec(queries.uploaded_games()).all()
    logger(f'Found {len(uploaded)} games')
    asyncio.run(pull_games(
      session=s, games=uploaded[:args.max_games],
      online_images=online_blobs, blobs=blobs,
      Qpush=Qpush, logger=logger
    ))