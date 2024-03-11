from flask import Flask, render_template_string,request,render_template
import pickle

# importing model
model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
ms =pickle.load(open('minmaxscaler.pkl','rb'))

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
			<h5 class="card-title" style="text-align:center">{{title}}</h5>
			<p class="card-text" style="text-align:center">{{ result }}</p>
            <p class="card-text" style="text-align:center">{{ description }}</p>
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
    crop_dict = {
    'rice': "Rice is a staple food for a significant portion of the world's population, particularly in Asia. It is a cereal grain and is cultivated in flooded fields called paddies.",
    'maize': "Maize is a cereal grain that is widely cultivated throughout the world. It is used for food, animal feed, and industrial purposes such as ethanol production.",
    'jute': "Jute is a long, soft, shiny vegetable fiber that is used primarily to make burlap, hessian, and gunny cloth. It is also used for making bags, ropes, and other textile materials.",
    'cotton': "Cotton is a soft, fluffy staple fiber that grows in a boll around the seeds of the cotton plant. It is used to make textiles, including clothing, bed linens, and towels.",
    'coconut': "The coconut palm produces the coconut fruit, which is used for its water, milk, oil, and flesh. Coconut is widely used in cooking, cosmetics, and traditional medicine.",
    'papaya': "Papaya is a tropical fruit with sweet, orange flesh. It is rich in vitamins, minerals, and antioxidants and is known for its digestive properties.",
    'orange': "Oranges are citrus fruits known for their juicy flesh and sweet-tart flavor. They are consumed fresh, juiced, or used in cooking and baking.",
    'apple': "Apples are one of the most widely cultivated fruits in the world. They come in various colors and flavors and are consumed fresh, cooked, or in the form of juice and cider.",
    'muskmelon': "Muskmelon, also known as cantaloupe, is a type of melon with sweet, juicy flesh. It is often eaten fresh or used in fruit salads and desserts.",
    'watermelon': "Watermelon is a large, juicy fruit with sweet, red flesh and black seeds. It is consumed fresh and is popular in summer due to its high water content.",
    'grapes': "Grapes are small, juicy fruits that grow in clusters on vines. They are consumed fresh, dried (as raisins), or used to make wine, juice, and jelly.",
    'mango': "Mango is a tropical fruit known for its sweet and juicy flesh. It is widely consumed fresh, as well as in juices, smoothies, desserts, and savory dishes.",
    'banana': "Bananas are elongated, curved fruits with a creamy flesh and a sweet taste. They are consumed fresh and are also used in baking, smoothies, and desserts.",
    'pomegranate': "Pomegranate is a fruit with a tough outer rind and juicy, seed-filled interior. It is rich in antioxidants and is consumed fresh or used in juices and salads.",
    'lentil': "Lentils are edible pulses that come in various colors, including green, brown, red, and black. They are rich in protein and fiber and are commonly used in soups, stews, and salads.",
    'blackgram': "Blackgram, also known as urad dal, is a type of pulse that is rich in protein and other nutrients. It is commonly used in Indian cuisine to make dal, curries, and snacks.",
    'mungbean': "Mungbean, also known as green gram, is a type of pulse that is rich in protein, fiber, and antioxidants. It is commonly used in Asian cuisine to make dal, sprouts, and desserts.",
    'mothbeans': "Mothbeans, also known as matki or Turkish gram, are small, brown pulses with a nutty flavor. They are commonly used in Indian cuisine to make dal, curries, and snacks.",
    'pigeonpeas': "Pigeonpeas, also known as arhar dal or toor dal, are edible pulses that are rich in protein and dietary fiber. They are commonly used in Indian cuisine to make dal, soups, and stews.",
    'kidneybeans': "Kidney beans are large, kidney-shaped pulses that are rich in protein, fiber, and various vitamins and minerals. They are commonly used in chili, soups, salads, and bean dishes.",
    'chickpea': "Chickpeas, also known as garbanzo beans, are edible pulses that are rich in protein, fiber, and other nutrients. They are commonly used in salads, soups, stews, and curries.",
    'coffee': "Coffee is a brewed beverage made from roasted coffee beans, which are the seeds of the Coffea plant. It is one of the most popular beverages worldwide and is known for its stimulating effects due to its caffeine content."
}
    N = float(request.form['Nitrogen'])
    P = float(request.form['Phosporus'])
    K = float(request.form['Potassium'])
    temp = float(request.form['Temperature'])
    humidity = float(request.form['Humidity'])
    ph = float(request.form['Ph'])
    rainfall = float(request.form['Rainfall'])
    if not (0 < N <= 141 and 5 <= P <= 146 and 5 <= K <= 206 and 9 <= temp <= 45 and 15 <= humidity <= 101 and 4 <= ph <= 11 and 21 <= rainfall <= 300):
        error_message = "Could not find the suitable crop"
        return render_template_string(index_template, result=error_message,title ='Error')
    single_pred = [[N, P, K, temp, humidity, ph, rainfall]]
    scaled_features = ms.transform(single_pred)
    final_features = sc.transform(scaled_features)
    prediction = model.predict(final_features)
    result = prediction[0]
    if result in crop_dict:
    	description = crop_dict[result]
    	return render_template_string(index_template,result = result,title ='Recommend Crop for cultivation is:',description=description)

if __name__ == "__main__":
    app.run(debug=True)