from flask import Flask, jsonify, request, send_from_directory, abort
import os, json, shutil
from flask_cors import CORS
from werkzeug.utils import secure_filename


app = Flask(__name__)

CORS(app)

app.config['ALLOWED_FILE_EXTENSIONS'] = ['JPEG', 'JPG', 'PNG', 'GIF', 'MP4', 'MP3', 'WMV', 'DWG', 'DXF', 'XSLX', 'CSV', 'PDF']
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False





#  [A D M I N S]  [A D M I N S]  [A D M I N S]  [A D M I N S]  [A D M I N S]  [A D M I N S]  [A D M I N S]

@app.route("/api/v1/admins", methods=["GET", "POST"])
def admins_manage():

    path = os.path.join("static", "admins.json")
    body = request.json

    if request.method == "GET":
        
        if os.path.exists(path):
            with open(path, "r") as file:

                admins = json.load(file)
                return jsonify({"admins": admins, "message": "Admins database loaded successfully", "status": "200 OK"})

        return jsonify({"admins": [], "message": "Admins database empity", "status": "204 NO CONTENT"})



    if request.method == "POST":

        if not os.path.exists(path):
            with open(path, "w") as file:
                admins = []
                admins.append(body)
                file.write(json.dumps(admins, indent = 4))
                return jsonify({"admin": body, "message": "Admin successfully registered", "status": "201 CREATED"})

        else:

            with open(path, "r+") as file:
                admins = json.load(file)

                if any(admin['adminID'] == body['adminID'] for admin in admins):
                    return jsonify({"admin": body['adminID'], "message": "The adminID already exists", "status": "304 NOT MODIFED"})

                elif any(admin['email'] == body['email'] for admin in admins):
                    return jsonify({"email": body['email'], "message": "This email is in use", "status": "304 NOT MODIFED"}) 

                else:  
                    admins.append(body)  
                    file.seek(0)
                    json.dump(admins, file, indent = 4)
                    return jsonify({"admin": body, "message": "Admin successfully registered", "status": "201 CREATED"})

                    

#  [A D M I N S  -  P A T H   V A R I A B L E]  [A D M I N S  -  P A T H   V A R I A B L E]   [A D M I N S  -  P A T H   V A R I A B L E]   

@app.route("/api/v1/admins/<adminID>", methods=["GET", "PUT"])
def edit_admins(adminID):

    path = os.path.join("static", "admins.json")
    body = request.json

    if request.method == "GET":

        if os.path.exists(path):
            with open(path, "r") as file:
                admins_list = json.load(file)

                if any(admin['adminID'] == adminID for admin in admins_list):
                    for admin in admins_list:

                        if admin['adminID'] == adminID:
                            return jsonify({"admin": admin, "message": "Admin loaded successfully", "status": "200 OK"})
             
                return jsonify({"admin": adminID, "message": "The admin not exists", "status": "204 NO CONTENT"})

        return jsonify({"admins_list": [], "message": "Admins database empity", "status": "204 NO CONTENT"}) 
                    


    if request.method == "PUT":
        
            if os.path.exists(path):
                with open(path, "r+") as file:
                    admins = json.load(file)

                    if any(admin["adminID"] == body["adminID"] and admin["adminID"] == adminID for admin in admins):

                        for admin in admins:
                            if admin["adminID"] == body["adminID"]:
                                admins.remove(admin)
                                admins.append(body)
                                
                                with open(path, "w") as file:

                                    file.write(json.dumps(admins, indent = 4))
                                    return jsonify({"admin": body, "message": "Admin data updated", "status": "200 OK"})
                 
                    return jsonify({"admin": adminID, "message": "The admin not exists", "status": "304 NOT MODIFED"})

            return jsonify({"admins_list": [], "message": "Admin database empity", "status": "204 NO CONTENT"})



# [C L I E N T S]  [C L I E N T S]  [C L I E N T S]  [C L I E N T S]  [C L I E N T S]  [C L I E N T S]  [C L I E N T S] 


@app.route("/api/v1/clients", methods=["GET", "POST"])
def clients_manage():

    path = os.path.join('static', 'clients.json')
    body = request.json

    if request.method == "GET":

        if os.path.exists(path):
            with open(path, "r") as file:
                clients = json.load(file)
                return jsonify({"clients": clients, "message": "Clients database loaded successfully", "status": "200 OK"})

        return jsonify({"clients": [], "message": "Clients database empity", "status": "204 NO CONTENT"})



    if request.method == "POST":
        
        if not os.path.exists(path):
            with open(path, "w") as file:

                clients = []
                clients.append(body)
                file.write(json.dumps(clients, indent = 4))
                return jsonify({"client": body, "message": "Client successfully registered", "status": "201 CREATED"})

        else:
            with open(path, "r+") as file:
                clients = json.load(file)

                if any(client["clientID"] == body["clientID"] for client in clients):
                    return jsonify({"client": body["clientID"], "message": "The clientID already exists", "status": "304 NOT MODIFED"})

                elif any(client["email"] == body["email"] for client in clients):
                    return jsonify({"email": body["email"], "message": "This email is in use", "status": "304 NOT MODIFED"}) 

                else:  
                    clients.append(body)  
                    file.seek(0)
                    json.dump(clients, file, indent = 4)
                    return jsonify({"client": body, "message": "Client successfully registered", "status": "201 CREATED"})



#  [C L I E N T S - P A T H  V A R I A B L E]  [C L I E N T S - P A T H  V A R I A B L E]  [C L I E N T S - P A T H  V A R I A B L E]


@app.route("/api/v1/clients/<clientID>", methods=["GET", "PUT", "DELETE"])
def edit_clients(clientID):

    path = os.path.join('static', 'clients.json')
    body = request.json

    if request.method == "GET":

        if os.path.exists(path):
            with open(path, "r") as file:
                clients = json.load(file)

                if any(client['clientID'] == clientID for client in clients):

                    for client in clients:
                        if client['clientID'] == clientID:
                            return jsonify({"client": client, "message": "Client loaded successfully", "status": "200 OK"})

                return jsonify({"client": clientID, "message": "The clientID not exists", "status": "204 NO CONTENT"})

        return jsonify({"clients": [], "message": "Clients database empity", "status": "204 NO CONTENT"}) 



    if request.method == "PUT":
  
        if os.path.exists(path):
            with open(path, "r+") as file:
                clients = json.load(file)

                if any(client['clientID'] == body['clientID'] and client['clientID'] == clientID for client in clients):

                    for client in clients:
                        if client['clientID'] == body['clientID']:
                            clients.remove(client)
                            clients.append(body)

                            with open(path, "w") as file:
                                file.write(json.dumps(clients, indent = 4))
                                return jsonify({"client": body, "message": "Client data updated", "status": "200 OK"})

                return jsonify({"client": clientID, "message": "The clientID not exists", "status": "304 NOT MODIFED"})

        return jsonify({"clients_list": [], "message": "Clients database empity", "status": "204 NO CONTENT"})



    if request.method == "DELETE":

        if os.path.exists(path):
            with open(path, "r+") as file:
                clients = json.load(file)
              
                for client in clients:
                    if client['clientID'] == clientID:

                        clients.remove(client)

                        with open(path, "w") as file:

                            file.write(json.dumps(clients, indent = 4))
                            return jsonify({"client": clientID, "message": "Client deleted successfully", "status": "200 OK"})

                return jsonify({"client": clientID, "message": "The clientID not exists", "status": "304 NOT MODIFED"})

        return jsonify({"clients": [], "message": "Clients database empity", "status": "204 NO CONTENT"})



#  [P R O Y E C T S]  &&    [P R O Y E C T S - P A R A M S]

@app.route("/api/v1/proyects", methods=["GET", "POST"])
def proyects_manage():

    path = os.path.join('static', 'proyects')
    json_path = os.path.join('static', 'proyects.json')
    
    if request.method == "GET":

        if request.args.get('client') is None  and  request.args.get('admin') is None:

            if os.path.exists(path) and os.path.exists(json_path):              
                with open(json_path, "r") as file:
                    proyects = json.load(file)
                    return jsonify({"proyects": proyects, "message": "Proyects database loaded sucessfully", "status": "200 OK"})

            return jsonify({"proyects": [], "message": "Proyects database empity", "status": "204 NO CONTENT"})

        else:
            #/api/v1/proyects?admin=<adminID>
            adminID = request.args.get('admin')
            clientID = request.args.get('client')

            if os.path.exists(json_path):
                
                with open(json_path, "r") as file:
                    proyects = json.load(file)
                    new_proyects_list = []

                    if adminID is not None:

                        if any(proyect["admin"] == adminID for proyect in proyects):

                            for proyect in proyects:
                                if proyect['admin'] == adminID:
                                    new_proyects_list.append(proyect)

                            return jsonify({"proyects": new_proyects_list, "admin": adminID, "message": "Proyects database loaded sucessfully", "status": "200 OK"})

                        return jsonify({"admin": adminID, "message": "This admin has no projects", "status": "204 NO CONTENT"})


                    elif clientID is not None:
                        if any(proyect["client"] == clientID for proyect in proyects):

                            for proyect in proyects:
                                if proyect['client'] == clientID:
                                    new_proyects_list.append(proyect)

                            return jsonify({"proyects": new_proyects_list, "client": clientID, "message": "Proyects database loaded sucessfully", "status": "200 OK"})

                        return jsonify({"admin": clientID, "message": "This client has no projects", "status": "204 NO CONTENT"})

            return jsonify({"proyects": [], "message": "Proyects database empity", "status": "204 NO CONTENT"})



    if request.method == "POST":
        
        path = os.path.join('static', 'proyects')
        body = request.json
        nameproyect = body['name']

        if not os.path.exists(path):
            os.mkdir(path)
            path = os.path.join(path, nameproyect)

            if not os.path.exists(path):
                os.mkdir(path)
                os.mkdir(os.path.join(path, 'ideas'))
                os.mkdir(os.path.join(path, 'doc'))
                os.mkdir(os.path.join(path, 'anteproyecto'))
                os.mkdir(os.path.join(path, 'avances'))
                os.mkdir(os.path.join(path, 'legajo'))
                os.mkdir(os.path.join(path, 'obra'))

                json_path = os.path.join('static', 'proyects.json')
                if not os.path.exists(path):

                    with open(json_path, "w") as file:
                        proyects = []
                        proyects.append(body)
                        file.write(json.dumps(proyects, indent = 4))
                        return jsonify({"proyect": body, "path": path, "message": "Proyect successfully saved", "status": "201 CREATED"})

                else:
                    with open(json_path, "r+") as file:
                        proyects = json.load(file)

                        if any(proyect["name"] == body["name"] for proyect in proyects):
                            return jsonify({"name": nameproyect, "message": "Proyect name already exists", "status": "304 NOT MODIFED"})

                        else:  
                            proyects.append(body)  
                            file.seek(0)
                            json.dump(proyects, file, indent = 4)
                            return jsonify({"proyect": body, "path": path, "message": "Proyect created succefully", "status": "201 CREATED"})

            return jsonify({"name": nameproyect, "message": "Proyect name already exists", "status": "304 NOT MODIFED"})


        else:
            path = os.path.join(path, nameproyect)

            if not os.path.exists(path):
                os.mkdir(path)
                os.mkdir(os.path.join(path, 'ideas'))
                os.mkdir(os.path.join(path, 'doc'))
                os.mkdir(os.path.join(path, 'anteproyecto'))
                os.mkdir(os.path.join(path, 'avances'))
                os.mkdir(os.path.join(path, 'legajo'))
                os.mkdir(os.path.join(path, 'obra'))

                json_path = os.path.join('static', 'proyects.json')
                if not os.path.exists(path):

                    with open(json_path, "w") as file:
                        proyects = []
                        proyects.append(body)
                        file.write(json.dumps(proyects, indent = 4))
                        return jsonify({"name": body, "path": path, "message": "Proyect successfully saved", "status": "201 CREATED"})
                        
                else:
                    with open(json_path, "r+") as file:
                        proyects = json.load(file)

                        if any(proyect["name"] == body["name"] for proyect in proyects):
                            return jsonify({"proyect": body["name"], "message": "Proyect name already exists", "status": "304 NOT MODIFED"})

                        else:  
                            proyects.append(body)  
                            file.seek(0)
                            json.dump(proyects, file, indent = 4)
                            return jsonify({"proyect": body, "path": path, "message": "Proyect created succefully", "status": "201 CREATED"})

            return jsonify({"proyect": nameproyect, "path": path, "message": "Proyect name already exists", "status": "304 NOT MODIFED"})




#  [P R O Y E C T S -  P A T H   V A R I A B L E]  [P R O Y E C T S -  P A T H   V A R I A B L E] 

@app.route("/api/v1/proyects/<proyectID>", methods=["GET", "PUT", "DELETE"])
def admin_proyect(proyectID):

    path = os.path.join('static', 'proyects.json')
    body = request.json

    if request.method == "GET":

        if os.path.exists(path):
            with open(path, "r") as file:
                proyects = json.load(file)

                if any(proyect['name'] == proyectID for proyect in proyects):

                    for proyect in proyects:
                        if proyect['name'] == proyectID:
                            return jsonify({"proyect": proyect, "message": "Proyect loaded successfully", "status": "200 OK"})
             
                return jsonify({"proyect": proyectID, "message": "The proyect not exists", "status": "204 NO CONTENT"})

        return jsonify({"proyects": [], "message": "Proyects database empity", "status": "204 NO CONTENT"})

             

    if request.method == "PUT":
  
        if os.path.exists(path):
            with open(path, "r+") as file:
                proyects = json.load(file)

                if any(proyect['name'] == proyectID  for  proyect in proyects):

                    for proyect in proyects:
                        if proyect['name'] == proyectID:
                            proyects.remove(proyect)
                            proyects.append(body)

                            with open(path, "w") as file:
                                file.write(json.dumps(proyects, indent = 4))

                                path = os.path.join('static', 'proyects', proyectID)
                                if os.path.exists(path):

                                    newName = body['name']
                                    newPath = os.path.join('static', 'proyects', newName)
                                    os.rename(path, newPath)
                                    return jsonify({"proyect": body, "message": "Proyect data updated", "status": "200 OK"})

                                return jsonify({"proyect": proyectID, "message": "The proyectID not exists", "status": "304 NOT MODIFED"})

                return jsonify({"proyect": proyectID, "message": "The proyectID not exists", "status": "304 NOT MODIFED"})

        return jsonify({"proyects_list": [], "message": "Proyects database empity", "status": "204 NO CONTENT"})



    if request.method == "DELETE":

        path = os.path.join('static', 'proyects.json')

        if os.path.exists(path):
            with open(path, "r+") as file:
                proyects = json.load(file)

                if any(proyect["name"] == proyectID for proyect in proyects):

                    for proyect in proyects:
                        if proyect["name"] == proyectID:
                            proyects.remove(proyect)

                            with open(path, "w") as file:
                                file.write(json.dumps(proyects, indent = 4))

                                path = os.path.join('static', 'proyects', proyectID)
                                if os.path.exists(path):
                                    shutil.rmtree(path, ignore_errors=True)
                                    return jsonify({"proyect": proyectID, "message": "Proyect deleted successfully", "status": "200 OK"})

                                return jsonify({"proyect": proyectID, "message": "The proyectID not exists", "status": "304 NOT MODIFED"})

                return jsonify({"proyect": proyectID, "message": "The proyectID not exists", "status": "304 NOT MODIFED"})

        return jsonify({"proyects_list": [], "message": "Proyects database empity", "status": "304 NOT MODIFED"})




#  [F I L E S   U P L O A D]  [F I L E S   U P L O A D]  [F I L E S   U P L O A D]  [F I L E S   U P L O A D]


@app.route("/api/v1/upload-file/<proyect>/<section>", methods=["GET", "POST"])
def upload_file(proyect, section):
    
    path = os.path.join('static', 'proyects', proyect, section)

    if request.method == "POST":

        if os.path.exists(path):
            if request.files:
                file = request.files["file"]
                filename = file.filename

                if filename == "":
                    return jsonify({'message': 'Unnamed file', 'status': '304 NOT MODIFED'})

                listdir = os.listdir(path)
                if any(file == filename for file in listdir):
                    return jsonify({'message': 'The file name already exist', 'status': '304 NOT MODIFED'})
                    
                if allowed_file(filename):
                    filename = secure_filename(filename)
                    file.save(os.path.join(path, filename))
                    return jsonify({'file': filename, 'path': os.path.join(path, filename), 'message': 'File saved successfully', 'status': '201 CREATED'})

                return jsonify({'message': 'That file extension is not allowed', 'status': 'BAD REQUEST	400'})

            return jsonify({'message': 'No file was sent', 'status': '304 NOT MODIFED'})

        return jsonify({'message': 'The directory not exist', 'status': '304 NOT MODIFED'})

    return jsonify({'message': 'Upload Files Page', 'status': '200 '})
        



 #   [F I L E S   L I S T]   [F I L E S   L I S T]   [F I L E S   L I S T]   [F I L E S   L I S T]

@app.route("/api/v1/uploads/files-view/<proyect>/<section>", methods=["GET", "POST"])
def files_view(proyect, section):

    path = os.path.join("static", "proyects", proyect , section, "files.json")
    directory_path = os.path.join("static", "proyects", proyect)
    body = request.json 
    
    if request.method == 'GET':

        if os.path.exists(path):
            with open(path, "r") as file:
                files = json.load(file)
                return jsonify({"files": files, "message": "Files database loaded", "status": "200 OK"})

        return jsonify({"files": [], "message": "Empty database files", "status":"204 NO CONTENT"})


    if request.method == 'POST':

        if os.path.exists(directory_path):

            if not os.path.exists(path):
                with open(path, "w") as file:
                    files = []
                    files.append(body)
                    file.write(json.dumps(files, indent = 4))
                    return jsonify({"file": body, "message": "Files database updated", "status": "200 OK"})   
            else:
                with open(path, "r+") as file:
                    files = json.load(file)

                    if any(file["name"] != body["name"] for file in files):
                        files.append(body)  
                        file.seek(0)
                        json.dump(files, file, indent = 4)
                        return jsonify({"file": body, "message": "Files database updated", "status": "200 OK"})

                    return jsonify({'message': 'The file name already exist', 'status': '304 NOT MODIFED'})

        return jsonify({'message': 'The proyect not exist', 'status': '304 NOT MODIFED'})




 #  [F I L E S -  P A T H  V A R I A B L E]  [F I L E S -  P A T H  V A R I A B L E]  [F I L E S -  P A T H  V A R I A B L E]


@app.route("/api/v1/uploads/<proyect>/<section>/<file_name>", methods=['GET', 'DELETE'])
def get_file(proyect, section, file_name):


    if request.method == "GET":
  
        path = os.path.join('static', 'proyects', proyect, section)

        try:
            return send_from_directory(path, file_name, as_attachment=False)
        
        except:
            return jsonify({"path": os.path.join(path, file_name), "message": "The file not exists", "status": "204 NO CONTENT"})


    if request.method == "DELETE":
 
        path = os.path.join('static', 'proyects', proyect, section, file_name)

        if os.path.exists(path):
            os.remove(path)

            path = os.path.join('static', 'proyects', proyect, section, "files.json")
            with open(path, "r+") as file:
                files = json.load(file)
                
                for file in files:
                    if file['name'] == file_name:
                        files.remove(file)

                        with open(path, "w") as file:
                            file.write(json.dumps(files, indent = 4))
                            return jsonify({"path": os.path.join(path, file_name), "message": "File deleted successfully", "status": "200 OK"})            

        return jsonify({"path": path, "message": "The file not exists", "status": "304 NOT MODIFED"})



if __name__ == '__main__':
    app.run(debug=True, port=4000)