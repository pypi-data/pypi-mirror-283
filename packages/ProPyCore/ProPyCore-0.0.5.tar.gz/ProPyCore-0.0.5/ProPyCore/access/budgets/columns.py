from ..base import Base
from ...exceptions import NotFoundItemError

class BudgetColumns(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/budget_views"

    def get(self, company_id, project_id, budget_view_id):
        params = {
            "project_id": project_id
        }
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        columns = self.get_request(
            api_url=f"{self.endpoint}/{budget_view_id}/budget_detail_columns",
            additional_headers=headers,
            params=params
        )
        return columns

    def find(self, company_id, project_id, budget_view_id, identifier):
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"
        for column in self.get(company_id=company_id, project_id=project_id, budget_view_id=budget_view_id):
            if column[key] == identifier:
                return column
        raise NotFoundItemError(f"Could not find column {identifier}")
