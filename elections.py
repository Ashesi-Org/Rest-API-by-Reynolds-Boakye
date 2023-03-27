# from https://pythonbasics.org/flask-rest-api/  

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/<int:student_id>', methods=['GET'])
def retrieve_voter(student_id):
    with open('./voters.txt', 'r') as f:
        data = f.read()
        if not data:
            return jsonify({'error': "text file is empty"}), 404
        voters = json.loads(data)
        for person in voters:
            if person['id'] == student_id:
                return jsonify(person)
        return jsonify({'error': "voter doesn't exist"}), 404

#create a new voter
@app.route('/', methods=['POST'])
def create_voter():
    voter = json.loads(request.data)
    found = False
    
    with open('./voters.txt', 'r') as f:
        data = f.read()
    if not data:
        voters = [voter]
    else:
        voters = json.loads(data)
        for each in voters:
            if each['id'] == voter['id']:
                found = True
                break
        voters.append(voter)
        
    if found:
        return f"{voter['id']} already exist in register", 404
    else:
        with open('./voters.txt', 'w') as f:
            f.write(json.dumps(voters, indent=2))
        return f"{voter['id']}'s record is added"

#update an existing voter
@app.route('/', methods=['PATCH'])
def update_voter_record():
    voter = json.loads(request.data)
    found = False
    changes = False
    
    with open('./voters.txt', 'r') as f:
        data = f.read()
        voters = json.loads(data)
    for id, person in enumerate(voters):
        if person['id'] == voter['id']:
            found = True
            # make the necessary changes only in the different information
            for key, value in voter.items():                
                if key not in person:
                    changes = True
                    person[key] = value     
                elif value != person[key]:
                    changes = True
                    person[key] = value
                    
            voters[id] = person
            break
        
    if found:
        if not changes:
            return f"{voter['id']}'s record is upto date"
            
        with open('./voters.txt', 'w') as f:
            f.write(json.dumps(voters, indent=2))
        return jsonify(person)
    
    return f"{voter['id']}'s record doesn't exist in register", 404
    
# delete a voter  
@app.route('/', methods=['DELETE'])
def delete_record():
    voter = json.loads(request.data)
    found = False
    with open('./voters.txt', 'r') as f:
        data = f.read()
        voters = json.loads(data)
        for id, person in enumerate(voters):
            if person['id'] == voter['id']:
                found = True    
                voters.pop(id)
                break
    with open('./voters.txt', 'w') as f:
        f.write(json.dumps(voters, indent=2))
        
    if found:
        return f"Voter deleted: {voter['id']}"
    
    return f"{voter['id']}'s record doesn't exist in register", 404


#for the election

#retrieve an election
@app.route('/election/<int:election_id>', methods=['GET'])
def retrieve_election(election_id):
    with open('./elections.txt', 'r') as f:
        data = f.read()
        if not data:
            return jsonify({'error': "text file is empty"}), 404
        elections = json.loads(data)
        for election in elections:
            if election['id'] == election_id:
                return jsonify(election)
        return jsonify({'error': "This election doesn't exist"}), 404

#create a new election
@app.route('/election', methods=['POST'])
def create_election():
    election = json.loads(request.data)
    found = False
    
    with open('./elections.txt', 'r') as f:
        data = f.read()
    if not data:
        elections = [election]
    else:
        elections = json.loads(data)
        for each in elections:
            if each['id'] == election['id']:
                found = True
                break
        elections.append(election)
        
    if found:
        return f"{election['id']} already exist", 404
    else:
        with open('./elections.txt', 'w') as f:
            f.write(json.dumps(elections, indent=2))
        return f"{election['title']} ({election['id']}) is added"

# delete an election  
@app.route('/election', methods=['DELETE'])
def delete_election():
    election = json.loads(request.data)
    new_elections = []
    found = False
    with open('./elections.txt', 'r') as f:
        data = f.read()
        elections = json.loads(data)
        for id,each in enumerate(elections):
            if each['id'] == election['id']:
                found = True
                deleted = elections.pop(id)
                break
    with open('./elections.txt', 'w') as f:
        f.write(json.dumps(elections, indent=2))
        
    if found:
        return f"Election deleted: {deleted['title']} ({deleted['id']})"
    
    return f"({election['id']})'s doesn't exist", 404

# registers a voter to vote in an election
@app.route('/election', methods=['LINK'])
def vote_in_election():
    election_id = json.loads(request.data)['election']
    voter_id = json.loads(request.data)['voter']

    with open('./elections.txt', 'r') as f:
        found = False
        data = f.read()
        if not data:
            return "No election set up", 404
        elections = json.loads(data)
        for each in elections:
            if election_id == each['id']:
                found = True
                break
                
        if not found:
            return f"{election_id} not found", 404
         
    with open('./voters.txt', 'r') as f:
        found = False
        data = f.read()
        if not data:
            return "No voter in register", 404
        voters = json.loads(data)
        for each in voters:
            if voter_id == each['id']:
                found = True
                break
        
        if not found:
            return f"{voter_id} not found", 404
            
    with open('./voting_in_election.txt', 'r') as f:
        changes = False
        data = f.read()
        if not data:
            changes = True
            voter_election = [
                                {
                                    "election_id": election_id,
                                    "voters": [voter_id],
                                    "total_voters": 1
                                }
                            ] 
        else:
            voter_election = json.loads(data)
            
            for election in voter_election:
                if election['election_id'] == election_id :
                    all_voters = election['voters']
                    if voter_id not in all_voters:
                        changes = True
                        all_voters.append(voter_id)
                        election['total_voters'] += 1
            
            
    if not changes:
        return "Election data is upto date", 404
    else:
        with open('./voting_in_election.txt', 'w') as f:
            f.write(json.dumps(voter_election, indent=4))
        return voter_election
    

app.run(debug=True)

