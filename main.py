from flask import Flask, render_template, jsonify, request
from EMLM import EMLM
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/card', methods=['POST'])
def card():
    return render_template('cardDiv.html', servClass = request.form['servClass'])

@app.route('/process', methods=['post'])
def process():
    result = request.form
    c = int(result['linkCapacity'])
    k = int(result['numOfServiceClasses'])
    a_list = []
    b_list = []
    for i in range(k):
        akey = 'trafficLoad' + str(i + 1)
        print akey 
        a_list.append(int(result[akey]))
        print a_list
        bkey = 'bwDemand' + str(i + 1) 
        b_list.append(int(result[bkey]))

    emlmObj = EMLM(c, k , b_list, a_list)
    
    qj = emlmObj.get_q()
    qj_norm = emlmObj.get_qNorm()
    congProb = emlmObj.get_pbk()
    ykj = emlmObj.get_ykj()
    U = emlmObj.get_u()
    
    print congProb
    
    results_dict = {'qj': qj, 'qj_norm': qj_norm, 'congProb': congProb, 'ykj': ykj, 'u': U}
    
    #result = {'qj': qj, 'qj_norm': qj_norm, 'congProb': congProb, 'ykj': ykj, 'u': U}
    #print result
    result = render_template('result.html', results = results_dict)

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