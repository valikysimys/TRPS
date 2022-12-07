from python_loc_counter import LOCCounter

path = "./venv/Lib/site-packages/numpy/__init__.pyi"

counter = LOCCounter(path)

print(f'Total lines:{counter.getTotalLineCountLOC()}')
print(f'Comment lines:{counter.getTotalCommentsLOC()}')
print(f'Blank lines:{counter.getBlankLinesLOC()}')
print(f'Source lines:{counter.getSourceLOC()}')
print(f'Comment to lines ratio:{counter.getTotalCommentsLOC()/counter.getTotalLineCountLOC()}')

