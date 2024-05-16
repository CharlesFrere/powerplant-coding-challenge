from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/productionplan', methods=['POST'])
def production_plan():
    data = request.json
    load = data['load']
    fuels = data['fuels']
    powerplants = data['powerplants']

    # Calculate cost per MWh for each powerplant
    for plant in powerplants:
        if plant['type'] == 'windturbine':
            plant['cost'] = 0
            plant['pmax'] = plant['pmax'] * (fuels['wind(%)'] / 100)
        elif plant['type'] == 'gasfired':
            plant['cost'] = fuels['gas(euro/MWh)'] / plant['efficiency']
        elif plant['type'] == 'turbojet':
            plant['cost'] = fuels['kerosine(euro/MWh)'] / plant['efficiency']

    # Sort powerplants by cost
    powerplants = sorted(powerplants, key=lambda x: x['cost'])

    # Allocate load to powerplants
    remaining_load = load
    result = []
    for plant in powerplants:
        if remaining_load <= 0:
            power = 0
        else:
            power = min(plant['pmax'], remaining_load)
            power = max(power, plant['pmin']) if remaining_load >= plant['pmin'] else 0
        remaining_load -= power
        result.append({"name": plant['name'], "p": round(power, 1)})

    return jsonify(result)


if __name__ == '__main__':
    app.run(port=8888)
