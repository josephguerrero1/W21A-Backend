from flask import Flask, request, Response
import dbhelpers
import json
import traceback
import sys

app = Flask(__name__)


@app.get("/api/candy_product")
def get_candy_products():
    candy_products = dbhelpers.run_select_statement(
        "SELECT name, description, image_url, weight_in_grams, price_in_dollars, id FROM candy", [])

    if(candy_products == None):
        return Response("Failed to GET candy_products", mimetype="text/plain", status=500)
    else:
        candy_products_json = json.dumps(candy_products, default=str)
        return Response(candy_products_json, mimetype="application/json", status=200)


@app.post("/api/candy_product")
def post_candy_product():
    try:
        candy_product_name = request.json['name']
        candy_product_desc = request.json['description']
        candy_product_img = request.json['image_url']
        candy_product_weight = request.json['weight_in_grams']
        candy_product_price = request.json['price_in_dollars']
    except:
        traceback.print_exc()
        return Response("Data Error", mimetype="text/plain", status=400)
    candy_product_id = dbhelpers.run_insert_statement("INSERT INTO candy (name, description, image_url, weight_in_grams, price_in_dollars) VALUES (?,?,?,?,?)",
                                                      [candy_product_name, candy_product_desc, candy_product_img, candy_product_weight, candy_product_price])
    if(candy_product_id == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        candy_product = [candy_product_name, candy_product_desc, candy_product_img,
                         candy_product_weight, candy_product_price, candy_product_id]
        candy_product_json = json.dumps(candy_product, default=str)
        return Response(candy_product_json, mimetype="application/json", status=201)


@app.delete("/api/candy_product")
def delete_candy_product():
    try:
        candy_product_id = int(request.json['id'])
    except:
        traceback.print_exc()
        return Response("Data Error", mimetype="text/plain", status=400)

    rows = dbhelpers.run_delete_statement(
        "DELETE FROM candy_product WHERE id=?", [candy_product_id, ])
    if(rows == 1):
        return Response("Candy Product Deleted", mimetype="text/plain", status=200)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern
    print("Bjoern is running.")
    bjoern.run(app, "0.0.0.0", 5016)
elif(mode == "testing"):
    # from flask_cors import CORS
    # CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()
