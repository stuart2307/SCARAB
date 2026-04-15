from rapidfuzz import process, utils

name="MARIO_ALLSTARS+WORLD"
candidates=["Super Mario All-Stars", "Super Mario All-Stars", "Super Mario All-Stars and Super Mario World"]
match = process.extractOne(name, candidates, processor=utils.default_process)
print(match)