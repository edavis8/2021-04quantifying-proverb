from gutenberg.acquire import get_metadata_cache

cache = get_metadata_cache()
cache.populate()


from gutenberg.query import list_supported_metadatas

f = open('./proverbs/metadata_list.txt', 'w')
f.write(str(list_supported_metadatas()))
f.close
