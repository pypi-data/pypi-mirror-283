from ..base import Base
from ...exceptions import NotFoundItemError

class BudgetViews(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/budget_views"

    def get(self, company_id, project_id, page=1, per_page=100):
        params = {
            "project_id": project_id,
            "page": page,
            "per_page": per_page
        }
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        views = self.get_request(
            api_url=f"{self.endpoint}",
            additional_headers=headers,
            params=params
        )
        return views

    def find(self, company_id, project_id, identifier):
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"
        for view in self.get(company_id=company_id, project_id=project_id):
            if view[key] == identifier:
                return view
        raise NotFoundItemError(f"Could not find view {identifier}")
