from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')  # read CSV
        data = data.to_dict() 
        return {'data': data}, 200  

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('A', required=True)  # add args
        parser.add_argument('B', required=True)
        parser.add_argument('C', required=True)
        
        args = parser.parse_args()  # parse arguments to dictionary
        
        # create new dataframe containing new values
        new_data = pd.DataFrame({
            'A': args['A'],
            'B': args['B'],
            'C': args['C'],
        })
        # read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists."
            }, 401
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': [[]]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK


api.add_resource(Users, '/users') 

if __name__ == '__main__':
    app.run()