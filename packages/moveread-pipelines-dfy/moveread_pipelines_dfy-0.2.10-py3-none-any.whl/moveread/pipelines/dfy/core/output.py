from typing import Sequence, NamedTuple
from haskellian import iter as I, either as E, promise as P
from kv import KV, ReadError
from moveread.pipelines.preprocess import Output as PreOutput
from moveread.core import Core, Game, Player, Sheet, Image, StylesNA
from ..spec import Output

def output_sheet(preprocessed: PreOutput, model: str) -> tuple[Sheet, Sequence[str]]:
  og = preprocessed.original
  corr = preprocessed.corrected
  images = [
    Image(url=og.img, meta=og.meta),
    Image(url=corr.img, meta=corr.meta),
  ]
  return Sheet(images=images, meta=Sheet.Meta(model=model)), [og.img, corr.img]


def output_game(key: str, out: Output):
  ann = out.annotations[0]
  styles = StylesNA(pawn_capture=ann.pawn_capture, piece_capture=ann.piece_capture)
  sheets, nested_imgs = I.unzip(output_sheet(img, out.model) for img in out.preprocessed_imgs)
  imgs = I.flatten(nested_imgs).sync()

  game = Game(
    meta=Game.Meta(pgn=out.pgn, early=out.early, tournament=out.gameId),
    players=[Player(
      meta=Player.Meta(language=ann.lang, end_correct=ann.end_correct, styles=styles),
      sheets=sheets
    )]
  )

  return game, imgs

@E.do[ReadError]()
async def output_one(
  core: Core, key: str, out: Output, *, images: KV[bytes]
):
  game, imgs = output_game(key, out)
  tasks = [images.copy(url, core.blobs, url) for url in imgs]
  E.sequence(await P.all(tasks)).unsafe()
  (await core.games.insert(key, game)).unsafe()