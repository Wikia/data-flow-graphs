def format_tsv_entry(source, edge, dest, weight, metadata=None):
    return '{}\t{}\t{}\t{:.4f}\t{}'.format(source, edge, dest, weight, metadata or '').strip()
