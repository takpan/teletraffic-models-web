from flask import Flask, render_template, jsonify, request
from EMLM import EMLM
from EnMLM import EnMLM
from EEMLM import EEMLM
from EEnMLM import EEnMLM
from SRM import SRM
from STM import STM
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
    elif model in ('enmlm', 'eenmlm'):
        return render_template('serv_class_card_enmlm.html', servClass = serviceClass)
    elif model == 'srm':
        return render_template('serv_class_card_srm.html', servClass = serviceClass)
    elif model == 'stm':
        return render_template('serv_class_card_stm.html', servClass = serviceClass)

@app.route('/getInput', methods=['POST'])
def getInput():
    model = request.form['model']
    if model == 'emlm':
        return render_template('input_emlm.html')
    elif model == 'enmlm':
        return render_template('input_enmlm.html')
    elif model == 'eemlm':
        return render_template('input_eemlm.html')
    elif model == 'eenmlm':
        return render_template('input_eenmlm.html')
    elif model in ('srm'):
        return render_template('input_srm.html')
    elif model in ('stm'):
        return render_template('input_stm.html')

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

    elif  model == 'eenmlm':
        n_list = []
        for i in range(k):
            nkey = 'totSources' + str(i + 1)
            n_list.append(int(result[nkey]))
        t = int(result['virtualLinkCapacity'])
        
        eenmlmObj = EEnMLM(c, t, k , n_list, b_list, a_list, t_list)

        qErlj = eenmlmObj.get_qErl()
        qErlNormj = eenmlmObj.get_qErlNorm()
        ykj = eenmlmObj.get_erl_ykj()
        qj = eenmlmObj.get_qEng()
        qNormj = eenmlmObj.get_qEngNorm()
        Cong_prob = eenmlmObj.get_pbk()
        U = eenmlmObj.get_u()
    
        results_dict = {'qErlj': qErlj, 'qErlNormj': qErlNormj, 'qj': qj, 'qj_norm': qNormj, 'congProb': Cong_prob, 'ykj': ykj, 'u': U}
        result = render_template('result_enmlm.html', results = results_dict)

    elif model == 'srm':
        ar_list = []
        br_list = []
        for i in range(k):
            arkey = 'retryTrafficLoad' + str(i + 1)
            ar_list.append(float(result[arkey]))
            brkey = 'rbwDemand' + str(i + 1)
            br_list.append(int(result[brkey]))

        srmObj = SRM(c, k , b_list, br_list, a_list, ar_list, t_list)
        
        qj = srmObj.get_q()
        qj_norm = srmObj.get_qNorm()
        bk = srmObj.get_bk()
        bkr = srmObj.get_bkr()
        cbkr = srmObj.get_cbkr()
        ykj = srmObj.get_ykj()
        ykrj = srmObj.get_ykrj()
        U = srmObj.get_u()
    
        results_dict = {'qj': qj, 'qj_norm': qj_norm, 'bk': bk, 'bkr': bkr, 'cbkr': cbkr, 'ykj': ykj, 'ykrj': ykrj, 'u': U}
        result = render_template('result_srm.html', results = results_dict)

    elif model == 'stm':
        ac_list = []
        bc_list = []
        for i in range(k):
            ackey = 'thresholdTrafficLoad' + str(i + 1)
            ac_list.append(float(result[ackey]))
            bckey = 'cbwDemand' + str(i + 1)
            bc_list.append(int(result[bckey]))
        j0 = int(result['threshold'])

        stmObj = STM(c, k , j0, b_list, bc_list, a_list, ac_list, t_list)

        qj = stmObj.get_q()
        qj_norm = stmObj.get_qNorm()
        bk = stmObj.get_bk()
        bkc = stmObj.get_bkc()
        cbkc = stmObj.get_cbkc()
        ykj = stmObj.get_ykj()
        ykcj = stmObj.get_ykcj()
        U = stmObj.get_u()

        results_dict = {'qj': qj, 'qj_norm': qj_norm, 'bk': bk, 'bkc': bkc, 'cbkc': cbkc, 'ykj': ykj, 'ykcj': ykcj, 'u': U}
        result = render_template('result_stm.html', results = results_dict)

    elif model == 'stm':
        ac_list = []
        bc_list = []
        for i in range(k):
            ackey = 'conditionalTrafficLoad' + str(i + 1)
            ac_list.append(float(result[ackey]))
            bckey = 'cbwDemand' + str(i + 1)
            bc_list.append(int(result[bckey]))
        j0 = int(result['threshold'])

        stmObj = STM(c, k , j0, b_list, bc_list, a_list, ac_list, t_list)
        
        qj = stmObj.get_q()
        qj_norm = stmObj.get_qNorm()
        congProb = stmObj.get_pbk()
        ykj = stmObj.get_ykj()
        U = stmObj.get_u()
    
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