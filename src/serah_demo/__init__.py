"""serah_demo — public demonstration package for the Serah evidence-packet pipeline.

This package demonstrates the packet validation, building, and reporting pipeline
using entirely synthetic data. It has no network access, no brokerage connection,
and no capability to place, draft, or submit financial orders.

All fixture data uses the fictional symbol SYNT-X. No output from this package
constitutes or resembles a real financial recommendation.
"""

__version__ = "1.0.0"
__all__ = ["models", "validator", "packet_builder", "report_builder", "demo"]
