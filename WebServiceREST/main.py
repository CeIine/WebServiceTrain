from flask import Flask, request, jsonify,json
from flask_restx import Api, fields, Resource
from werkzeug.utils import cached_property
import sqlite3


app = Flask(__name__)
api = Api(app)

# Connexion à la base de données SQLite
conn=sqlite3.connect('RestDataBase.db',check_same_thread=False)
cur=conn.cursor()

# Définition des modèles pour les paramètres d'entrée et les réponses
search_model = api.model('SearchModel', {
    'param1': fields.String(required=True, description='Le gare de depart'),
    'param2': fields.String(required=True, description='Le gare d\'arrivée'),
    'param3': fields.String(required=True, description='Date et heure de depart'),
    'param4': fields.String(required=True, description='La classe de voyage') })
# Définition des modèles pour les paramètres d'entrée et les réponses
backsearch_model = api.model('backsearchModel', {
    'param1': fields.String(required=True, description='Le gare de depart'),
    'param2': fields.String(required=True, description='Le gare d\'arrivée'),
    'param4': fields.String(required=True, description='Date et heure de retour'),
    'param5': fields.String(required=True, description='La classe de voyage') })

booking_model = api.model('BookingModel', {
    'param1': fields.String(required=True, description='L\'ID du billet qu\'on veut reserver') })

# Définition de la classe pour la route '/Billets/Depart/<param1>/Arrive/<param2>/dateheureD/<param3>/dateheureA/<param4>/classe/<param5>'
@api.route('/BilletsAller/Depart/<param1>/Arrive/<param2>/dateheureD/<param3>/classe/<param4>')
class SearchTrain(Resource):
    @api.doc('Recherche de Train disponible pour l\'Aller')
    @api.expect(search_model)
    def get(self, param1, param2, param3, param4):
        '''Recherche de Train disponible pour l'Aller '''
         # Exécution de la requête SQL pour récupérer les données de la base de données
        cur.execute(f'Select Billet.trainId,Billet.prix,Billet.type,Billet.id from Trains,Billet where Trains.trainId = Billet.trainId and Billet.gareD="{param1}" and Billet.gareA="{param2}" and Billet.dateheureD="{param3}" and Billet.classe="{param4}" and Billet.reserve="False"')
        Billets=cur.fetchall()
        #print(Billets)
        # Renvoi de la réponse à l'utilisateur
        if not Billets:
            return jsonify('Aucun Train disponible')    
        else:
            Billets_json = []
            for Billet in Billets:
                #print(Billet)
                Billet_json = [
                    'trainId:' ,Billet[0],
                    'prix:' ,Billet[1],
                    'type:' ,Billet[2],
                    'IDReservation:' ,Billet[3],
                ]
                Billets_json.append(Billet_json)
        # Renvoi de la réponse à l'utilisateur
        return {'Mes Billets disponibles': Billets_json}

# Définition de la classe pour la route '/Billets/IDReservation/<param1>'
@api.route('/Billets/IDReservation/<param1>')
class BookingTrain(Resource):
    @api.doc('Reserver un Train')
    @api.expect(booking_model)
    def put(self, param1):
        '''Reserver un Train'''
          # Exécution de la requête SQL pour récupérer les données de la base de données
        cur.execute(f'Select id from Billet where reserve="False" and id="{param1}"')
        Billets=cur.fetchone()
        #print(Billets)
        # Renvoi de la réponse à l'utilisateur
        if Billets is None:
            return jsonify('False')
        else:
            cur.execute(f'Update Billet set reserve="True" where id="{param1}"')
            conn.commit()
            return jsonify('true')
        
# Définition de la classe pour la route '/Billets/Depart/<param1>/Arrive/<param2>/dateheureD/<param3>/dateheureA/<param4>/classe/<param5>'
@api.route('/BilletsRetour/Depart/<param1>/Arrive/<param2>/dateheureR/<param3>/classe/<param4>')
class TrainForBack(Resource):
    @api.doc('Recherche de train pour le retour')
    @api.expect(backsearch_model)
    def get(self, param1, param2, param3,param4):
        '''Recherche de Train disponible pour le retour '''
         # Exécution de la requête SQL pour récupérer les données de la base de données
        cur.execute(f'Select Billet.trainId,Billet.prix,Billet.type,Billet.id from Trains,Billet where Trains.trainId = Billet.trainId and Billet.gareD="{param1}" and Billet.gareA="{param2}" and Billet.dateheureD="{param3}" and Billet.classe="{param4}" and Billet.reserve="False"')
        BilletsR=cur.fetchall()
        #print(Billets)
        # Renvoi de la réponse à l'utilisateur
        if not BilletsR:
            return jsonify('Aucun Train disponible')    
        else:
            Billets_json = []
            for BilletR in BilletsR:
                #print(Billet)
                Billet_json = [
                    'trainId:' ,BilletR[0],
                    'prix:' ,BilletR[1],
                    'type:' ,BilletR[2],
                    'IDReservation:' ,BilletR[3],
                ]
                Billets_json.append(Billet_json)
        # Renvoi de la réponse à l'utilisateur
        return {'Mes Billets disponibles': Billets_json}
       

if __name__ == '__main__':
    app.run()


#print(search_Train("paris","marseille","2022-10-05 10:00:00","2022-10-05 15:00:00",1,"standard"))