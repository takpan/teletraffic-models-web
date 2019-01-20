from flask import Flask, render_template, jsonify, request
from EMLM import EMLM
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    result = request.form
    c = int(result['linkCapacity'])
    k = int(result['numOfServiceClasses'])
    a1 = int(result['trafficLoad1'])
    b1 = int(result['bwDemand1'])
    a2 = int(result['trafficLoad2'])
    b2 = int(result['bwDemand2'])
    a_list = [a1, a2]
    b_list = [b1, b2]

    emlmObj = EMLM(c, k , b_list, a_list)
    
    qj = emlmObj.get_q()
    qj_norm = emlmObj.get_qNorm()
    congProb = emlmObj.get_pbk()
    ykj = emlmObj.get_ykj()
    U = emlmObj.get_u()
    
    result = {'qj': qj, 'qj_norm': qj_norm, 'congProb': congProb, 'ykj': ykj, 'u': U}
    print result


    return jsonify(result)
#     if request.method == 'POST':
#         result = request.form
#         return render_template("index.html",result = result)

@app.route('/hello/')
def hello_name(user):
    return render_template('hello.html', name = user)

@app.route('/EMLM')
def emlm():
    return render_template('emlm.html')

if __name__ == '__main__':
    app.run(debug = True)