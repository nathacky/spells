import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def batch_get_values(spreadsheet_id, _range_names):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    range_names = [_range_names]

    result = (
        service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=spreadsheet_id, ranges=range_names)
        .execute()
    )
    ranges = result.get("valueRanges", [])
    print(f"{len(ranges)} ranges retrieved")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


if __name__ == "__main__":
  # Pass: spreadsheet_id, and range_name

  data=batch_get_values("181HSGUgQiEizIjeZw2490CyevWEPCCPK7NMB4vO5Dh8", "Sheet1!E2:E")
  print(data["valueRanges"][0]["values"])

