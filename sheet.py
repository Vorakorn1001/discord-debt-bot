from auth import spreadsheet_service
from auth import drive_service

class GoogleSheetsAPI:
    def __init__(self):
        self.spreadsheet_id = None        

    def create_spreadsheet(self, title, email="vorakorn.ko@gmail.com"):
        spreadsheet_details = {
            'properties': {
                'title': title
            }
        }
        sheet = spreadsheet_service.spreadsheets().create(body=spreadsheet_details,
                                                          fields='spreadsheetId').execute()
        sheet_id = sheet.get('spreadsheetId')
        permission1 = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': f'{email}'
        }
        drive_service.permissions().create(fileId=sheet_id, body=permission1).execute()
        self.spreadsheet_id = sheet_id
        return sheet_id

    def use_spreadsheet(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        members = self.read_range('อู๋!A1:Z1')[0][1:]
        self.members = members

    def read_range(self, range_name):
        result = spreadsheet_service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        return rows

    def write_range(self, range_name, values):
        value_input_option = 'USER_ENTERED'
        body = {
            'values': values
        }
        result = spreadsheet_service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()

    def read_cell_value(self, range_name='B1:B1'):
        result = spreadsheet_service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        
        if not values:
            print('No data found in the specified range.')
            return None
        
        # Assuming there's only one value in the retrieved range (A1:A1)
        cell_value = values[0][0]
        return cell_value
    
    def append_row(self, values, range_name='Sheet1'):
        value_input_option = 'USER_ENTERED'
        body = {
            'values': [values]
        }
        result = spreadsheet_service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))
    
    def create_debt(self, borrower, lender, amount, description):
        index = self.members.index(lender) + 1
        values = [description] + ['' for _ in range(len(self.members))]
        values[index] = amount
        self.append_row(values, range_name=f'{borrower}!A:F')
        
    def create_log(self, borrower: str, lender: str, amount: float, description: str, lender_action: bool):
        values = [
            lender if lender_action else borrower, borrower, lender, amount, description
        ]
        self.append_row(values, "log!A:E")