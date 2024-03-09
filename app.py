from flask import Flask, render_template_string,request,render_template
import pickle

# importing model
model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
ms = pickle.load(open('minmaxscaler.pkl','rb'))

# creating flask app
app = Flask(__name__)
index_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Crop Recommendation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
  </head>
  <style>
		h1 {
			color: mediumseagreen;
			text-align: center;
		}

		.warning {
			color: red;
			font-weight: bold;
			text-align: center;
		}
		.card{
		margin-left:410px;
		margin-top: 20px;
		color: white;
		}
		.container{
		background:#edf2f7;
		font-weight: bold;
		padding-bottom:10px;
		border-radius: 15px;
		}
    
}
	</style>




  <body style="background:#BCBBB8">
  <!--=======================navbar=====================================================-->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid center" style ="display:flex;justify-content:center;">
    <a class="navbar-brand" href="/">Crop Recommendation</a>
    
  </div>
</nav>

  <div class="container my-3 mt-3">
      <h1 class="text-success">Crop Recommendation System </h1>

<!--      adding form-->
      <form action="/predict" method="POST">
          <div class="row">
              <div class="col-md-4">
					<label for="Nitrogen">Nitrogen</label>
					<input type="number" id="Nitrogen" name="Nitrogen" placeholder="Enter Nitrogen" class="form-control" required step="0">
				</div>
               <div class="col-md-4">
					<label for="Phosporus">Phosphorus</label>
					<input type="number" id="Phosporus" name="Phosporus" placeholder="Enter Phosphorus" class="form-control" required step="00">
				</div>
				<div class="col-md-4">
					<label for="Potassium">Potassium</label>
					<input type="number" id="Potassium" name="Potassium" placeholder="Enter Potassium" class="form-control" required step="0">
				</div>
          </div>

          <div class="row mt-4">
				<div class="col-md-4">
					<label for="Temperature">Temperature</label>
					<input type="number" step="0.01" id="Temperature" name="Temperature" placeholder="Enter Temperature in °C" class="form-control" required step="0">
				</div>
				<div class="col-md-4">
					<label for="Humidity">Humidity</label>
					<input type="number" step="0.01" id="Humidity" name="Humidity" placeholder="Enter Humidity in %" class="form-control" required step="0">
				</div>
				<div class="col-md-4">
					<label for="pH">pH</label>
					<input type="number" step="0.01" id="Ph" name="Ph" placeholder="Enter pH value" class="form-control" required step="0">
				</div>
			</div>

          <div class="row mt-4">
				<div class="col-md-4">
					<label for="Rainfall">Rainfall</label>
					<input type="number" step="0.01" id="Rainfall" name="Rainfall" placeholder="Enter Rainfall in mm" class="form-control" required>
				</div>
			</div>



           <div class="row mt-4">

           <div class="col-md-12 text-center">
				<button type="submit" class="btn btn-primary btn-lg">Get Recommendation</button>
			</div>
			</div>
      </form>


  <div style="display:flex;justify-content:center;">
       {% if result %}
		<div class="card bg-dark " style="width: 18rem;margin:20px auto">
		  <div class="card-body">
			<h5 class="card-title">Recommend Crop for cultivation is:</h5>
			<p class="card-text">{{ result }}</p>
		  </div>
		</div>
        </div>
	   {% endif %}
  </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
  </body>
</html>
"""
@app.route('/')
def home():
    return render_template_string(index_template)

@app.route("/predict",methods=['POST'])
def predict():
    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    
    single_pred = [[N, P, K, temp, humidity, ph, rainfall]]

    # scaled_features = sc.transform(single_pred) 
    final_features = sc.transform(single_pred)
    prediction = model.predict(final_features)
    print("Predicted crop:", prediction[0])
    result = prediction[0]
    return render_template_string(index_template,result = result)

if __name__ == "__main__":
    app.run(debug=True)