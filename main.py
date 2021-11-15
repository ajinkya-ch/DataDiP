# """
# To-Do
# 1) make file paths absolute to avoid error from root directory
# 2) import image dp
# """
from flask import Flask, render_template, request, redirect, url_for, send_file,abort
import os
from os.path import join, dirname, realpath
from noise_add import noise_addd
from model_test import model_check
# from imagedp import privateImage

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

accuracy = ("","")
# Root URL
@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def index(req_path):
     # Set The upload HTML template '\templates\home.html'
    print("connected:), ", accuracy) 
    BASE_DIR = 'filesp'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    files = list(filter(lambda f: f.endswith('.csv'), files))

    # return render_template('page1.html', files=files)
    return render_template('page1.html', imgname='fooo.jpg',accuracy1 = accuracy[0], accuracy2 = accuracy[1],files=files )

csvfile = ""
# Get the uploaded files

def uploadFiles(request):
    global csvfile
      # get the uploaded file
    uploaded_file = request.files['csvfile']
    csvfile = uploaded_file.filename
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
    
def uploadData(request):
    feature1 = {}

    col_private_info = request.form['private']
    col_binary_vals = request.form['binary']
    categorical = request.form['categorical']
    numerical = request.form['numerical']
    epsilon = request.form['epsilon']

    col_private_info = [x.strip() for x in col_private_info.split(',')]
    col_binary_vals = [x.strip() for x in col_binary_vals.split(',')]
    categorical = [x.strip() for x in categorical.split(',')]
    numerical = [x.strip() for x in numerical.split(',')]
    epsilon = [x.strip() for x in epsilon.split(',')]

    for i in range(len(epsilon)):
        epsilon[i] = float(epsilon[i])
    
    feature1['private'] = col_private_info
    feature1['binary'] = col_binary_vals
    feature1['categorical'] = categorical
    feature1['numerical'] = numerical
    feature1['epsilon'] = epsilon
    
    nameofdownloaded = noise_addd(feature1, csvfile)
    # path = f"files/private_{csvfile}"
    # print(path)
    return send_file(nameofdownloaded, as_attachment=True)


def uploadModel(request):
    global accuracy
    feature2 = {}
    colinp = request.form['colinp']
    colop = request.form['colop']
    mlalgo = request.form['mlalgo']
    traintest = request.form['traintest']
    mlpara = request.form['mlpara']

    colinp = [x.strip() for x in colinp.split(',')]
    colop = [x.strip() for x in colop.split(',')]
    mlalgo = [x.strip() for x in mlalgo.split(',')]
    traintest = [x.strip() for x in traintest.split(',')]
    mlpara = [x.strip() for x in mlpara.split(',')]

    mlalgo = int(mlalgo[0])

    for i in range(len(traintest)):
        traintest[i] = int(traintest[i])

    for i in range(len(mlpara)):
        mlpara[i] = float(mlpara[i])
    
    feature2['colinp'] = colinp
    feature2['colop'] = colop
    feature2['mlalgo'] = mlalgo
    # print("ALGOOOOOOOOOOOOOOOOOOO",mlalgo)
    feature2['traintest'] = traintest
    feature2['mlpara'] = mlpara
    accuracy = model_check(feature2, csvfile)
    

@app.route("/", methods=['POST'])
def mainapp():
    uploadFiles(request)
    # try:
    # check = request.form['epsilon']
    # check = [x.strip() for x in check.split(',')]
    # privateImage(request.files['csvfile'].filename, check)
    # print("Image", image)
    # cv2.imsave("files/img.jpg", image) 
    # except:
    try:
        a = request.form['private']
        file = uploadData(request)
        return file
    except:
        uploadModel(request)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    #For windows you need to use drive name [ex: F:/Example.pdf]
    # path = f"files/{filename}.csv"
    return send_file(path, as_attachment=True)

if (__name__ == "__main__"):
     app.run(port = 8080)



