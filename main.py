from flask import Flask, render_template, jsonify, request
from EMLM import EMLM
from EnMLM import EnMLM
from EEMLM import EEMLM
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/card', methods=['POST'])
def card():
    model = request.form['model']
    serviceClass = request.form['servClass']
    if model in ('emlm', 'eemlm'):
        return render_template('serv_class_card_emlm.html', servClass = serviceClass)
    elif model == 'enmlm':
        return render_template('serv_class_card_enmlm.html', servClass = serviceClass)

@app.route('/getInput', methods=['POST'])
def getInput():
    model = request.form['model']
    if model == 'emlm':
        return render_template('input_emlm.html')
    elif model == 'enmlm':
        return render_template('input_enmlm.html')
    elif model == 'eemlm':
        return render_template('input_eemlm.html')

@app.route('/process', methods=['POST'])
def process():
    result = request.form
    model = result['teletrafficModel']
    c = int(result['linkCapacity'])
    k = int(result['numOfServiceClasses'])
    a_list = []
    b_list = []
    t_list = []
    for i in range(k):
        akey = 'trafficLoad' + str(i + 1)
        a_list.append(float(result[akey]))
        bkey = 'bwDemand' + str(i + 1) 
        b_list.append(int(result[bkey]))

    if request.form.get("bwReservation") is not None:
        for i in range(k):
            tkey = 'reservedBw' + str(i + 1)
            t_list.append(int(result[tkey]))
    else:
        t_list = None

    if model == 'emlm':
        emlmObj = EMLM(c, k , b_list, a_list, t_list)
    
        qj = emlmObj.get_q()
        qj_norm = emlmObj.get_qNorm()
        congProb = emlmObj.get_pbk()
        ykj = emlmObj.get_ykj()
        U = emlmObj.get_u()
    
        results_dict = {'qj': qj, 'qj_norm': qj_norm, 'congProb': congProb, 'ykj': ykj, 'u': U}
        result = render_template('result_emlm.html', results = results_dict)
    
    elif  model == 'enmlm':
        n_list = []
        for i in range(k):
            nkey = 'totSources' + str(i + 1)
            n_list.append(int(result[nkey]))
        
        print k
        print c
        print n_list
        print b_list
        print a_list
        print t_list
        
        enmlmObj = EnMLM(c, k , n_list, b_list, a_list, t_list)

        qErlj = enmlmObj.get_qErl()
        qErlNormj = enmlmObj.get_qErlNorm()
        ykj = enmlmObj.get_erl_ykj()
        qj = enmlmObj.get_qEng()
        qNormj = enmlmObj.get_qEngNorm()
        Cong_prob = enmlmObj.get_pbk()
        U = enmlmObj.get_u()
    
        results_dict = {'qErlj': qErlj, 'qErlNormj': qErlNormj, 'qj': qj, 'qj_norm': qNormj, 'congProb': Cong_prob, 'ykj': ykj, 'u': U}
        result = render_template('result_enmlm.html', results = results_dict)
    
    elif model == 'eemlm':
        t = int(result['virtualLinkCapacity'])
        eemlmObj = EEMLM(c, t, k , b_list, a_list, t_list)
    
        qj = eemlmObj.get_q()
        qj_norm = eemlmObj.get_qNorm()
        congProb = eemlmObj.get_pbk()
        ykj = eemlmObj.get_ykj()
        U = eemlmObj.get_u()
    
        results_dict = {'qj': qj, 'qj_norm': qj_norm, 'congProb': congProb, 'ykj': ykj, 'u': U}
        result = render_template('result_emlm.html', results = results_dict)
        

    #result = {'qj': qj, 'qj_norm': qj_norm, 'congProb': congProb, 'ykj': ykj, 'u': U}
    #print result

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