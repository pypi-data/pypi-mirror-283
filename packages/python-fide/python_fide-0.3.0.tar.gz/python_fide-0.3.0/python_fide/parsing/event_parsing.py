from typing import Dict, Optional

from python_fide.parsing.common_parsing import detect_client_error
from python_fide.types.core import FideEventDetail
from python_fide.types.adapters import PartialDictAdapter

def event_detail_parsing(response: Dict[str, dict]) -> Optional[FideEventDetail]:
    """
    Logic to parse the response returned from the event
    detail endpoint.

    Args:
        response (Dict[str, Any]): A dictionary representation
            of the JSON response.

    Returns:
        FideEventDetail | None: A FideEventDetail object or if
            there was no results, None.
    """
    # This is a search by Fide ID, thus there should never
    # be a response that has more than one item, although
    # there can be a response with no items
    no_results = detect_client_error(response=response)

    if no_results:
        return
    else:
        partial_adapter = PartialDictAdapter.model_validate(response)
        fide_detail = FideEventDetail.from_validated_model(
            record=partial_adapter.data
        )
        return fide_detail