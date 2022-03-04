from io import StringIO
import sys
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from treelib import Tree
import markdown
import markdown.extensions.fenced_code


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

################## Database Models #########################################################
# Mind map table
class Mindmap(db.Model):
    mindmap_id = db.Column(db.Integer, primary_key=True)
    mindmap_name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"mindmap_id={self.mindmap_id} | mindmap_name={self.mindmap_name}"

# Child table
class Child(db.Model):
    child_id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(50), nullable=False)
    child_text = db.Column(db.String(50), nullable=False)
    parent_child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'), nullable=True)
    
    mindmap_id = db.Column(db.Integer, db.ForeignKey('mindmap.mindmap_id'), nullable=False)
    mindmap = db.relationship('Mindmap', backref=db.backref('root', lazy=True))

    def __repr__(self):
        return f"mindmap_id={self.mindmap} | child_id={self.child_id} | child_name={self.child_name} | parent_child_id={self.parent_child_id}"


############################ Database Creation ############################################
def create_database():
    path = 'app/database.db'

    if not os.path.exists(path):
        db.create_all()
        print('\n', "Database was created sucessfully")

create_database()


############################### Home Endpoint ############################################
@app.route('/')
def home():

    readme_file = open("app/Mindmap.md", "r")
    mrkdwn_tmp_str = markdown.markdown(readme_file.read(), extensions=["fenced_code"])
    return mrkdwn_tmp_str


########################### Mind Map Endpoint#############################################
@app.route('/mindmaps', methods=['GET'])
def get_mind_maps():
    maps = Mindmap.query.all()

    result = []
    for map in maps:
        map_data = {'id':map.mindmap_id, 'name': map.mindmap_name}
        result.append(map_data)

    return {"Mindmap": result}


# 'POST' Method
@app.route('/mindmaps', methods=['POST'])
def add_mind_map():
    map = Mindmap(mindmap_name=request.json['name'])
    db.session.add(map)
    db.session.commit()
    
    return {'id':map.mindmap_id, 'name': map.mindmap_name}, 200


####################### Leaves Endpoint ################################################
# 'GET' Method
@app.route('/mindmaps/leaves', methods=['GET'])
def get_leaves():
    map = Mindmap.query.all()
    
    result = []
    tree = Tree()
    main_root = tree.create_node(tag="root|root", identifier="root")
    for m in map:
        children = db.session.query(Child).filter(Child.mindmap_id == m.mindmap_id)

        for child in children:
            p = child.parent_child_id
            if p is None:
                tree.create_node(tag=child.child_name + "|" + child.child_text, identifier=child.child_id, parent=main_root.identifier)
            else:
                tree.create_node(tag=child.child_name + "|" + child.child_text, identifier=child.child_id, parent=p)

        id_paths = tree.paths_to_leaves()

        for i_path in id_paths:
            p_len = len(i_path) - 1
            path_to_append = ""
            text_to_append = ""
            for index, x in enumerate(i_path):
                tag = tree.get_node(x).tag
                if index == p_len:
                    path_to_append += tag.split("|")[0]
                    text_to_append = tag.split("|")[1]
                else:
                    path_to_append += tag.split("|")[0] + "/"
            
            item = {"path":path_to_append, "text":text_to_append, "map_info": m}
            result.append(str(item))

    return {"Leaves": result}


####################### Leaf Endpoint ################################################
# 'POST' Method
@app.route('/mindmaps/leaf', methods=['POST'])
def add_children():
    path=request.json['path']
    text=request.json['text']
    mindmap_id=request.json['mindmap_id']

    result = {}
    status_code = 404

    # if something is found, no error will be thrown
    # thus, the program will continue
    Mindmap.query.get_or_404(mindmap_id)

    nodes = path.split("/")

    n_len = len(nodes) - 1
    parent_id = None

    for index, n in enumerate(nodes):
        child = db.session.query(Child).filter(Child.mindmap_id == mindmap_id, Child.child_name == n).first()
        
        if index == n_len:
            if child is None:
                new_child = Child(child_name=n, child_text=text, parent_child_id=parent_id, mindmap_id=mindmap_id)
                db.session.add(new_child)
                db.session.commit()
                result= {"[Output]": f"This leaf has been successfully added"}
                status_code = 200
            else:
                result = {"[Error]": f"This leaf already exist for this mindmap"}
        elif index == 0:
            if child is None:
                new_child = Child(child_name=n, child_text="", parent_child_id=None, mindmap_id=mindmap_id)
                parent_id = new_child.child_id
                db.session.add(new_child)
                db.session.commit()
            else:
                parent_id = child.child_id
        else:
            if child is None:
                new_child = Child(child_name=n, child_text="", parent_child_id=parent_id, mindmap_id=mindmap_id)
                parent_id = new_child.child_id
                db.session.add(new_child)
                db.session.commit()
            else:
                parent_id = child.child_id
    
    return result, status_code


######################## Tree Endpoint ################################################
# 'GET' Method
@app.route('/mindmaps/tree', methods=['GET'])
def show_tree():
    map = Mindmap.query.all()
    
    result = []
    tree = Tree()
    main_root = tree.create_node(tag="root", identifier="root")
    for m in map:
        children = db.session.query(Child).filter(Child.mindmap_id == m.mindmap_id)

        for child in children:
            p = child.parent_child_id
            if p is None:
                tree.create_node(tag=child.child_name, identifier=child.child_id, parent=main_root.identifier)
            else:
                tree.create_node(tag=child.child_name, identifier=child.child_id, parent=p)
    
    with Capturing() as output:
        tree.show()
    
    # proper display when executed in commandline
    return "\n".join(output)
  
  
# to get the the output of tree.show()
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout