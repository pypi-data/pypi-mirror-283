from haskellian import Either
from chess_pairings import GroupPairings, RoundPairings
from chess_scraping import Source, ScrapingError, chess_results as cr, chess_manager as cm, info64

async def scrape_group(src: Source) -> Either[ScrapingError, GroupPairings]:
  if src.tag == 'chess-results':
    return await cr.scrape_group(src.id)
  elif src.tag == 'chess-manager':
    return await cm.scrape_group(src.id)
  elif src.tag == 'info64':
    return await info64.scrape_group(src.id)
  else:
    raise ValueError(f'Unknown scraping source: {src.tag}')
  
async def scrape_round(src: Source, round: str | int) -> Either[ScrapingError, RoundPairings]:
  if src.tag == 'chess-results':
    return await cr.scrape_round(src.id, round)
  elif src.tag == 'chess-manager':
    return await cm.scrape_round(src.id, round)
  elif src.tag == 'info64':
    return await info64.scrape_round(src.id, round)
  else:
    raise ValueError(f'Unknown scraping source: {src.tag}')