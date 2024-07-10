from ..base import Base
from ...exceptions import NotFoundItemError

class BudgetRows(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/budget_views"

    def get_budget_rows(self, company_id, project_id, budget_view_id):
        params = {
            "project_id": project_id,
            "budget_row_type": "all"
        }
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        rows = self.get_request(
            api_url=f"{self.endpoint}/{budget_view_id}/detail_rows",
            additional_headers=headers,
            params=params
        )
        return rows

    def find_budget_row(self, company_id, project_id, budget_view_id, identifier):
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "cost_code"
        for row in self.get_budget_rows(company_id=company_id, project_id=project_id, budget_view_id=budget_view_id):
            if row[key] == identifier:
                return row
        raise NotFoundItemError(f"Could not find row {identifier}")
