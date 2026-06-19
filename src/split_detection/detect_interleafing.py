def detect_interleafing(log):
    directly_follows_relations = log.get_directly_follows_relations_by_label()

    return False