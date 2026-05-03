from flask import Blueprint, request, jsonify

services_bp = Blueprint('services', __name__)

# Mock database of arrested persons for the "Arrest Details" service
# In a real system, this would query a dedicated 'arrests' table in Supabase
MOCK_ARRESTS = [
    { "id": "AR202401", "name": "Rahul Sharma", "age": 32, "district": "Chennai", "offense": "Commercial Fraud", "date": "2024-03-25", "status": "In Custody" },
    { "id": "AR202402", "name": "Anish Kumar", "age": 28, "district": "Madurai", "offense": "Aggravated Assault", "date": "2024-04-01", "status": "Judicial Remand" },
    { "id": "AR202403", "name": "Priya Das", "age": 35, "district": "Coimbatore", "offense": "Cyber Theft", "date": "2024-04-05", "status": "Bail Refused" },
    { "id": "AR202404", "name": "Suresh Mani", "age": 41, "district": "Chennai", "offense": "Public Nuisance", "date": "2024-03-30", "status": "In Custody" },
    { "id": "AR202405", "name": "Vikram R", "age": 24, "district": "Trichy", "offense": "Drug Possession", "date": "2024-04-02", "status": "In Custody" },
    { "id": "AR202406", "name": "Karthik Raj", "age": 30, "district": "Salem", "offense": "Traffic Offense", "date": "2024-04-07", "status": "Released on Bail" }
]

@services_bp.route('/arrests', methods=['GET'])
def get_arrests():
    name_query = request.args.get('name', '').lower()
    district_query = request.args.get('district', '')
    
    filtered = MOCK_ARRESTS
    if name_query:
        filtered = [a for a in filtered if name_query in a['name'].lower()]
    if district_query:
        filtered = [a for a in filtered if a['district'] == district_query]
        
    return jsonify(filtered), 200
