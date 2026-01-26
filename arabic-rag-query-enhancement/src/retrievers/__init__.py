# Lazy imports to avoid unnecessary dependencies
# Only import what's actually used

def __getattr__(name):
    if name == 'mDPRRetriever':
        from .dense import mDPRRetriever
        return mDPRRetriever
    elif name == 'BM25SRetriever':
        from .bm25 import BM25SRetriever
        return BM25SRetriever
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ['mDPRRetriever', 'BM25SRetriever']
